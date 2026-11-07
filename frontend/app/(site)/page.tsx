"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  CategoryIcon,
  ChatIcon,
  ClockIcon,
  SearchIcon,
  ArrowRightIcon,
} from "@/components/icons";
import { DocArt } from "@/components/DocArt";
import { openChat } from "@/components/ChatWidget";
import { DocSummary, api } from "@/lib/api";
import { categoryStyle, categoryThemes, docType, docTypeOrder, readingTime } from "@/lib/theme";

export default function HomePage() {
  const [docs, setDocs] = useState<DocSummary[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedFormat, setSelectedFormat] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"title" | "longest" | "shortest">("title");

  const searchInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    api<DocSummary[]>("/documents")
      .then((data) => setDocs(data))
      .catch((err) => console.error("Error loading documents:", err))
      .finally(() => setLoading(false));
  }, []);

  // Keyboard shortcut '/' to focus search, Esc to clear
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const activeTag = document.activeElement?.tagName.toLowerCase();
      if (activeTag === "input" || activeTag === "textarea") {
        if (e.key === "Escape" && document.activeElement === searchInputRef.current) {
          setSearchQuery("");
          searchInputRef.current?.blur();
        }
        return;
      }
      if (e.key === "/") {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Category counts
  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const d of docs) {
      counts[d.category] = (counts[d.category] || 0) + 1;
    }
    return counts;
  }, [docs]);

  // Overall Stats
  const totalWords = useMemo(() => {
    return docs.reduce((acc, d) => acc + (d.words || 0), 0);
  }, [docs]);

  // Filtered & Sorted Documents
  const filteredDocs = useMemo(() => {
    return docs.filter((d) => {
      if (selectedCategory !== "all" && d.category.toLowerCase() !== selectedCategory.toLowerCase()) {
        return false;
      }
      if (selectedFormat !== "all") {
        const typeInfo = docType(d.format);
        if (typeInfo.key !== selectedFormat) return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        const matchesTitle = d.title.toLowerCase().includes(q);
        const matchesPreview = d.preview.toLowerCase().includes(q);
        if (!matchesTitle && !matchesPreview) return false;
      }
      return true;
    });
  }, [docs, selectedCategory, selectedFormat, searchQuery]);

  const sortedDocs = useMemo(() => {
    const list = [...filteredDocs];
    if (sortBy === "title") {
      list.sort((a, b) => a.title.localeCompare(b.title));
    } else if (sortBy === "longest") {
      list.sort((a, b) => b.words - a.words);
    } else if (sortBy === "shortest") {
      list.sort((a, b) => a.words - b.words);
    }
    return list;
  }, [filteredDocs, sortBy]);

  // Format chip counts based on current category and search query
  const formatCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const d of docs) {
      if (selectedCategory !== "all" && d.category.toLowerCase() !== selectedCategory.toLowerCase()) {
        continue;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        if (!d.title.toLowerCase().includes(q) && !d.preview.toLowerCase().includes(q)) {
          continue;
        }
      }
      const typeKey = docType(d.format).key;
      counts[typeKey] = (counts[typeKey] || 0) + 1;
    }
    return counts;
  }, [docs, selectedCategory, searchQuery]);

  const hasActiveFilters =
    searchQuery.trim() !== "" || selectedCategory !== "all" || selectedFormat !== "all";

  const clearFilters = () => {
    setSearchQuery("");
    setSelectedCategory("all");
    setSelectedFormat("all");
    setSortBy("title");
  };

  const scrollToCollection = () => {
    document.getElementById("collection")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="space-y-16 sm:space-y-20">
      {/* 1. Hero */}
      <section className="relative isolate overflow-hidden rounded-[22px] bg-navy text-on-navy shadow-lg">
        {/* Background photo & overlays */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <Image
            src="/images/hero-shelves.webp"
            alt="Library shelves with antique volumes"
            fill
            priority
            sizes="100vw"
            className="object-cover animate-ken-burns opacity-60"
          />
          <div
            className="absolute inset-0"
            style={{
              background:
                "linear-gradient(100deg, rgb(13 20 36 / 0.96) 0%, rgb(13 20 36 / 0.86) 45%, rgb(13 20 36 / 0.35) 100%)",
            }}
          />
        </div>

        {/* Inset Gold Hairline Frame */}
        <div className="absolute inset-3 sm:inset-4 rounded-[16px] border border-[#d9b46a]/25 pointer-events-none" />

        {/* Content */}
        <div className="animate-rise px-6 py-12 sm:px-12 sm:py-16 lg:py-20 max-w-3xl">
          <div className="eyebrow !text-[#d9b46a]">THE READING ROOM</div>
          <h1 className="mt-3 font-display text-[2.6rem] sm:text-6xl lg:text-[4.2rem] leading-[1.02] font-semibold text-white">
            Every answer, <span className="italic text-[#e6c483]">properly sourced.</span>
          </h1>
          <p className="mt-4 text-sm sm:text-base leading-relaxed text-[#ece6da]/80 max-w-xl">
            Browse a curated collection of documents on history, science, food, health and more — or
            ask the librarian, who answers only from these pages and cites every source.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={() => openChat()}
              className="btn btn-lg bg-[#d9b46a] text-[#1b1407] font-semibold shadow-md transition-all duration-200 hover:bg-[#e6c483] hover:-translate-y-0.5"
            >
              <ChatIcon size={18} />
              <span>Ask the librarian</span>
            </button>
            <button
              type="button"
              onClick={scrollToCollection}
              className="btn btn-lg border border-[#ece6da]/35 text-white hover:bg-white/10"
            >
              <span>Browse the collection</span>
              <span>→</span>
            </button>
          </div>

          {/* Stats Row */}
          <div className="mt-12 pt-6 border-t border-[#d9b46a]/30">
            <dl className="grid grid-cols-3 gap-4">
              <div>
                <dt className="text-[0.68rem] font-semibold uppercase tracking-[0.22em] text-[#d9b46a]/80">
                  Documents
                </dt>
                <dd className="font-display text-2xl sm:text-3xl text-[#e6c483] tabular-nums font-semibold mt-0.5">
                  {loading ? "—" : docs.length}
                </dd>
              </div>
              <div>
                <dt className="text-[0.68rem] font-semibold uppercase tracking-[0.22em] text-[#d9b46a]/80">
                  Subjects
                </dt>
                <dd className="font-display text-2xl sm:text-3xl text-[#e6c483] tabular-nums font-semibold mt-0.5">
                  {loading ? "—" : Object.keys(categoryThemes).length}
                </dd>
              </div>
              <div>
                <dt className="text-[0.68rem] font-semibold uppercase tracking-[0.22em] text-[#d9b46a]/80">
                  Words indexed
                </dt>
                <dd className="font-display text-2xl sm:text-3xl text-[#e6c483] tabular-nums font-semibold mt-0.5">
                  {loading ? "—" : totalWords.toLocaleString()}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </section>

      {/* 2. Browse by Subject */}
      <section className="space-y-6">
        <div className="text-center space-y-1">
          <div className="eyebrow">BROWSE BY SUBJECT</div>
          <h2 className="font-display text-4xl sm:text-[2.75rem] font-semibold text-text">
            The Shelves
          </h2>
          <div className="ornament mx-auto max-w-[220px]">
            <span>◆</span>
          </div>
        </div>

        {/* Category Photo Tiles Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7 gap-4 max-sm:flex max-sm:overflow-x-auto max-sm:snap-x max-sm:pb-2">
          {Object.entries(categoryThemes).map(([catKey, theme], idx) => {
            const count = categoryCounts[catKey] || 0;
            const isSelected = selectedCategory.toLowerCase() === catKey;

            return (
              <div
                key={catKey}
                onClick={() => {
                  setSelectedCategory(isSelected ? "all" : catKey);
                  scrollToCollection();
                }}
                style={{ animationDelay: `${idx * 60}ms` }}
                className={`group relative isolate flex flex-col justify-between overflow-hidden rounded-[14px] p-4 text-white shadow-md cursor-pointer transition-all duration-300 hover:-translate-y-1 hover:shadow-lg h-52 max-sm:w-40 max-sm:flex-shrink-0 max-sm:snap-start ${
                  isSelected ? "ring-2 ring-accent ring-offset-2 ring-offset-bg" : ""
                }`}
              >
                {/* Background Image */}
                <Image
                  src={theme.image}
                  alt={theme.category}
                  fill
                  sizes="(max-width: 768px) 160px, (max-width: 1200px) 25vw, 14vw"
                  className="object-cover zoom-img -z-20"
                />

                {/* Overlays */}
                <div
                  className="absolute inset-0 -z-10 transition-opacity duration-300"
                  style={{
                    background: `linear-gradient(180deg, transparent 15%, ${theme.color} 92%)`,
                    opacity: isSelected ? 0.9 : 0.8,
                  }}
                />
                <div className="absolute inset-0 -z-10 bg-black/15" />

                {/* Top Glass Badge */}
                <div className="self-start flex h-8 w-8 items-center justify-center rounded-full border border-white/40 bg-black/20 backdrop-blur-sm text-white">
                  <CategoryIcon category={catKey} size={16} />
                </div>

                {/* Bottom Details */}
                <div>
                  <h3 className="font-display text-2xl font-semibold capitalize leading-none drop-shadow-sm">
                    {theme.category}
                  </h3>
                  <span className="text-xs text-white/80 font-medium mt-1 block">
                    {count} {count === 1 ? "volume" : "volumes"}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 3. The Collection */}
      <section id="collection" className="space-y-6 pt-4">
        <div className="text-center space-y-1">
          <div className="eyebrow">THE CATALOGUE</div>
          <h2 className="font-display text-4xl sm:text-[2.75rem] font-semibold text-text">
            The Collection
          </h2>
          <div className="ornament mx-auto max-w-[220px]">
            <span>◆</span>
          </div>
        </div>

        {/* Toolbar */}
        <div className="card p-4 sm:p-5 space-y-4">
          <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
            {/* Search Input */}
            <div className="relative flex-1">
              <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted">
                <SearchIcon size={18} />
              </span>
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search collection by title or topic…"
                className="field pl-10 pr-12 text-sm"
              />
              <span className="absolute right-3.5 top-1/2 -translate-y-1/2 hidden sm:inline-block pointer-events-none">
                <kbd className="rounded border border-border-strong bg-surface-2 px-1.5 py-0.5 text-[0.65rem] font-mono text-muted">
                  /
                </kbd>
              </span>
            </div>

            {/* Sort Dropdown */}
            <div className="flex items-center gap-2 flex-shrink-0">
              <label htmlFor="sort-select" className="text-xs font-semibold uppercase tracking-wider text-muted">
                Sort:
              </label>
              <select
                id="sort-select"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="field text-xs py-2 w-44"
              >
                <option value="title">Title (A–Z)</option>
                <option value="longest">Longest first</option>
                <option value="shortest">Shortest first</option>
              </select>
            </div>
          </div>

          {/* Category Filter Chips */}
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <button
              type="button"
              onClick={() => setSelectedCategory("all")}
              aria-pressed={selectedCategory === "all"}
              className="chip"
            >
              All subjects
            </button>
            {Object.keys(categoryThemes).map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => setSelectedCategory(cat)}
                aria-pressed={selectedCategory.toLowerCase() === cat.toLowerCase()}
                className="chip capitalize"
              >
                <CategoryIcon category={cat} size={14} />
                <span>{cat}</span>
              </button>
            ))}
          </div>

          <div className="h-[1px] w-full bg-border" />

          {/* Format Chips */}
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className="font-semibold uppercase tracking-wider text-faint pr-1">FORMAT</span>
            <button
              type="button"
              onClick={() => setSelectedFormat("all")}
              aria-pressed={selectedFormat === "all"}
              className="chip !text-xs !py-1"
            >
              All ({filteredDocs.length})
            </button>
            {docTypeOrder.map((dt) => {
              const count = formatCounts[dt.key] || 0;
              return (
                <button
                  key={dt.key}
                  type="button"
                  onClick={() => setSelectedFormat(dt.key)}
                  aria-pressed={selectedFormat === dt.key}
                  disabled={count === 0}
                  className="chip !text-xs !py-1"
                >
                  {dt.label} ({count})
                </button>
              );
            })}
          </div>

          {/* Status Bar */}
          <div className="flex items-center justify-between text-xs text-muted pt-1">
            <span aria-live="polite">
              Showing <strong>{sortedDocs.length}</strong> of {docs.length} documents
            </span>
            {hasActiveFilters && (
              <button
                type="button"
                onClick={clearFilters}
                className="link text-xs font-medium"
              >
                Clear filters
              </button>
            )}
          </div>
        </div>

        {/* 4. Document Grid */}
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
            {[1, 2, 3, 4, 5, 6].map((n) => (
              <div key={n} className="card flex flex-col overflow-hidden p-0">
                <div className="skeleton h-36 w-full" />
                <div className="p-5 space-y-3">
                  <div className="skeleton h-4 w-24" />
                  <div className="skeleton h-6 w-3/4" />
                  <div className="skeleton h-12 w-full" />
                  <div className="skeleton h-4 w-1/2 pt-2" />
                </div>
              </div>
            ))}
          </div>
        ) : sortedDocs.length === 0 ? (
          // Empty State
          <div className="card p-12 text-center space-y-4">
            <SearchIcon size={40} className="mx-auto text-gold" />
            <h3 className="font-display text-2xl font-semibold text-text">
              Nothing on the shelves matches that.
            </h3>
            <p className="text-sm text-muted max-w-md mx-auto">
              Try adjusting your search terms, clearing filters, or ask the librarian to look for
              information across all archives.
            </p>
            <div className="pt-2 flex justify-center gap-3">
              <button
                type="button"
                onClick={clearFilters}
                className="btn btn-secondary btn-sm"
              >
                Clear filters
              </button>
              <button
                type="button"
                onClick={() => openChat(searchQuery || undefined)}
                className="btn btn-primary btn-sm"
              >
                <ChatIcon size={14} />
                <span>Ask the librarian</span>
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
            {sortedDocs.map((doc, idx) => {
              const readMin = readingTime(doc.words);
              return (
                <Link
                  key={doc.slug}
                  href={`/documents/${doc.slug}`}
                  style={{ animationDelay: `${Math.min(idx, 11) * 40}ms` }}
                  className="card card-hover group animate-rise flex flex-col overflow-hidden text-left"
                >
                  {/* Top Book Cover Art */}
                  <div className="relative h-36 w-full overflow-hidden bg-surface-2 border-b border-border">
                    <DocArt
                      slug={doc.slug}
                      category={doc.category}
                      className="h-full w-full zoom-img"
                    />

                    {/* Non-txt Format Badge */}
                    {doc.format !== "txt" && (
                      <span className="absolute top-2.5 right-2.5 rounded border border-white/20 bg-black/35 px-2 py-0.5 font-mono text-[10px] font-semibold tracking-[0.12em] text-[#f1d79b] backdrop-blur-sm">
                        {doc.format.toUpperCase()}
                      </span>
                    )}
                  </div>

                  {/* Card Body */}
                  <div className="p-5 flex-1 flex flex-col justify-between">
                    <div>
                      {/* Eyebrow */}
                      <div className="eyebrow flex items-center gap-1.5 mb-2 !text-[0.68rem]">
                        <CategoryIcon category={doc.category} size={13} />
                        <span>{doc.category}</span>
                      </div>

                      {/* Title */}
                      <h3 className="font-display text-[1.6rem] font-semibold leading-[1.1] text-text transition-colors group-hover:text-accent">
                        {doc.title}
                      </h3>

                      {/* Preview Snippet */}
                      <p className="mt-2.5 text-sm text-muted line-clamp-3 leading-relaxed">
                        {doc.preview}
                      </p>
                    </div>

                    {/* Footer Row */}
                    <div className="mt-5 pt-3 border-t border-border/50 flex items-center justify-between text-xs text-faint">
                      <div className="flex items-center gap-1.5">
                        <ClockIcon size={13} />
                        <span>
                          {readMin} min read · {doc.words.toLocaleString()} words
                        </span>
                      </div>

                      <div className="flex items-center gap-1 text-accent font-semibold opacity-0 transition-all duration-200 group-hover:opacity-100 group-hover:translate-x-0.5">
                        <span>Read</span>
                        <ArrowRightIcon size={13} />
                      </div>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}

