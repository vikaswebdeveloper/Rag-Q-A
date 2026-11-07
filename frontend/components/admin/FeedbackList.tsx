"use client";

import React, { useState } from "react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import { ThumbUpIcon, ThumbDownIcon } from "@/components/icons";
import { AdminFeedback, api, reasonLabels } from "@/lib/api";

export interface FeedbackListProps {
  feedback: AdminFeedback[];
  onUpdateFeedback: (updated: AdminFeedback) => void;
  onFixDocument: (slug: string) => void;
}

export function FeedbackList({
  feedback,
  onUpdateFeedback,
  onFixDocument,
}: FeedbackListProps) {
  const [filterRating, setFilterRating] = useState<"not_helpful" | "helpful" | "all">("not_helpful");
  const [filterState, setFilterState] = useState<"open" | "resolved" | "all">("open");
  const [notesState, setNotesState] = useState<Record<string, string>>({});

  const handleNoteChange = (id: string, text: string) => {
    setNotesState((prev) => ({ ...prev, [id]: text }));
  };

  const handleSaveNote = async (item: AdminFeedback) => {
    const currentNote = notesState[item.id] !== undefined ? notesState[item.id] : item.admin_note || "";
    try {
      const updated = await api<AdminFeedback>(`/admin/feedback/${item.id}`, {
        method: "PATCH",
        json: { admin_note: currentNote },
      });
      onUpdateFeedback(updated);
    } catch (err) {
      console.error("Failed to save admin note", err);
    }
  };

  const handleToggleStatus = async (item: AdminFeedback) => {
    const nextStatus = item.status === "open" ? "resolved" : "open";
    try {
      const updated = await api<AdminFeedback>(`/admin/feedback/${item.id}`, {
        method: "PATCH",
        json: { status: nextStatus },
      });
      onUpdateFeedback(updated);
    } catch (err) {
      console.error("Failed to toggle status", err);
    }
  };

  const filteredItems = feedback.filter((item) => {
    if (filterRating === "not_helpful" && item.rating !== -1) return false;
    if (filterRating === "helpful" && item.rating !== 1) return false;
    if (filterState === "open" && item.status !== "open") return false;
    if (filterState === "resolved" && item.status !== "resolved") return false;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Filters Toolbar */}
      <div className="card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => {
              setFilterRating("not_helpful");
              setFilterState("open");
            }}
            aria-pressed={filterRating === "not_helpful" && filterState === "open"}
            className="chip text-xs"
          >
            To review
          </button>
          <button
            type="button"
            onClick={() => {
              setFilterRating("all");
              setFilterState("resolved");
            }}
            aria-pressed={filterState === "resolved"}
            className="chip text-xs"
          >
            Resolved
          </button>
          <button
            type="button"
            onClick={() => {
              setFilterRating("helpful");
              setFilterState("all");
            }}
            aria-pressed={filterRating === "helpful"}
            className="chip text-xs"
          >
            Helpful
          </button>
          <button
            type="button"
            onClick={() => {
              setFilterRating("all");
              setFilterState("all");
            }}
            aria-pressed={filterRating === "all" && filterState === "all"}
            className="chip text-xs"
          >
            All
          </button>
        </div>

        <p className="text-xs text-muted">
          Only answers that users rated are shown — rating shares that question and answer.
        </p>
      </div>

      {/* List */}
      {filteredItems.length === 0 ? (
        <div className="card p-12 text-center space-y-2">
          <p className="font-display text-2xl font-semibold text-text">All caught up</p>
          <p className="text-xs text-muted">No feedback items match this filter.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredItems.map((item) => {
            const isHelpful = item.rating === 1;
            const currentNote =
              notesState[item.id] !== undefined ? notesState[item.id] : item.admin_note || "";
            const noteChanged = currentNote !== (item.admin_note || "");

            return (
              <div key={item.id} className="card p-6 space-y-4">
                {/* Header Row */}
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border/50 pb-3">
                  <div className="flex items-center gap-2">
                    <div
                      className={`flex h-7 w-7 items-center justify-center rounded-full border ${
                        isHelpful
                          ? "border-success bg-success/15 text-success"
                          : "border-danger bg-danger/15 text-danger"
                      }`}
                    >
                      {isHelpful ? <ThumbUpIcon size={14} /> : <ThumbDownIcon size={14} />}
                    </div>

                    {item.reason && (
                      <span className="badge badge-danger">
                        {reasonLabels[item.reason] || item.reason}
                      </span>
                    )}

                    <span
                      className={`badge ${
                        item.status === "open" ? "badge-warning" : "badge-success"
                      }`}
                    >
                      {item.status === "open" ? "Open" : "Resolved"}
                    </span>
                  </div>

                  <div className="text-xs text-muted">
                    {item.user ? `${item.user.name} (${item.user.email})` : "Anonymous"} ·{" "}
                    {new Date(item.created_at).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>
                </div>

                {/* Question */}
                <h4 className="font-display text-xl font-semibold text-text">
                  “{item.question}”
                </h4>

                {/* Collapsible Answer & User Comment */}
                <details className="text-xs text-muted space-y-3 cursor-pointer">
                  <summary className="font-medium text-text hover:text-accent">
                    Answer given
                  </summary>
                  <div className="mt-2.5 rounded-lg border border-border bg-surface-2 p-3.5 space-y-3">
                    <div className="md prose-doc !text-xs leading-5">
                      <ReactMarkdown>{item.answer}</ReactMarkdown>
                    </div>

                    {item.comment && (
                      <blockquote className="border-l-2 border-gold pl-3 py-1 font-serif italic text-text text-sm">
                        “{item.comment}”
                      </blockquote>
                    )}
                  </div>
                </details>

                {/* Sources Used with View & Fix */}
                {item.sources && item.sources.length > 0 && (
                  <div className="space-y-1.5 pt-1">
                    <span className="eyebrow text-[0.65rem]">SOURCES USED</span>
                    <div className="flex flex-wrap gap-2">
                      {item.sources.map((src, sIdx) => (
                        <div
                          key={sIdx}
                          className="flex items-center gap-1.5 rounded-md border border-border bg-surface-2 px-2.5 py-1 text-xs"
                        >
                          <span className="font-medium text-text">{src.slug}</span>
                          <span className="text-faint">({src.section})</span>
                          <div className="flex items-center gap-1 ml-1 border-l border-border pl-1.5">
                            <Link
                              href={`/documents/${src.slug}`}
                              className="text-accent hover:underline font-semibold text-[11px]"
                            >
                              View
                            </Link>
                            <span className="text-border">|</span>
                            <button
                              type="button"
                              onClick={() => onFixDocument(src.slug)}
                              className="text-accent hover:underline font-semibold text-[11px]"
                            >
                              Fix
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Admin Note & Resolution Controls */}
                <div className="pt-3 border-t border-border/50 flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                  <div className="flex-1">
                    <textarea
                      value={currentNote}
                      onChange={(e) => handleNoteChange(item.id, e.target.value)}
                      placeholder="Add an internal note or action taken…"
                      rows={1}
                      maxLength={2000}
                      className="field text-xs py-1.5"
                    />
                  </div>

                  <div className="flex items-center justify-end gap-2 flex-shrink-0">
                    {noteChanged && (
                      <button
                        type="button"
                        onClick={() => handleSaveNote(item)}
                        className="btn btn-secondary btn-sm"
                      >
                        Save note
                      </button>
                    )}

                    <button
                      type="button"
                      onClick={() => handleToggleStatus(item)}
                      className={`btn btn-sm ${
                        item.status === "open" ? "btn-primary" : "btn-secondary"
                      }`}
                    >
                      {item.status === "open" ? "Mark resolved" : "Reopen"}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

