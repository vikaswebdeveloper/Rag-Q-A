"use client";

import React, { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { AuthShell, Notice, StatusMark, buttonClass, inputClass, linkClass } from "@/components/AuthShell";
import { SettingsIcon } from "@/components/icons";
import { api } from "@/lib/api";

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token") || "";

  const [password, setPassword] = useState("");
  const [repeat, setRepeat] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const mismatch = repeat.length > 0 && password !== repeat;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (mismatch) return;
    setError(null);
    setLoading(true);

    try {
      await api("/auth/reset-password", {
        method: "POST",
        json: { token, password },
      });
      setSuccess(true);
      setTimeout(() => {
        window.location.assign("/");
      }, 1500);
    } catch (err: any) {
      setError(err.message || "Failed to reset password. The link may have expired.");
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="text-center space-y-4">
        <Notice tone="error">
          <p>No reset token was provided in the link.</p>
        </Notice>
        <p className="text-xs text-muted">
          <Link href="/forgot-password" className={linkClass}>
            Request a new link
          </Link>
        </p>
      </div>
    );
  }

  if (success) {
    return (
      <div className="text-center space-y-4 animate-fade">
        <StatusMark tone="success">
          <SettingsIcon size={24} />
        </StatusMark>
        <h1 className="font-display text-3xl font-semibold">Password changed</h1>
        <p className="text-sm text-muted">
          Your password has been updated and any other sessions were signed out. Redirecting to the library…
        </p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="space-y-1">
        <div className="eyebrow">NEW CREDENTIALS</div>
        <h1 className="font-display text-[2.6rem] font-semibold leading-tight text-text">
          Choose a new password
        </h1>
        <p className="text-sm text-muted">Enter and confirm your new password below.</p>
      </div>

      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        {error && (
          <Notice tone="error">
            <p>{error}</p>
            <div className="mt-2 text-xs">
              <Link href="/forgot-password" className="font-semibold underline">
                Request a new link
              </Link>
            </div>
          </Notice>
        )}

        <div className="space-y-1">
          <label htmlFor="new-pwd" className="text-xs font-semibold uppercase tracking-wider text-muted">
            New Password
          </label>
          <input
            id="new-pwd"
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••••••"
            className={inputClass}
          />
        </div>

        <div className="space-y-1">
          <label htmlFor="repeat-pwd" className="text-xs font-semibold uppercase tracking-wider text-muted">
            Confirm Password
          </label>
          <input
            id="repeat-pwd"
            type="password"
            required
            minLength={8}
            value={repeat}
            onChange={(e) => setRepeat(e.target.value)}
            placeholder="••••••••••••"
            className={inputClass}
          />
          {mismatch && (
            <p className="text-xs text-danger font-medium">The two passwords don&apos;t match.</p>
          )}
        </div>

        <button type="submit" disabled={loading || mismatch} className={buttonClass}>
          {loading ? "Updating password…" : "Update password"}
        </button>
      </form>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <AuthShell>
      <Suspense fallback={<div className="text-center text-muted">Loading…</div>}>
        <ResetPasswordForm />
      </Suspense>
    </AuthShell>
  );
}

