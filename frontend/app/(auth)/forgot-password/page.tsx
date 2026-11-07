"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AuthShell, Notice, buttonClass, inputClass, linkClass } from "@/components/AuthShell";
import { api } from "@/lib/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [serverMsg, setServerMsg] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api<{ message: string }>("/auth/forgot-password", {
        method: "POST",
        json: { email },
      });
      setServerMsg(res.message);
      setSubmitted(true);
    } catch {
      setServerMsg("If an account exists for that email, we've sent it a link.");
      setSubmitted(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell>
      <div className="w-full max-w-md mx-auto">
        <div className="space-y-1">
          <div className="eyebrow">ACCOUNT RECOVERY</div>
          <h1 className="font-display text-[2.6rem] font-semibold leading-tight text-text">
            Forgot your password?
          </h1>
          <p className="text-sm text-muted">
            Enter your email address and we&apos;ll send you a link to reset it.
          </p>
        </div>

        {submitted ? (
          <div className="mt-6 space-y-4 animate-fade">
            <Notice tone="success">
              <p className="font-medium">{serverMsg}</p>
              <p className="mt-1 text-xs text-muted">The link expires in 1 hour.</p>
            </Notice>
            <p className="text-center text-xs text-muted pt-2">
              <Link href="/login" className={linkClass}>
                ← Return to log in
              </Link>
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div className="space-y-1">
              <label htmlFor="email" className="text-xs font-semibold uppercase tracking-wider text-muted">
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="reader@library.org"
                className={inputClass}
              />
            </div>

            <button type="submit" disabled={loading} className={buttonClass}>
              {loading ? "Sending link…" : "Send reset link"}
            </button>

            <div className="ornament my-6">
              <span>◆</span>
            </div>

            <p className="text-center text-xs text-muted">
              Remember your password?{" "}
              <Link href="/login" className={linkClass}>
                Log in
              </Link>
            </p>
          </form>
        )}
      </div>
    </AuthShell>
  );
}

