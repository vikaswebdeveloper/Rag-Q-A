"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useParams } from "next/navigation";
import {
  ArrowLeftIcon,
  CategoryIcon,
  ChatIcon,
  ClockIcon,
  DownloadIcon,
  ListIcon,
} from "@/components/icons";
import { DocArt } from "@/components/DocArt";
import { DataTable } from "@/components/DataTable";
import { openChat } from "@/components/ChatWidget";
import { Doc, api, sectionAnchor } from "@/lib/api";
import { categoryStyle, readingTime } from "@/lib/theme";

interface ParsedSection {
  level: number;
  heading: string;
  anchor: string;
  paragraphs: string[];
}

export default function DocumentReaderPage() {
  const params = useParams();
  const slug = params?.slug as string;

  const [doc, setDoc] = useState<Doc | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Reading progress state
  const [progress, setProgress] = useState(0);
  const [activeSectionAnchor, setActiveSectionAnchor] = useState<string>("");

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    api<Doc>(`/documents/${slug}`)
      .then((data) => {
        setDoc(data);
        document.title = `${data.title} · RAG Q&A`;
      })
      .catch((err) => {
        setError(err.message || "Failed to load document.");
      })
      .finally(() => setLoading(false));
  }, [slug]);

  // Handle URL hash on initial load
  useEffect(() => {
    if (!loading && doc && typeof window !== "undefined") {
      const hash = window.location.hash.slice(1);
      if (hash) {
        setTimeout(() => {
          const el = document.getElementById(hash);
          if (el) el.scrollIntoView({ behavior: "smooth" });
        }, 150);
      }
    }
  }, [loading, doc]);

  // Reading progress bar calculation
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;
      const scrollHeight = document.documentElement.scrollHeight;
      const innerHeight = window.innerHeight;
      const total = scrollHeight - innerHeight;
      if (total > 0) {
        setProgress(Math.min(1, Math.max(0, scrollY / total)));
      }
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Parse sections from doc text
  const { parsedSections, topLevelHeadings, wordCount } = useMemo(() => {
    if (!doc || !doc.text) {
      return { parsedSections: [], topLevelHeadings: [], wordCount: 0 };
    }

    const lines = doc.text.split("\n");
    let startIndex = 0;
    // Drop first line if it matches title
    if (lines.length > 0 && lines[0].trim().toLowerCase() === doc.title.toLowerCase()) {
      startIndex = 1;
    }

    const sections: ParsedSection[] = [];
    let currentLevel = 1;
    let currentHeading = "";
    let currentAnchor = "";
    let currentParagraphs: string[] = [];

    const flush = () => {
      if (currentHeading || currentParagraphs.length > 0) {
        sections.push({
          level: currentLevel,
          heading: currentHeading,
          anchor: currentAnchor,
          paragraphs: [...currentParagraphs],
        });
        currentParagraphs = [];
      }
    };

    let totalWords = 0;

    for (let i = startIndex; i < lines.length; i++) {
      const line = lines[i];
      const headingMatch = line.trim().match(/^(=+)\s*(.+?)\s*\1$/);

      if (headingMatch) {
        flush();
        currentLevel = headingMatch[1].length;
        currentHeading = headingMatch[2].trim();
        currentAnchor = sectionAnchor(currentHeading);
      } else {
        const trimmed = line.trim();
        if (trimmed) {
          currentParagraphs.push(trimmed);
          totalWords += trimmed.split(/\s+/).length;
        }
      }
    }
    flush();

    const topHeadings = sections.filter((s) => s.level <= 2 && s.heading);
    return { parsedSections: sections, topLevelHeadings: topHeadings, wordCount: totalWords };
  }, [doc]);

  // Active section tracking via IntersectionObserver
  useEffect(() => {
    if (topLevelHeadings.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveSectionAnchor(entry.target.id);
            break;
          }
        }
      },
      {
        rootMargin: "-90px 0px -65% 0px",
        threshold: 0,
      }
    );

    topLevelHeadings.forEach((h) => {
      const el = document.getElementById(h.anchor);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [topLevelHeadings]);

  if (loading) {
    return (
      <div className="space-y-8 animate-fade py-4">
        <div className="skeleton h-6 w-48" />
        <div className="skeleton h-64 w-full rounded-[22px]" />
        <div className="card p-10 space-y-4">
          <div className="skeleton h-8 w-1/3" />
          <div className="skeleton h-4 w-full" />
          <div className="skeleton h-4 w-5/6" />
          <div className="skeleton h-4 w-4/6" />
        </div>
      </div>
    );
  }

  if (error || !doc) {
    return (
      <div className="card p-12 text-center space-y-4 my-8">
        <div className="eyebrow !text-danger">ARCHIVE NOTICE</div>
        <h2 className="font-display text-3xl font-semibold text-text">This volume is missing</h2>
        <p className="text-sm text-muted max-w-md mx-auto">{error || "Document not found in the stacks."}</p>
        <div className="pt-2">
          <Link href="/" className="btn btn-primary btn-sm">
            ← Back to the library
          </Link>
        </div>
      </div>
    );
  }

  const theme = categoryStyle(doc.category);
  const readMin = readingTime(wordCount);
  const isSpreadsheet = Boolean(doc.tables && doc.tables.length > 0);

  return (
    <div className="space-y-8 pb-16">
      {/* Fixed Reading Progress Bar */}
      <div className="fixed inset-x-0 top-0 z-20 h-[3px] bg-transparent">
        <div
          className="h-full bg-accent origin-left transition-transform duration-150 ease-out"
          style={{ transform: `scaleX(${progress})` }}
        />
      </div>

      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs text-muted font-medium">
        <Link href="/" className="group inline-flex items-center gap-1.5 hover:text-accent">
          <span className="transition-transform group-hover:-translate-x-1">←</span>
          <span>Library</span>
        </Link>
        <span>/</span>
        <span className="capitalize">{doc.category}</span>
        <span className="hidden sm:inline">/</span>
        <span className="hidden sm:inline truncate max-w-sm text-text font-semibold">{doc.title}</span>
      </nav>

      {/* Title Banner */}
      <section className="relative isolate mt-5 overflow-hidden rounded-[22px] text-white shadow-lg">
        {/* Background photo & category gradient */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <Image
            src={theme.image}
            alt={doc.category}
            fill
            priority
            sizes="100vw"
            className="object-cover animate-ken-burns opacity-65"
          />
          <div
            className="absolute inset-0"
            style={{
              background: `linear-gradient(100deg, ${theme.color}f2 0%, ${theme.color}d9 45%, ${theme.color}66 100%)`,
            }}
          />
        </div>

        {/* Inset Hairline Frame */}
        <div className="absolute inset-3 sm:inset-4 rounded-[16px] border border-white/20 pointer-events-none" />

        {/* Banner Content Grid */}
        <div className="relative p-6 sm:p-10 lg:p-12 flex flex-col lg:flex-row lg:items-center justify-between gap-8">
          {/* Left Metadata & Actions */}
          <div className="animate-rise max-w-2xl space-y-4">
            {/* Eyebrow */}
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-white/30 bg-black/25 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-[#f1d79b]">
                <CategoryIcon category={doc.category} size={14} />
                <span>{doc.category}</span>
              </span>
              <span className="rounded border border-white/30 px-2 py-0.5 font-mono text-[11px] font-semibold uppercase tracking-wider text-white/90">
                {doc.format}
              </span>
            </div>

            {/* Document Title */}
            <h1 className="font-display text-[2.6rem] sm:text-5xl lg:text-6xl font-semibold leading-[1.02] text-white">
              {doc.title}
            </h1>

            {/* Meta Statistics Row */}
            <div className="flex items-center gap-3 text-xs text-white/80 font-medium">
              {!isSpreadsheet && (
                <div className="flex items-center gap-1">
                  <ClockIcon size={14} />
                  <span>{readMin} min read</span>
                </div>
              )}
              <span>•</span>
              <span>{isSpreadsheet ? `${doc.tables?.length} tables` : `${wordCount.toLocaleString()} words`}</span>
              <span>•</span>
              <span>{parsedSections.length} sections</span>
            </div>

            {/* Banner Buttons */}
            <div className="pt-2 flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={() => openChat(`What are the key points of “${doc.title}”?`)}
                className="btn btn-md bg-[#f1d79b] text-[#1b1407] font-semibold hover:bg-white shadow-md transition-transform hover:-translate-y-0.5"
              >
                <ChatIcon size={16} />
                <span>Ask about this document</span>
              </button>

              <a
                href={`/api/documents/${doc.slug}/file`}
                download
                className="btn btn-md border border-white/35 text-white hover:bg-white/10"
              >
                <DownloadIcon size={16} />
                <span>Download original (.{doc.format})</span>
              </a>
            </div>
          </div>

          {/* Right Portrait Clothbound Book (lg and up) */}
          <div className="hidden lg:flex justify-center flex-shrink-0">
            <div className="group relative w-56 transform rotate-2 rounded-md transition-all duration-500 ease-out hover:rotate-0 hover:scale-105 shadow-[0_24px_40px_-12px_rgb(0_0_0/0.6)] ring-1 ring-black/30">
              <DocArt slug={doc.slug} category={doc.category} portrait={true} className="w-full h-auto rounded-md" />
            </div>
          </div>
        </div>
      </section>

      {/* Main Document Body */}
      {isSpreadsheet ? (
        <div className="space-y-8 animate-fade">
          {doc.tables?.map((table, tIdx) => (
            <DataTable key={tIdx} table={table} category={doc.category} />
          ))}
        </div>
      ) : (
        <div className={`grid gap-8 ${topLevelHeadings.length > 1 ? "lg:grid-cols-[1fr_250px]" : "grid-cols-1"}`}>
          {/* Article Reading Area */}
          <article className="card prose-doc px-6 py-10 sm:px-14 sm:py-14 space-y-6">
            <div className="max-w-[68ch] mx-auto space-y-6">
              {parsedSections.map((sec, secIdx) => {
                const isFirstSec = secIdx === 0;

                return (
                  <div key={secIdx} className="space-y-4">
                    {/* Headings */}
                    {sec.heading && (
                      sec.level <= 2 ? (
                        <h2
                          id={sec.anchor}
                          className="font-display text-[2rem] font-semibold text-text border-b border-border pb-2 !mt-12 scroll-mt-24"
                        >
                          {sec.heading}
                        </h2>
                      ) : (
                        <h3
                          id={sec.anchor}
                          className="font-display italic text-[1.45rem] font-medium text-text !mt-8 scroll-mt-24"
                        >
                          {sec.heading}
                        </h3>
                      )
                    )}

                    {/* Paragraphs */}
                    {sec.paragraphs.map((pText, pIdx) => {
                      const isDropCap = isFirstSec && pIdx === 0 && !sec.heading;
                      return (
                        <p
                          key={pIdx}
                          className={`text-text leading-relaxed ${isDropCap ? "drop-cap" : ""}`}
                        >
                          {pText}
                        </p>
                      );
                    })}
                  </div>
                );
              })}

              {/* End of article ornament */}
              <div className="ornament my-12 text-center text-gold">
                <span>◆ ◆ ◆</span>
              </div>
            </div>
          </article>

          {/* Table of Contents (lg and up) */}
          {topLevelHeadings.length > 1 && (
            <aside className="hidden lg:block">
              <div className="sticky top-24 card p-5 space-y-3">
                <div className="eyebrow flex items-center gap-1.5 text-[0.68rem]">
                  <ListIcon size={14} />
                  <span>CONTENTS</span>
                </div>

                <nav className="border-l border-border space-y-1">
                  {topLevelHeadings.map((h, hIdx) => {
                    const isActive = activeSectionAnchor === h.anchor;
                    return (
                      <a
                        key={hIdx}
                        href={`#${h.anchor}`}
                        className={`block py-1.5 pl-3 text-xs transition-colors border-l-2 -ml-[2px] ${
                          isActive
                            ? "border-accent text-accent font-semibold"
                            : "border-transparent text-muted hover:text-text hover:border-border-strong"
                        }`}
                      >
                        {h.heading}
                      </a>
                    );
                  })}
                </nav>
              </div>
            </aside>
          )}
        </div>
      )}
    </div>
  );
}

