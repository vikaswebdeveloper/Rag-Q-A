"use client";

import React, { useEffect, useState } from "react";
import { SettingsIcon } from "@/components/icons";
import { StatTile } from "@/components/admin/StatTile";
import { QuestionsChart } from "@/components/admin/QuestionsChart";
import { UsersTable } from "@/components/admin/UsersTable";
import { FeedbackList } from "@/components/admin/FeedbackList";
import { DocumentsManager } from "@/components/admin/DocumentsManager";
import { useUser } from "@/components/UserProvider";
import { AdminDoc, AdminFeedback, AdminStats, AdminUser, api } from "@/lib/api";

export default function AdminPage() {
  const { user, loading: userLoading } = useUser();

  const [activeTab, setActiveTab] = useState<"overview" | "users" | "feedback" | "documents">(
    "overview"
  );

  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [feedback, setFeedback] = useState<AdminFeedback[]>([]);
  const [documents, setDocuments] = useState<AdminDoc[]>([]);
  const [loading, setLoading] = useState(true);

  // Cross-tab interaction for Feedback "Fix" button
  const [openEditSlug, setOpenEditSlug] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [sData, uData, fbData, dData] = await Promise.all([
        api<AdminStats>("/admin/stats"),
        api<AdminUser[]>("/admin/users"),
        api<AdminFeedback[]>("/admin/feedback?rating=all&state=all"),
        api<AdminDoc[]>("/admin/documents"),
      ]);
      setStats(sData);
      setUsers(uData);
      setFeedback(fbData);
      setDocuments(dData);
    } catch (err) {
      console.error("Failed to load admin data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.is_admin) {
      loadData();
    } else if (!userLoading) {
      setLoading(false);
    }
  }, [user, userLoading]);

  // Non-admin guard
  if (!userLoading && (!user || !user.is_admin)) {
    return (
      <div className="card p-12 text-center space-y-4 my-12">
        <SettingsIcon size={44} className="mx-auto text-gold" />
        <h2 className="font-display text-3xl font-semibold text-text">Admins only</h2>
        <p className="text-sm text-muted max-w-sm mx-auto">
          Ask an administrator to grant your account access via <code>make_admin.py</code>.
        </p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="space-y-6 py-8">
        <div className="skeleton h-8 w-48" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="skeleton h-32 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  const helpfulRatio = stats
    ? stats.feedback.helpful + stats.feedback.not_helpful > 0
      ? Math.round(
          (stats.feedback.helpful / (stats.feedback.helpful + stats.feedback.not_helpful)) * 100
        )
      : 100
    : 100;

  const handleFixDocument = (slug: string) => {
    setOpenEditSlug(slug);
    setActiveTab("documents");
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div className="space-y-1">
        <div className="eyebrow">LIBRARY MANAGEMENT</div>
        <h1 className="font-display text-4xl sm:text-5xl font-semibold text-text">Admin panel</h1>
      </div>

      {/* Underline Tabs */}
      <div className="border-b border-border flex items-center gap-6 text-sm font-medium">
        <button
          type="button"
          onClick={() => setActiveTab("overview")}
          className={`pb-3 transition-colors ${
            activeTab === "overview"
              ? "border-b-2 border-accent text-accent font-semibold"
              : "text-muted hover:text-text"
          }`}
        >
          Overview
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("users")}
          className={`pb-3 flex items-center gap-1.5 transition-colors ${
            activeTab === "users"
              ? "border-b-2 border-accent text-accent font-semibold"
              : "text-muted hover:text-text"
          }`}
        >
          <span>Users</span>
          <span className="rounded-full bg-surface-2 border border-border px-1.5 py-0.2 text-[10px] tabular-nums">
            {users.length}
          </span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("feedback")}
          className={`pb-3 flex items-center gap-1.5 transition-colors ${
            activeTab === "feedback"
              ? "border-b-2 border-accent text-accent font-semibold"
              : "text-muted hover:text-text"
          }`}
        >
          <span>Feedback</span>
          {stats && stats.feedback.open > 0 && (
            <span className="rounded-full bg-accent text-on-accent px-1.5 py-0.2 text-[10px] font-semibold tabular-nums">
              {stats.feedback.open}
            </span>
          )}
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("documents")}
          className={`pb-3 flex items-center gap-1.5 transition-colors ${
            activeTab === "documents"
              ? "border-b-2 border-accent text-accent font-semibold"
              : "text-muted hover:text-text"
          }`}
        >
          <span>Documents</span>
          <span className="rounded-full bg-surface-2 border border-border px-1.5 py-0.2 text-[10px] tabular-nums">
            {documents.length}
          </span>
        </button>
      </div>

      {/* Tab Panels */}
      {activeTab === "overview" && stats && (
        <div className="space-y-8 animate-fade">
          {/* 5 StatTiles */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            <StatTile
              label="Users"
              value={stats.users.total}
              detail={`${stats.users.verified} verified · ${stats.users.new_7d} new this week`}
            />
            <StatTile
              label="Questions asked"
              value={stats.questions.total}
              detail={`${stats.questions.today} today · ${stats.questions.last_7d} this week`}
            />
            <StatTile label="Conversations" value={stats.conversations} detail="Total active threads" />
            <StatTile
              label="Documents"
              value={stats.documents.total}
              detail={`${stats.chunks.toLocaleString()} searchable chunks`}
            />
            <StatTile
              label="Answers rated helpful"
              value={`${helpfulRatio}%`}
              detail={`${stats.feedback.helpful} helpful · ${stats.feedback.not_helpful} not helpful · ${stats.feedback.open} to review`}
            />
          </div>

          {/* Questions Chart */}
          <QuestionsChart data={stats.questions.per_day} />

          {/* Breakdown Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* By Format */}
            <div className="card p-6 space-y-3">
              <h3 className="font-display text-lg font-semibold text-text">Documents by type</h3>
              <div className="space-y-2.5 pt-1">
                {Object.entries(stats.documents.by_format).map(([fmt, count]) => {
                  const pct = stats.documents.total > 0 ? (count / stats.documents.total) * 100 : 0;
                  return (
                    <div key={fmt} className="space-y-1">
                      <div className="flex justify-between text-xs font-medium">
                        <span className="uppercase text-faint">{fmt}</span>
                        <span className="tabular-nums text-text font-semibold">{count}</span>
                      </div>
                      <div className="h-1.5 w-full rounded-full bg-surface-2 overflow-hidden">
                        <div
                          style={{ width: `${pct}%` }}
                          className="h-full bg-chart rounded-full transition-all duration-700 ease-out"
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* By Category */}
            <div className="card p-6 space-y-3">
              <h3 className="font-display text-lg font-semibold text-text">Documents by category</h3>
              <div className="space-y-2.5 pt-1">
                {Object.entries(stats.documents.by_category).map(([cat, count]) => {
                  const pct = stats.documents.total > 0 ? (count / stats.documents.total) * 100 : 0;
                  return (
                    <div key={cat} className="space-y-1">
                      <div className="flex justify-between text-xs font-medium">
                        <span className="capitalize text-faint">{cat}</span>
                        <span className="tabular-nums text-text font-semibold">{count}</span>
                      </div>
                      <div className="h-1.5 w-full rounded-full bg-surface-2 overflow-hidden">
                        <div
                          style={{ width: `${pct}%` }}
                          className="h-full bg-chart rounded-full transition-all duration-700 ease-out"
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === "users" && (
        <div className="animate-fade">
          <UsersTable users={users} />
        </div>
      )}

      {activeTab === "feedback" && (
        <div className="animate-fade">
          <FeedbackList
            feedback={feedback}
            onUpdateFeedback={(updated) => {
              setFeedback((prev) => prev.map((f) => (f.id === updated.id ? updated : f)));
              loadData();
            }}
            onFixDocument={handleFixDocument}
          />
        </div>
      )}

      {activeTab === "documents" && (
        <div className="animate-fade">
          <DocumentsManager
            documents={documents}
            onRefresh={loadData}
            openEditSlug={openEditSlug}
            onClearOpenEditSlug={() => setOpenEditSlug(null)}
          />
        </div>
      )}
    </div>
  );
}

