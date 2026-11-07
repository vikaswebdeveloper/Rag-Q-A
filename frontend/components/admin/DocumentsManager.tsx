"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { AdminDoc, api } from "@/lib/api";
import { Notice } from "@/components/AuthShell";

export interface DocumentsManagerProps {
  documents: AdminDoc[];
  onRefresh: () => void;
  openEditSlug?: string | null;
  onClearOpenEditSlug?: () => void;
}

export function DocumentsManager({
  documents,
  onRefresh,
  openEditSlug,
  onClearOpenEditSlug,
}: DocumentsManagerProps) {
  // Upload State
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadCategory, setUploadCategory] = useState<string>("general");
  const [isNewCategory, setIsNewCategory] = useState(false);
  const [customCategory, setCustomCategory] = useState("");
  const [uploadName, setUploadName] = useState("");
  const [replaceExisting, setReplaceExisting] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadNotice, setUploadNotice] = useState<{ tone: "success" | "error"; msg: string } | null>(null);

  // Table Filters
  const [tableSearch, setTableSearch] = useState("");
  const [tableCategory, setTableCategory] = useState("all");

  // Modals: "edit" | "rename" | "replace" | "delete"
  const [activeModal, setActiveModal] = useState<"edit" | "rename" | "replace" | "delete" | null>(null);
  const [selectedDoc, setSelectedDoc] = useState<AdminDoc | null>(null);

  // Edit Modal State
  const [editText, setEditText] = useState("");
  const [editLoading, setEditLoading] = useState(false);

  // Rename Modal State
  const [renameCategory, setRenameCategory] = useState("");
  const [renameName, setRenameName] = useState("");
  const [renameLoading, setRenameLoading] = useState(false);

  // Replace Modal State
  const [replaceFile, setReplaceFile] = useState<File | null>(null);
  const [replaceLoading, setReplaceLoading] = useState(false);

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Existing categories
  const categories = useMemo(() => {
    const set = new Set<string>();
    for (const d of documents) {
      if (d.category) set.add(d.category.toLowerCase());
    }
    return Array.from(set).sort();
  }, [documents]);

  // Check if any document is queued or indexing -> poll every 2s
  useEffect(() => {
    const hasPending = documents.some(
      (d) => d.index_state === "queued" || d.index_state === "indexing"
    );
    if (!hasPending) return;

    const interval = setInterval(() => {
      onRefresh();
    }, 2000);
    return () => clearInterval(interval);
  }, [documents, onRefresh]);

  // Handle auto-opening edit modal when openEditSlug is provided (e.g. from Feedback "Fix")
  useEffect(() => {
    if (openEditSlug) {
      const target = documents.find((d) => d.slug === openEditSlug);
      if (target) {
        if (target.editable) {
          openEditModal(target);
        } else {
          openReplaceModal(target);
        }
      }
      onClearOpenEditSlug?.();
    }
  }, [openEditSlug, documents]);

  // Filtered documents
  const filteredDocs = useMemo(() => {
    return documents.filter((d) => {
      if (tableCategory !== "all" && d.category.toLowerCase() !== tableCategory.toLowerCase()) {
        return false;
      }
      if (tableSearch.trim()) {
        const q = tableSearch.toLowerCase().trim();
        return (
          d.title.toLowerCase().includes(q) ||
          d.file.toLowerCase().includes(q) ||
          d.slug.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [documents, tableCategory, tableSearch]);

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;

    const finalCat = isNewCategory ? customCategory.trim() : uploadCategory;
    if (!finalCat) {
      setUploadNotice({ tone: "error", msg: "Please specify a category." });
      return;
    }

    setUploadLoading(true);
    setUploadNotice(null);

    const formData = new FormData();
    formData.append("file", uploadFile);
    formData.append("category", finalCat);
    if (uploadName.trim()) {
      formData.append("name", uploadName.trim());
    }
    formData.append("replace", String(replaceExisting));

    try {
      const res = await fetch("/api/admin/documents", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        let errDetail = `Upload failed (${res.status})`;
        try {
          const j = await res.json();
          errDetail = j.detail || errDetail;
        } catch {}
        setUploadNotice({ tone: "error", msg: errDetail });
      } else {
        setUploadNotice({ tone: "success", msg: "Document uploaded and queued for indexing!" });
        setUploadFile(null);
        setUploadName("");
        if (fileInputRef.current) fileInputRef.current.value = "";
        onRefresh();
      }
    } catch (err: any) {
      setUploadNotice({ tone: "error", msg: err.message || "Failed to upload document." });
    } finally {
      setUploadLoading(false);
    }
  };

  const openEditModal = async (doc: AdminDoc) => {
    setSelectedDoc(doc);
    setActiveModal("edit");
    setEditLoading(true);
    try {
      const data = await api<{ file: string; text: string }>(`/admin/documents/${doc.slug}/content`);
      setEditText(data.text);
    } catch (err) {
      console.error("Failed to load text for editing", err);
      setActiveModal(null);
    } finally {
      setEditLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!selectedDoc) return;
    setEditLoading(true);
    try {
      await api(`/admin/documents/${selectedDoc.slug}/content`, {
        method: "PUT",
        json: { text: editText },
      });
      setActiveModal(null);
      onRefresh();
    } catch (err) {
      console.error("Failed to save content", err);
    } finally {
      setEditLoading(false);
    }
  };

  const openRenameModal = (doc: AdminDoc) => {
    setSelectedDoc(doc);
    setRenameCategory(doc.category);
    const stem = doc.file.includes("__") ? doc.file.split("__")[1] : doc.file;
    const nameWithoutExt = stem.replace(/\.[a-z0-9]+$/i, "");
    setRenameName(nameWithoutExt);
    setActiveModal("rename");
  };

  const handleSaveRename = async () => {
    if (!selectedDoc) return;
    setRenameLoading(true);
    try {
      await api(`/admin/documents/${selectedDoc.slug}`, {
        method: "PATCH",
        json: { category: renameCategory, name: renameName },
      });
      setActiveModal(null);
      onRefresh();
    } catch (err) {
      console.error("Failed to rename document", err);
    } finally {
      setRenameLoading(false);
    }
  };

  const openReplaceModal = (doc: AdminDoc) => {
    setSelectedDoc(doc);
    setReplaceFile(null);
    setActiveModal("replace");
  };

  const handleSaveReplace = async () => {
    if (!selectedDoc || !replaceFile) return;
    setReplaceLoading(true);

    const formData = new FormData();
    formData.append("file", replaceFile);
    formData.append("category", selectedDoc.category);
    const stem = selectedDoc.file.includes("__") ? selectedDoc.file.split("__")[1] : selectedDoc.file;
    const nameWithoutExt = stem.replace(/\.[a-z0-9]+$/i, "");
    formData.append("name", nameWithoutExt);
    formData.append("replace", "true");

    try {
      const res = await fetch("/api/admin/documents", {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        setActiveModal(null);
        onRefresh();
      }
    } catch (err) {
      console.error("Replace failed", err);
    } finally {
      setReplaceLoading(false);
    }
  };

  const openDeleteModal = (doc: AdminDoc) => {
    setSelectedDoc(doc);
    setActiveModal("delete");
  };

  const handleConfirmDelete = async () => {
    if (!selectedDoc) return;
    try {
      await api(`/admin/documents/${selectedDoc.slug}`, { method: "DELETE" });
      setActiveModal(null);
      onRefresh();
    } catch (err) {
      console.error("Delete failed", err);
    }
  };

  return (
    <div className="space-y-8">
      {/* 1. Upload Card */}
      <div className="card p-6 space-y-4">
        <h3 className="font-display text-xl font-semibold text-text">Upload New Volume</h3>

        {uploadNotice && (
          <Notice tone={uploadNotice.tone}>
            <p>{uploadNotice.msg}</p>
          </Notice>
        )}

        <form onSubmit={handleUploadSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* File Input */}
            <div className="space-y-1">
              <label className="text-xs font-semibold uppercase tracking-wider text-muted">
                File (Max 25 MB)
              </label>
              <input
                ref={fileInputRef}
                type="file"
                required
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                className="field text-xs py-1.5"
              />
            </div>

            {/* Category Select */}
            <div className="space-y-1">
              <label className="text-xs font-semibold uppercase tracking-wider text-muted">
                Category
              </label>
              {!isNewCategory ? (
                <div className="flex gap-2">
                  <select
                    value={uploadCategory}
                    onChange={(e) => {
                      if (e.target.value === "__NEW__") {
                        setIsNewCategory(true);
                      } else {
                        setUploadCategory(e.target.value);
                      }
                    }}
                    className="field text-xs py-2 capitalize"
                  >
                    {categories.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                    <option value="__NEW__">+ New category…</option>
                  </select>
                </div>
              ) : (
                <div className="flex gap-2">
                  <input
                    type="text"
                    required
                    value={customCategory}
                    onChange={(e) => setCustomCategory(e.target.value)}
                    placeholder="e.g. astronomy"
                    className="field text-xs py-2"
                  />
                  <button
                    type="button"
                    onClick={() => setIsNewCategory(false)}
                    className="btn btn-ghost btn-sm"
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>

            {/* Optional Custom Name */}
            <div className="space-y-1">
              <label className="text-xs font-semibold uppercase tracking-wider text-muted">
                Name (Optional)
              </label>
              <input
                type="text"
                value={uploadName}
                onChange={(e) => setUploadName(e.target.value)}
                placeholder="Leave blank to use filename"
                className="field text-xs py-2"
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            <label className="flex items-center gap-2 text-xs text-muted cursor-pointer">
              <input
                type="checkbox"
                checked={replaceExisting}
                onChange={(e) => setReplaceExisting(e.target.checked)}
                className="rounded border-border"
              />
              <span>Replace if file already exists</span>
            </label>

            <button type="submit" disabled={uploadLoading || !uploadFile} className="btn btn-primary btn-sm">
              {uploadLoading ? "Uploading…" : "Upload & Index"}
            </button>
          </div>
        </form>
      </div>

      {/* 2. Documents Table Card */}
      <div className="card overflow-hidden">
        {/* Table Toolbar */}
        <div className="border-b border-border bg-surface p-4 flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
          <input
            type="text"
            value={tableSearch}
            onChange={(e) => setTableSearch(e.target.value)}
            placeholder="Search documents by title or filename…"
            className="field text-xs py-1.5 sm:max-w-xs"
          />

          <div className="flex items-center gap-2 text-xs">
            <span className="font-semibold uppercase text-faint">Category:</span>
            <select
              value={tableCategory}
              onChange={(e) => setTableCategory(e.target.value)}
              className="field text-xs py-1.5 w-36 capitalize"
            >
              <option value="all">All</option>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b border-border bg-surface-2 text-xs font-semibold uppercase tracking-wider text-faint">
                <th className="py-3 px-4">Document</th>
                <th className="py-3 px-3">Category</th>
                <th className="py-3 px-2">Type</th>
                <th className="py-3 px-3 text-right">Size</th>
                <th className="py-3 px-3 text-right">Chunks</th>
                <th className="py-3 px-3">Search Index</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredDocs.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-xs text-muted">
                    No documents found matching filters.
                  </td>
                </tr>
              ) : (
                filteredDocs.map((doc) => {
                  let badge = <span className="badge badge-warning">Not indexed</span>;
                  if (doc.index_state === "ready") {
                    badge = <span className="badge badge-success">Ready</span>;
                  } else if (doc.index_state === "indexing" || doc.index_state === "queued") {
                    badge = <span className="badge badge-warning animate-pulse capitalize">{doc.index_state}</span>;
                  } else if (doc.index_state === "error") {
                    badge = (
                      <span className="badge badge-danger" title={doc.index_detail}>
                        Error
                      </span>
                    );
                  }

                  return (
                    <tr
                      key={doc.slug}
                      className="border-b border-border/40 transition-colors hover:bg-surface-2"
                    >
                      <td className="py-3 px-4">
                        <div className="font-medium text-text">{doc.title}</div>
                        <div className="font-mono text-[11px] text-faint">{doc.file}</div>
                      </td>
                      <td className="py-3 px-3 text-xs capitalize text-muted">{doc.category}</td>
                      <td className="py-3 px-2 font-mono text-xs uppercase text-faint">{doc.format}</td>
                      <td className="py-3 px-3 text-right tabular-nums text-xs text-muted">
                        {(doc.size / 1024).toFixed(1)} KB
                      </td>
                      <td className="py-3 px-3 text-right tabular-nums text-xs font-medium text-text">
                        {doc.chunks}
                      </td>
                      <td className="py-3 px-3">{badge}</td>
                      <td className="py-3 px-4 text-right">
                        <div className="flex items-center justify-end gap-1.5 text-xs font-semibold">
                          <Link href={`/documents/${doc.slug}`} className="link">
                            View
                          </Link>
                          {doc.editable && (
                            <>
                              <span className="text-border">·</span>
                              <button
                                type="button"
                                onClick={() => openEditModal(doc)}
                                className="link"
                              >
                                Edit
                              </button>
                            </>
                          )}
                          <span className="text-border">·</span>
                          <button
                            type="button"
                            onClick={() => openRenameModal(doc)}
                            className="link"
                          >
                            Rename
                          </button>
                          <span className="text-border">·</span>
                          <button
                            type="button"
                            onClick={() => openReplaceModal(doc)}
                            className="link"
                          >
                            Replace
                          </button>
                          <span className="text-border">·</span>
                          <button
                            type="button"
                            onClick={() => openDeleteModal(doc)}
                            className="text-danger hover:underline font-semibold"
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* MODALS */}
      {activeModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-[2px] animate-fade"
          onClick={() => setActiveModal(null)}
        >
          <div
            className="card animate-rise w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col bg-surface shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="border-b border-border p-4 flex items-center justify-between">
              <h3 className="font-display text-xl font-semibold capitalize text-text">
                {activeModal} {selectedDoc?.title}
              </h3>
              <button
                type="button"
                onClick={() => setActiveModal(null)}
                className="text-muted hover:text-text p-1"
              >
                ✕
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 flex-1 overflow-y-auto space-y-4">
              {/* EDIT MODAL */}
              {activeModal === "edit" && (
                <div className="space-y-3">
                  <div className="text-xs text-muted">
                    Format: {selectedDoc?.format.toUpperCase()} ·{" "}
                    {selectedDoc?.format === "csv"
                      ? "The first row holds the column names."
                      : selectedDoc?.format === "md"
                      ? "# and ## headings become sections."
                      : "Lines like == Heading == become sections."}
                  </div>
                  <textarea
                    value={editText}
                    onChange={(e) => setEditText(e.target.value)}
                    rows={16}
                    maxLength={5_000_000}
                    className="field font-mono text-xs leading-5"
                  />
                  <div className="text-xs text-faint text-right">
                    {editText.length.toLocaleString()} / 5,000,000 characters
                  </div>
                </div>
              )}

              {/* RENAME MODAL */}
              {activeModal === "rename" && (
                <div className="space-y-4">
                  <Notice tone="error">
                    <p className="text-xs">Warning: Old links to this document will stop working.</p>
                  </Notice>

                  <div className="space-y-1">
                    <label className="text-xs font-semibold uppercase text-muted">Category</label>
                    <input
                      type="text"
                      required
                      value={renameCategory}
                      onChange={(e) => setRenameCategory(e.target.value)}
                      className="field text-sm"
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs font-semibold uppercase text-muted">Document Name</label>
                    <input
                      type="text"
                      required
                      value={renameName}
                      onChange={(e) => setRenameName(e.target.value)}
                      className="field text-sm"
                    />
                  </div>
                </div>
              )}

              {/* REPLACE MODAL */}
              {activeModal === "replace" && (
                <div className="space-y-3">
                  <p className="text-xs text-muted">
                    Upload a replacement file. It must have the same extension (
                    <strong>.{selectedDoc?.format}</strong>).
                  </p>
                  <input
                    type="file"
                    accept={`.${selectedDoc?.format}`}
                    required
                    onChange={(e) => setReplaceFile(e.target.files?.[0] || null)}
                    className="field text-xs py-2"
                  />
                </div>
              )}

              {/* DELETE MODAL */}
              {activeModal === "delete" && (
                <div className="space-y-3">
                  <p className="text-sm text-text">
                    Are you sure you want to delete <strong>{selectedDoc?.file}</strong>?
                  </p>
                  <p className="text-xs text-muted">
                    The file will be safely moved to <code>backend/trash/</code> and its search
                    chunks will be removed immediately.
                  </p>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="border-t border-border p-4 flex justify-end gap-2 bg-surface-2">
              <button
                type="button"
                onClick={() => setActiveModal(null)}
                className="btn btn-secondary btn-sm"
              >
                Cancel
              </button>

              {activeModal === "edit" && (
                <button
                  type="button"
                  onClick={handleSaveEdit}
                  disabled={editLoading}
                  className="btn btn-primary btn-sm"
                >
                  {editLoading ? "Saving…" : "Save Changes"}
                </button>
              )}

              {activeModal === "rename" && (
                <button
                  type="button"
                  onClick={handleSaveRename}
                  disabled={renameLoading}
                  className="btn btn-primary btn-sm"
                >
                  {renameLoading ? "Renaming…" : "Rename"}
                </button>
              )}

              {activeModal === "replace" && (
                <button
                  type="button"
                  onClick={handleSaveReplace}
                  disabled={replaceLoading || !replaceFile}
                  className="btn btn-primary btn-sm"
                >
                  {replaceLoading ? "Replacing…" : "Upload Replacement"}
                </button>
              )}

              {activeModal === "delete" && (
                <button
                  type="button"
                  onClick={handleConfirmDelete}
                  className="btn btn-danger btn-sm"
                >
                  Delete Volume
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

