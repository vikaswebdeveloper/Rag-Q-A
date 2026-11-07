import csv
import io
import os
import re
import shutil
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

# Constants
Converted = {
    ".ppt": ".pptx",
    ".odp": ".pptx",
    ".doc": ".docx",
    ".odt": ".docx",
    ".rtf": ".docx",
    ".xls": ".xlsx",
    ".ods": ".xlsx",
}
Supported = {".txt", ".md", ".csv", ".pdf", ".pptx", ".docx", ".xlsx", *Converted}
RowsPerSection = 50
GenericTitles = {"powerpoint presentation", "presentation", "document", "untitled", "slide 1", "title"}
TableFormats = {".csv", ".xlsx", ".xls", ".ods"}
MaxTableRows = 500


def slugFor(filename: str | Path) -> str:
    """A .txt file's slug is its stem. Any other format's slug is <stem>-<ext>."""
    p = Path(filename)
    stem = p.stem
    ext = p.suffix.lstrip(".").lower()
    if ext == "txt" or not ext:
        return stem
    return f"{stem}-{ext}"


def titleFromName(path: str | Path) -> str:
    """The part after __, with _ replaced by spaces, in Title Case."""
    stem = Path(path).stem
    if "__" in stem:
        part = stem.split("__", 1)[1]
    else:
        part = stem
    part = part.replace("_", " ").strip()
    return part.title()


def withTitle(title: str, sections: list[str]) -> str:
    """Combine title and non-empty sections."""
    non_empty = [s.strip() for s in sections if s and s.strip()]
    if not non_empty:
        return title
    return title + "\n\n" + "\n\n".join(non_empty)


def realTitle(t: Optional[str]) -> str:
    """Returns "" if t is empty or in GenericTitles."""
    if not t:
        return ""
    clean_t = t.strip()
    if clean_t.lower() in GenericTitles:
        return ""
    return clean_t


def clean(text: str) -> str:
    """Normalise \\r\\n to \\n, remove NUL characters, collapse runs of spaces and tabs."""
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    return text


def formatRow(header: list[str], row: list[Any]) -> str:
    """Col A: value; Col B: value, skipping empty values and None."""
    parts = []
    for i, (h, val) in enumerate(zip(header, row)):
        if val is None:
            continue
        if isinstance(val, float) and val.is_integer():
            val_str = str(int(val))
        else:
            val_str = str(val).strip()
        if not val_str or val_str.lower() == "none":
            continue
        col_name = str(h).strip() if (h is not None and str(h).strip()) else f"Column {i+1}"
        parts.append(f"{col_name}: {val_str}")
    return "; ".join(parts)


def rowSections(header: list[str], rows: list[list[Any]], level: str = "==") -> list[str]:
    """Groups rows into sections of 50 with one formatted row per paragraph."""
    sections = []
    total = len(rows)
    for start_idx in range(0, total, RowsPerSection):
        chunk_rows = rows[start_idx : start_idx + RowsPerSection]
        end_idx = start_idx + len(chunk_rows)
        heading = f"{level} Rows {start_idx + 1}–{end_idx} {level}"
        paragraphs = []
        for r in chunk_rows:
            formatted = formatRow(header, r)
            if formatted:
                paragraphs.append(formatted)
        if paragraphs:
            section_content = heading + "\n\n" + "\n\n".join(paragraphs)
            sections.append(section_content)
    return sections


def _read_txt(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = clean(raw)
    lines = text.split("\n")
    first_line = lines[0].strip() if lines else ""
    if first_line and len(first_line) < 100 and not first_line.endswith((".", "!", "?")):
        title = first_line
        body = "\n".join(lines[1:]).strip()
        return f"{title}\n\n{body}" if body else title
    title = titleFromName(path)
    return f"{title}\n\n{text.strip()}"


def _read_md(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = clean(raw)
    lines = text.split("\n")
    title = ""
    content_lines = []
    found_title = False

    for line in lines:
        stripped = line.strip()
        if not found_title and stripped.startswith("# ") and not stripped.startswith("## "):
            title = stripped[2:].strip()
            found_title = True
            continue
        if stripped:
            found_title = True  # Stop looking for title once any non-empty line appears

        # Convert markdown headings to MediaWiki style
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", stripped)
        if m:
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            if level <= 2:
                content_lines.append(f"== {heading_text} ==")
            elif level == 3:
                content_lines.append(f"=== {heading_text} ===")
            else:
                content_lines.append(f"==== {heading_text} ====")
        else:
            content_lines.append(line)

    if not title:
        title = titleFromName(path)
    body = "\n".join(content_lines).strip()
    return f"{title}\n\n{body}" if body else title


def _read_csv(path: Path) -> str:
    try:
        content = path.read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError:
        content = path.read_bytes().decode("latin-1")

    sample = content[:4096]
    delimiter = ","
    try:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample, delimiters=",;\t|")
        delimiter = dialect.delimiter
    except Exception:
        pass

    reader = csv.reader(io.StringIO(content), delimiter=delimiter)
    all_rows = [row for row in reader if any(cell.strip() for cell in row)]
    if not all_rows:
        return f"{titleFromName(path)}\n\n== Columns ==\n0 rows."

    raw_header = all_rows[0]
    header = [
        str(h).strip() if str(h).strip() else f"Column {i+1}"
        for i, h in enumerate(raw_header)
    ]
    data_rows = all_rows[1:]
    total_rows = len(data_rows)

    title = titleFromName(path)
    cols_str = ", ".join(header)
    col_section = f"== Columns ==\nColumns: {cols_str}. {total_rows} rows."
    sections = [col_section]
    sections.extend(rowSections(header, data_rows, level="=="))
    return withTitle(title, sections)


def _read_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    meta = reader.metadata
    title = ""
    if meta and meta.title:
        candidate = realTitle(meta.title)
        if 3 <= len(candidate) <= 99:
            title = candidate
    if not title:
        title = titleFromName(path)

    sections = []
    for i, page in enumerate(reader.pages):
        raw_page = page.extract_text() or ""
        # Re-join hyphenated line breaks: '-\n' followed by a word character
        page_text = re.sub(r"-\n(\w)", r"\1", raw_page)
        # Turn single newlines into spaces, preserving double newlines
        paragraphs = page_text.split("\n\n")
        cleaned_paras = []
        for p in paragraphs:
            one_line = re.sub(r"\s*\n\s*", " ", p).strip()
            if one_line:
                cleaned_paras.append(one_line)
        body = "\n\n".join(cleaned_paras)
        if body:
            sections.append(f"== Page {i + 1} ==\n\n{body}")

    return withTitle(title, sections)


def _read_pptx(path: Path) -> str:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    prs = Presentation(str(path))
    title = ""
    try:
        if prs.core_properties and prs.core_properties.title:
            title = realTitle(prs.core_properties.title)
    except Exception:
        pass

    slides_content = []
    first_slide_title = ""

    def extract_shape_text(shape) -> list[str]:
        texts = []
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            for child in shape.shapes:
                texts.extend(extract_shape_text(child))
        elif shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                pt = p.text.strip()
                if pt:
                    texts.append(pt)
        elif shape.has_table:
            for row in shape.table.rows:
                row_vals = [cell.text.strip() for cell in row.cells]
                texts.append(" | ".join(row_vals))
        return texts

    for i, slide in enumerate(prs.slides):
        slide_title = ""
        try:
            if slide.shapes.title and slide.shapes.title.text:
                slide_title = realTitle(slide.shapes.title.text)
        except Exception:
            pass

        if not first_slide_title and slide_title:
            first_slide_title = slide_title

        heading = f"== Slide {i + 1}: {slide_title} ==" if slide_title else f"== Slide {i + 1} =="

        slide_texts = []
        for shape in slide.shapes:
            if shape == getattr(slide.shapes, "title", None):
                continue
            slide_texts.extend(extract_shape_text(shape))

        # Check speaker notes
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            notes = slide.notes_slide.notes_text_frame.text.strip()
            if notes:
                slide_texts.append(f"Speaker notes: {notes}")

        body = "\n\n".join(slide_texts).strip()
        slides_content.append(f"{heading}\n\n{body}" if body else heading)

    if not title:
        title = first_slide_title or titleFromName(path)

    return withTitle(title, slides_content)


def _read_docx(path: Path) -> str:
    import docx

    doc = docx.Document(str(path))
    title = ""
    sections = []
    current_heading = None
    current_paragraphs: list[str] = []

    def flush_section():
        nonlocal current_heading, current_paragraphs
        if current_heading or current_paragraphs:
            text = "\n\n".join(current_paragraphs).strip()
            if current_heading:
                sections.append(f"{current_heading}\n\n{text}" if text else current_heading)
            elif text:
                sections.append(text)
            current_heading = None
            current_paragraphs = []

    for block in doc.element.body:
        if block.tag.endswith("p"):
            p = docx.text.paragraph.Paragraph(block, doc)
            text = p.text.strip()
            if not text:
                continue
            style_name = p.style.name if p.style else ""
            if style_name == "Title" and not title:
                title = text
                continue
            m = re.match(r"^Heading\s*(\d+)$", style_name, re.IGNORECASE)
            if m:
                flush_section()
                n = int(m.group(1))
                eq_count = min(n + 1, 5)
                eqs = "=" * eq_count
                current_heading = f"{eqs} {text} {eqs}"
            else:
                current_paragraphs.append(text)
        elif block.tag.endswith("tbl"):
            t = docx.table.Table(block, doc)
            table_rows = []
            for row in t.rows:
                table_rows.append([cell.text.strip() for cell in row.cells])
            if table_rows:
                header = table_rows[0]
                for r in table_rows[1:]:
                    formatted = formatRow(header, r)
                    if formatted:
                        current_paragraphs.append(formatted)

    flush_section()

    if not title:
        title = titleFromName(path)

    return withTitle(title, sections)


def _read_xlsx(path: Path) -> str:
    import openpyxl

    wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
    title = titleFromName(path)
    sections = []

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        raw_rows = []
        for row in sheet.iter_rows(values_only=True):
            if any(cell is not None and str(cell).strip() != "" for cell in row):
                raw_rows.append(list(row))

        if not raw_rows:
            continue

        raw_header = raw_rows[0]
        header = [
            str(h).strip() if (h is not None and str(h).strip()) else f"Column {i+1}"
            for i, h in enumerate(raw_header)
        ]
        data_rows = raw_rows[1:]
        cols_summary = ", ".join(header)
        sheet_header = f"== Sheet: {sheet_name} ==\nColumns: {cols_summary}. {len(data_rows)} rows."
        sheet_sections = [sheet_header]
        sheet_sections.extend(rowSections(header, data_rows, level="==="))
        sections.append("\n\n".join(sheet_sections))

    wb.close()
    return withTitle(title, sections)


def _convert_old_format(path: Path) -> Path:
    ext = path.suffix.lower()
    target_ext = Converted.get(ext)
    if not target_ext:
        raise ValueError(f"No conversion available for {ext}")

    soffice = shutil.which("soffice")
    if not soffice:
        raise RuntimeError("LibreOffice (soffice) is required to convert legacy formats but was not found.")

    tmp_dir = tempfile.mkdtemp(prefix="rag_convert_")
    cmd = [soffice, "--headless", "--convert-to", target_ext.lstrip("."), "--outdir", tmp_dir, str(path)]
    subprocess.run(cmd, timeout=180, check=True)
    converted_file = Path(tmp_dir) / f"{path.stem}{target_ext}"
    if not converted_file.exists():
        raise RuntimeError(f"Conversion failed, expected output at {converted_file}")
    return converted_file


@lru_cache(maxsize=512)
def _extract_text_cached(abs_path: str, mtime: float) -> str:
    p = Path(abs_path)
    ext = p.suffix.lower()

    if ext in Converted:
        converted_p = _convert_old_format(p)
        try:
            return extractText(converted_p)
        finally:
            shutil.rmtree(converted_p.parent, ignore_errors=True)

    if ext == ".txt":
        return _read_txt(p)
    elif ext == ".md":
        return _read_md(p)
    elif ext == ".csv":
        return _read_csv(p)
    elif ext == ".pdf":
        return _read_pdf(p)
    elif ext == ".pptx":
        return _read_pptx(p)
    elif ext == ".docx":
        return _read_docx(p)
    elif ext == ".xlsx":
        return _read_xlsx(p)
    else:
        raise ValueError(f"Unsupported format: {ext}")


def extractText(path: str | Path) -> str:
    """The public entry point, cached on (absolute path, modification time)."""
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    return _extract_text_cached(str(p), p.stat().st_mtime)


@lru_cache(maxsize=64)
def _read_tables_cached(abs_path: str, mtime: float) -> Optional[list[dict[str, Any]]]:
    p = Path(abs_path)
    ext = p.suffix.lower()

    if ext not in TableFormats:
        return None

    if ext == ".csv":
        try:
            content = p.read_bytes().decode("utf-8-sig")
        except UnicodeDecodeError:
            content = p.read_bytes().decode("latin-1")

        sample = content[:4096]
        delimiter = ","
        try:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample, delimiters=",;\t|")
            delimiter = dialect.delimiter
        except Exception:
            pass

        reader = csv.reader(io.StringIO(content), delimiter=delimiter)
        all_rows = [row for row in reader if any(cell.strip() for cell in row)]
        if not all_rows:
            return [{"name": p.stem, "columns": [], "rows": [], "totalRows": 0}]

        max_len = max(len(r) for r in all_rows)
        raw_header = all_rows[0]
        header = [
            str(raw_header[i]).strip() if i < len(raw_header) and str(raw_header[i]).strip() else f"Column {i+1}"
            for i in range(max_len)
        ]

        data_rows = []
        for r in all_rows[1:]:
            padded = [r[i] if i < len(r) else "" for i in range(max_len)]
            data_rows.append(padded)

        return [{
            "name": p.stem,
            "columns": header,
            "rows": data_rows[:MaxTableRows],
            "totalRows": len(data_rows),
        }]

    elif ext == ".xlsx":
        import openpyxl

        wb = openpyxl.load_workbook(str(p), read_only=True, data_only=True)
        tables = []
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            raw_rows = []
            for row in sheet.iter_rows(values_only=True):
                if any(cell is not None and str(cell).strip() != "" for cell in row):
                    raw_rows.append(list(row))
            if not raw_rows:
                continue

            max_len = max(len(r) for r in raw_rows)
            raw_header = raw_rows[0]
            header = [
                str(raw_header[i]).strip() if i < len(raw_header) and raw_header[i] is not None and str(raw_header[i]).strip() else f"Column {i+1}"
                for i in range(max_len)
            ]

            data_rows = []
            for r in raw_rows[1:]:
                padded = []
                for i in range(max_len):
                    val = r[i] if i < len(r) else None
                    if isinstance(val, float) and val.is_integer():
                        padded.append(str(int(val)))
                    else:
                        padded.append(str(val) if val is not None else "")
                data_rows.append(padded)

            tables.append({
                "name": sheet_name,
                "columns": header,
                "rows": data_rows[:MaxTableRows],
                "totalRows": len(data_rows),
            })
        wb.close()
        return tables

    return None


def readTables(path: str | Path) -> Optional[list[dict[str, Any]]]:
    """For spreadsheet formats only, returns [{name, columns, rows (first 500), totalRows}]."""
    p = Path(path).resolve()
    if not p.exists():
        return None
    return _read_tables_cached(str(p), p.stat().st_mtime)

