"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { BookIcon, SettingsIcon, LogoutIcon, Emblem } from "@/components/icons";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useUser } from "@/components/UserProvider";
import { api } from "@/lib/api";

export function Header() {
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();
  const router = useRouter();
  const { user } = useUser();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 8);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleLogout = async () => {
    try {
      await api("/auth/logout", { method: "POST" });
    } catch {}
    router.push("/login");
  };

  const isHome = pathname === "/";
  const isAdmin = pathname.startsWith("/admin");

  return (
    <header
      className={`sticky top-0 z-10 border-b bg-bg/85 backdrop-blur-md transition-all duration-200 ${
        scrolled
          ? "border-border shadow-[0_8px_24px_-18px_rgb(0_0_0/0.5)]"
          : "border-transparent"
      }`}
    >
      {/* 3px Top Gradient Strip */}
      <div
        className="h-[3px] w-full"
        style={{
          background: "linear-gradient(90deg, var(--navy), var(--accent) 50%, var(--gold))",
        }}
      />

      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        {/* Left: Logo & Wordmark */}
        <Link href="/" className="group flex items-center gap-3">
          <div className="transition-transform duration-500 ease-out group-hover:-rotate-8">
            <Emblem size={38} />
          </div>
          <div className="flex flex-col">
            <span className="font-display text-[1.6rem] font-semibold leading-none tracking-tight">
              RAG <span className="italic text-accent">Q&amp;A</span>
            </span>
            <span className="hidden text-[0.62rem] font-semibold tracking-[0.28em] text-faint sm:inline-block">
              THE DOCUMENT LIBRARY
            </span>
          </div>
        </Link>

        {/* Right: Navigation, ThemeToggle, User & Logout */}
        <div className="flex items-center gap-2 sm:gap-3">
          <nav className="flex items-center gap-1">
            <Link
              href="/"
              className={`hidden md:inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                isHome
                  ? "bg-surface-2 text-text"
                  : "text-muted hover:bg-surface-2 hover:text-text"
              }`}
            >
              <BookIcon size={16} />
              <span>Library</span>
            </Link>

            {user?.is_admin && (
              <Link
                href="/admin"
                className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                  isAdmin
                    ? "bg-surface-2 text-text"
                    : "text-muted hover:bg-surface-2 hover:text-text"
                }`}
              >
                <SettingsIcon size={16} />
                <span>Admin</span>
              </Link>
            )}
          </nav>

          {/* Divider */}
          <div className="h-6 w-[1px] bg-border-strong/60" />

          {/* Theme Toggle */}
          <ThemeToggle />

          {/* User Profile initial & Logout */}
          {user && (
            <div className="flex items-center gap-2 sm:gap-3">
              <div className="hidden items-center gap-2 lg:flex">
                <div className="flex h-8 w-8 items-center justify-center rounded-full border border-gold bg-navy font-display text-base font-semibold text-gold">
                  {user.name.charAt(0).toUpperCase()}
                </div>
                <span className="max-w-[130px] truncate text-xs font-medium text-text">
                  {user.name}
                </span>
              </div>

              <button
                type="button"
                onClick={handleLogout}
                aria-label="Log out"
                title="Log out"
                className="btn btn-ghost btn-sm"
              >
                <LogoutIcon size={16} />
                <span className="hidden sm:inline">Log out</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

