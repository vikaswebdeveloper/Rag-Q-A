import React from "react";

export interface StatTileProps {
  label: string;
  value: string | number;
  detail?: string;
}

export function StatTile({ label, value, detail }: StatTileProps) {
  return (
    <div className="card card-hover relative overflow-hidden p-6 flex flex-col justify-between">
      {/* 3px Top Accent to Gold Gradient Bar */}
      <div
        className="absolute inset-x-0 top-0 h-[3px]"
        style={{
          background: "linear-gradient(90deg, var(--accent), var(--gold))",
        }}
      />

      <div>
        <span className="text-[0.68rem] font-semibold uppercase tracking-[0.22em] text-faint">
          {label}
        </span>
        <div className="mt-2 font-display text-4xl font-semibold text-text tabular-nums">
          {value}
        </div>
      </div>

      {detail && (
        <div className="mt-4 pt-3 border-t border-border/50 text-xs text-muted">
          {detail}
        </div>
      )}
    </div>
  );
}

