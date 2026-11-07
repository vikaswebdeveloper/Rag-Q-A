"use client";

import React, { useMemo, useState } from "react";

export interface QuestionsChartProps {
  data: { date: string; count: number }[];
}

function getNiceMax(rawMax: number): number {
  if (rawMax <= 4) return 4;
  let power = Math.pow(10, Math.floor(Math.log10(rawMax)));
  let fraction = rawMax / power;
  let niceFraction = 1;
  if (fraction <= 1) niceFraction = 1;
  else if (fraction <= 2) niceFraction = 2;
  else if (fraction <= 5) niceFraction = 5;
  else niceFraction = 10;
  return niceFraction * power;
}

export function QuestionsChart({ data }: QuestionsChartProps) {
  const [viewAsTable, setViewAsTable] = useState(false);
  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);

  const { maxVal, peakIdx } = useMemo(() => {
    let peak = 0;
    let pIdx = -1;
    for (let i = 0; i < data.length; i++) {
      if (data[i].count > peak) {
        peak = data[i].count;
        pIdx = i;
      }
    }
    return { maxVal: getNiceMax(peak), peakIdx: pIdx };
  }, [data]);

  return (
    <div className="card p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-display text-xl font-semibold text-text">
          Questions per day · last 14 days
        </h3>
        <button
          type="button"
          onClick={() => setViewAsTable(!viewAsTable)}
          className="link text-xs font-medium"
        >
          {viewAsTable ? "View as chart" : "View as table"}
        </button>
      </div>

      {viewAsTable ? (
        <div className="overflow-x-auto max-h-64">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-border text-faint">
                <th className="py-2 px-3 font-semibold uppercase">Date</th>
                <th className="py-2 px-3 font-semibold uppercase text-right">Questions</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item, idx) => (
                <tr key={idx} className="border-b border-border/40 hover:bg-surface-2">
                  <td className="py-2 px-3 font-mono text-muted">{item.date}</td>
                  <td className="py-2 px-3 font-semibold text-text text-right tabular-nums">
                    {item.count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="relative pt-6 pb-2">
          {/* Y-Axis Gridlines */}
          <div className="absolute inset-0 flex flex-col justify-between pointer-events-none pb-8 text-[10px] text-faint font-mono">
            <div className="flex items-center gap-2">
              <span className="w-6 text-right">{maxVal}</span>
              <div className="h-[1px] flex-1 border-b border-dashed border-border" />
            </div>
            <div className="flex items-center gap-2">
              <span className="w-6 text-right">{Math.round(maxVal / 2)}</span>
              <div className="h-[1px] flex-1 border-b border-dashed border-border" />
            </div>
            <div className="flex items-center gap-2">
              <span className="w-6 text-right">0</span>
              <div className="h-[1px] flex-1 border-b border-border" />
            </div>
          </div>

          {/* Chart Bars */}
          <div className="ml-8 flex items-end justify-between h-44 pb-8 pt-4 gap-1 sm:gap-2">
            {data.map((item, idx) => {
              const heightPct = maxVal > 0 ? (item.count / maxVal) * 100 : 0;
              const isDimmed = hoveredIdx !== null && hoveredIdx !== idx;
              const isPeak = idx === peakIdx && item.count > 0;
              const shortDate = item.date.slice(5); // MM-DD

              return (
                <div
                  key={idx}
                  className="relative flex-1 flex flex-col items-center h-full justify-end group"
                  onMouseEnter={() => setHoveredIdx(idx)}
                  onMouseLeave={() => setHoveredIdx(null)}
                  onFocus={() => setHoveredIdx(idx)}
                  onBlur={() => setHoveredIdx(null)}
                  tabIndex={0}
                  aria-label={`${item.date}: ${item.count} questions`}
                >
                  {/* Peak Label */}
                  {isPeak && (
                    <span className="absolute -top-5 text-[11px] font-bold text-accent tabular-nums">
                      {item.count}
                    </span>
                  )}

                  {/* Tooltip Card */}
                  {hoveredIdx === idx && (
                    <div className="absolute -top-12 z-10 whitespace-nowrap rounded-lg border border-border-strong bg-surface px-2.5 py-1 text-center text-xs shadow-md animate-pop-in pointer-events-none">
                      <div className="font-semibold text-text">{item.date}</div>
                      <div className="text-[11px] text-muted">
                        {item.count} {item.count === 1 ? "question" : "questions"}
                      </div>
                    </div>
                  )}

                  {/* Bar */}
                  <div
                    style={{ height: `${Math.max(4, heightPct)}%` }}
                    className={`w-full max-w-[28px] rounded-t-md bg-chart transition-all duration-200 ${
                      isDimmed ? "opacity-40" : "opacity-100"
                    }`}
                  />

                  {/* Date Axis Label (Every other day) */}
                  <div className="absolute -bottom-6 text-[10px] text-faint">
                    {idx % 2 === 0 ? shortDate : ""}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

