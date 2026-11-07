import React from "react";
import { Table } from "@/lib/api";
import { categoryStyle } from "@/lib/theme";

export interface DataTableProps {
  table: Table;
  category: string;
}

function prettifyHeader(header: string): string {
  if (!header) return "";
  const spaced = header.replace(/_/g, " ").trim();
  return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}

function isNumericColumn(values: (string | number)[][], colIndex: number): boolean {
  if (values.length === 0) return false;
  const numRegex = /^[-+]?[\d,]*\.?\d+%?$/;
  return values.every((row) => {
    const val = row[colIndex];
    if (val === undefined || val === null || val === "") return true;
    return numRegex.test(String(val).trim());
  });
}

export function DataTable({ table, category }: DataTableProps) {
  const theme = categoryStyle(category);
  const totalRows = table.totalRows || table.rows.length;
  const isTruncated = table.rows.length < totalRows;

  // Determine numeric alignment for each column
  const colIsNumeric = table.columns.map((_, idx) => isNumericColumn(table.rows, idx));

  return (
    <div className="card my-6 overflow-hidden">
      {/* Header */}
      <div className="border-b border-border bg-surface px-6 py-4 flex items-center justify-between">
        <h3 className="font-display text-xl font-semibold text-text">
          {table.name || "Data Table"}
        </h3>
        <span className="text-xs uppercase font-medium tracking-wider text-faint">
          {totalRows} ROWS × {table.columns.length} COLUMNS
        </span>
      </div>

      {/* Table Container */}
      <div className="overflow-x-auto max-h-[70vh] relative">
        <table className="w-full text-left text-sm border-collapse">
          {/* Sticky Header */}
          <thead className="sticky top-0 z-[2] shadow-sm">
            <tr style={{ backgroundColor: theme.color }} className="text-white">
              <th className="py-2.5 px-3 text-xs font-semibold uppercase tracking-wider text-white/70 w-12 text-center">
                #
              </th>
              {table.columns.map((col, idx) => (
                <th
                  key={idx}
                  className={`py-2.5 px-4 text-xs font-semibold uppercase tracking-wider ${
                    colIsNumeric[idx] ? "text-right" : "text-left"
                  }`}
                >
                  {prettifyHeader(col)}
                </th>
              ))}
            </tr>
          </thead>

          {/* Rows */}
          <tbody>
            {table.rows.map((row, rowIdx) => (
              <tr
                key={rowIdx}
                className={`transition-colors hover:bg-gold-soft ${
                  rowIdx % 2 === 0 ? "bg-surface" : "bg-surface-2"
                }`}
              >
                <td className="py-2 px-3 text-xs text-faint text-center border-b border-border/50 tabular-nums">
                  {rowIdx + 1}
                </td>
                {row.map((cell, colIdx) => (
                  <td
                    key={colIdx}
                    className={`py-2.5 px-4 text-sm text-text border-b border-border/50 ${
                      colIdx === 0 ? "font-medium" : ""
                    } ${colIsNumeric[colIdx] ? "text-right tabular-nums" : "text-left"}`}
                  >
                    {cell !== null && cell !== undefined ? String(cell) : ""}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Footer */}
      {isTruncated && (
        <div className="border-t border-border bg-surface-2 px-6 py-2.5 text-xs text-muted">
          Showing the first {table.rows.length} of {totalRows} rows.
        </div>
      )}
    </div>
  );
}

