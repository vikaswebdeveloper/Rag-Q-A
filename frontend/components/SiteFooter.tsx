import React from "react";
import { Emblem } from "@/components/icons";

export function SiteFooter() {
  return (
    <footer className="mt-20 border-t border-border bg-surface-2/60 py-12 text-center">
      <div className="mx-auto flex max-w-4xl flex-col items-center px-4 sm:px-6">
        <Emblem size={34} className="mb-5" />

        <blockquote className="font-display text-xl sm:text-2xl italic text-text max-w-lg mb-2">
          “A library is not a luxury but one of the necessities of life.”
        </blockquote>
        <cite className="not-italic text-xs tracking-[0.2em] uppercase text-faint mb-6">
          HENRY WARD BEECHER
        </cite>

        <div className="ornament w-full max-w-xs mb-6">
          <span>◆</span>
        </div>

        <p className="text-xs text-muted max-w-md leading-relaxed">
          RAG Q&amp;A · Answers are generated from the library&apos;s documents — check the cited sources.{" "}
          <a
            href="https://unsplash.com"
            target="_blank"
            rel="noopener noreferrer"
            className="underline-grow text-text font-medium"
          >
            Photography from Unsplash.
          </a>
        </p>
      </div>
    </footer>
  );
}

