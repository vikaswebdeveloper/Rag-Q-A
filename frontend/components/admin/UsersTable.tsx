import React from "react";
import { AdminUser } from "@/lib/api";

export function UsersTable({ users }: { users: AdminUser[] }) {
  return (
    <div className="card overflow-hidden">
      <div className="border-b border-border bg-surface px-6 py-4 flex items-center justify-between">
        <h3 className="font-display text-xl font-semibold text-text">Registered Readers</h3>
        <span className="text-xs text-muted">
          Counts only — what users asked stays private to them.
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm border-collapse">
          <thead>
            <tr className="border-b border-border bg-surface-2 text-xs font-semibold uppercase tracking-wider text-faint">
              <th className="py-3 px-5">User</th>
              <th className="py-3 px-4">Joined</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4 text-right">Conversations</th>
              <th className="py-3 px-4 text-right">Questions</th>
              <th className="py-3 px-5">Last Active</th>
            </tr>
          </thead>
          <tbody>
            {users.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-8 text-center text-xs text-muted">
                  No accounts found.
                </td>
              </tr>
            ) : (
              users.map((u) => (
                <tr
                  key={u.id}
                  className="border-b border-border/40 transition-colors hover:bg-surface-2"
                >
                  <td className="py-3 px-5">
                    <div className="font-medium text-text">{u.name}</div>
                    <div className="text-xs text-muted">{u.email}</div>
                  </td>
                  <td className="py-3 px-4 text-xs text-muted">
                    {new Date(u.joined).toLocaleDateString(undefined, {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex flex-wrap gap-1">
                      {u.is_admin && <span className="badge badge-accent">Admin</span>}
                      {u.verified ? (
                        <span className="badge badge-success">Verified</span>
                      ) : (
                        <span className="badge badge-warning">Unverified</span>
                      )}
                    </div>
                  </td>
                  <td className="py-3 px-4 text-right tabular-nums text-xs font-medium text-text">
                    {u.conversations}
                  </td>
                  <td className="py-3 px-4 text-right tabular-nums text-xs font-medium text-text">
                    {u.questions}
                  </td>
                  <td className="py-3 px-5 text-xs text-muted">
                    {u.last_active
                      ? new Date(u.last_active).toLocaleDateString(undefined, {
                          month: "short",
                          day: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })
                      : "Never"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

