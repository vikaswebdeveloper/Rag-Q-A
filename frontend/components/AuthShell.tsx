import React from "react";
import Image from "next/image";
import Link from "next/link";
import { Emblem } from "@/components/icons";
import { ThemeToggle } from "@/components/ThemeToggle";

export const inputClass = "field";
export const buttonClass = "btn btn-primary btn-lg w-full";
export const linkClass = "link";

export function StatusMark({
  tone = "accent",
  children,
}: {
  tone?: "accent" | "success" | "danger";
  children: React.ReactNode;
}) {
  const bg =
    tone === "success"
      ? "bg-success/10 text-success border-success/30"
      : tone === "danger"
      ? "bg-danger/10 text-danger border-danger/30"
      : "bg-accent-soft text-accent border-accent/30";

  return (
    <div
      className={`mx-auto flex h-14 w-14 items-center justify-center rounded-full border ${bg} shadow-sm`}
    >
      {children}
    </div>
  );
}

export function Notice({
  tone = "error",
  children,
}: {
  tone?: "error" | "success";
  children: React.ReactNode;
}) {
  const isErr = tone === "error";
  const styles = isErr
    ? "border-danger/40 bg-danger/[0.07] text-danger"
    : "border-success/40 bg-success/[0.08] text-success";

  return (
    <div
      role={isErr ? "alert" : "status"}
      className={`rounded-lg border border-l-4 p-3.5 text-sm leading-relaxed ${styles}`}
    >
      {children}
    </div>
  );
}

export function AuthShell({ children }: { children: React.ReactNode }) {
  return (
    <main className="relative flex flex-1 items-center justify-center px-4 py-4 sm:py-6 min-h-screen">
      {/* Theme Toggle Wrapper */}
      <div className="absolute top-4 right-4 z-10">
        <ThemeToggle />
      </div>

      {/* Main Card */}
      <div className="animate-rise grid w-full max-w-5xl overflow-hidden rounded-[22px] border border-border bg-surface shadow-lg md:grid-cols-[1.05fr_1fr]">
        {/* Left Art Panel */}
        <div className="auth-art relative isolate flex min-h-32 flex-col justify-between overflow-hidden bg-navy p-6 text-[#ece6da] md:min-h-[min(600px,calc(100dvh-3rem-2px))] md:p-10">
          {/* Background Photo with slow zoom */}
          <div className="absolute inset-0 -z-10 overflow-hidden">
            <Image
              src="/images/library-aisle.webp"
              alt="Grand library aisle"
              fill
              priority
              sizes="(max-width: 768px) 100vw, 50vw"
              className="object-cover animate-ken-burns"
            />
            {/* Gradient Overlay */}
            <div
              className="absolute inset-0"
              style={{
                background:
                  "linear-gradient(180deg, rgb(13 20 36 / 0.55) 0%, rgb(13 20 36 / 0.35) 40%, rgb(13 20 36 / 0.92) 100%)",
              }}
            />
          </div>

          {/* Inset Gold Hairline Frame */}
          <div className="absolute inset-3 rounded-[14px] border border-[#d9b46a]/25 pointer-events-none" />

          {/* Top Branding */}
          <Link href="/" className="relative z-[1] flex items-center gap-3">
            <Emblem size={40} />
            <div className="flex flex-col">
              <span className="font-display text-[1.6rem] font-semibold leading-none tracking-tight text-white">
                RAG <span className="italic text-[#e6c483]">Q&amp;A</span>
              </span>
              <span className="text-[0.62rem] font-semibold tracking-[0.28em] text-[#d9b46a]/70">
                THE DOCUMENT LIBRARY
              </span>
            </div>
          </Link>

          {/* Bottom Heading & Pitch (md and up) */}
          <div className="relative z-[1] hidden md:block mt-8">
            <h2 className="font-display text-[2.6rem] leading-[1.05] font-semibold text-white">
              Ask the library.{" "}
              <span className="italic block text-[#e6c483]">It answers, with sources.</span>
            </h2>
            <p className="mt-4 text-xs text-[#ece6da]/80 max-w-sm leading-relaxed">
              A reading room of documents on history, science, food, health and more — and a
              librarian who has read every page.
            </p>
          </div>
        </div>

        {/* Right Auth Pane */}
        <div className="auth-pane flex flex-col justify-center p-6 sm:p-12">
          {children}
        </div>
      </div>
    </main>
  );
}

