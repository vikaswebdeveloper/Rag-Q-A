"use client";

import React, { useLayoutEffect } from "react";
import { SunIcon, MoonIcon } from "@/components/icons";

export function ThemeToggle({ className = "" }: { className?: string }) {
  useLayoutEffect(() => {
    try {
      const stored = localStorage.getItem("theme");
      if (stored === "light" || stored === "dark") {
        document.documentElement.setAttribute("data-theme", stored);
      } else {
        const sysDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        document.documentElement.setAttribute("data-theme", sysDark ? "dark" : "light");
      }

      const mql = window.matchMedia("(prefers-color-scheme: dark)");
      const onChange = (e: MediaQueryListEvent) => {
        if (!localStorage.getItem("theme")) {
          document.documentElement.setAttribute("data-theme", e.matches ? "dark" : "light");
        }
      };
      mql.addEventListener("change", onChange);
      return () => mql.removeEventListener("change", onChange);
    } catch {}
  }, []);

  const toggle = () => {
    try {
      const current = document.documentElement.getAttribute("data-theme") || "light";
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("theme", next);

      document.documentElement.classList.add("theme-switching");
      setTimeout(() => {
        document.documentElement.classList.remove("theme-switching");
      }, 400);
    } catch {}
  };

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label="Toggle day and night mode"
      title="Toggle day and night mode"
      className={`relative inline-flex h-9 w-[68px] items-center justify-between rounded-full border border-border-strong bg-surface-2 p-1 transition-colors hover:border-text focus-visible:outline-2 focus-visible:outline-accent ${className}`}
    >
      {/* Sliding Knob */}
      <span
        aria-hidden="true"
        className="pointer-events-none absolute left-1 top-1 h-7 w-7 rounded-full bg-navy shadow-md transition-transform duration-300 ease-[cubic-bezier(.2,.7,.2,1)] dark:translate-x-[30px] dark:bg-accent"
      />

      {/* Sun Icon (Left) */}
      <span className="relative z-[1] flex h-7 w-7 items-center justify-center text-gold transition-transform duration-200 hover:rotate-45 dark:text-muted">
        <SunIcon size={15} />
      </span>

      {/* Moon Icon (Right) */}
      <span className="relative z-[1] flex h-7 w-7 items-center justify-center text-muted transition-transform duration-200 hover:-rotate-12 dark:text-on-accent">
        <MoonIcon size={14} />
      </span>
    </button>
  );
}

