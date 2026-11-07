"use client";

import React, { useEffect, useState } from "react";
import { ArrowUpIcon } from "@/components/icons";

export function BackToTop() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setVisible(window.scrollY > 700);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <button
      type="button"
      onClick={scrollToTop}
      aria-label="Back to top"
      title="Back to top"
      className={`fixed right-[1.6rem] bottom-24 z-[14] flex h-10 w-10 items-center justify-center rounded-full border border-border bg-surface text-muted shadow-md transition-all duration-300 hover:-translate-y-0.5 hover:text-text hover:border-text focus-visible:outline-2 focus-visible:outline-accent ${
        visible
          ? "opacity-100 translate-y-0 pointer-events-auto"
          : "opacity-0 translate-y-3 pointer-events-none"
      }`}
    >
      <ArrowUpIcon size={18} />
    </button>
  );
}

