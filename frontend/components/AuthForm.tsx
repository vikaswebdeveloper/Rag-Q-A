"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowRightIcon, FileIcon } from "@/components/icons";
import { Notice, StatusMark, buttonClass, inputClass, linkClass } from "@/components/AuthShell";
import { ResendVerification } from "@/components/ResendVerification";
import { api } from "@/lib/api";

export interface AuthFormProps {
  mode: "login" | "register";
}

export function AuthForm({ mode }: AuthFormProps) {
  const searchParams = useSearchParams();
  const next = searchParams.get("next");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isUnverified, setIsUnverified] = useState(false);
  const [verificationSent, setVerificationSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsUnverified(false);
    setLoading(true);

    try {
      if (mode === "register") {
        const res = await api<{ verification_required: boolean }>("/auth/register", {
          method: "POST",
          json: { name, email, password },
        });

        if (res.verification_required) {
          setVerificationSent(true);
        } else {
          redirectAfterAuth();
        }
      } else {
        await api("/auth/login", {
          method: "POST",
          json: { email, password },
        });
        redirectAfterAuth();
      }
    } catch (err: any) {
      if (err.status === 403) {
        setIsUnverified(true);
        setError("Please verify your email first. Check your inbox for the link.");
      } else {
        setError(err.message || "An error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const redirectAfterAuth = () => {
    const safeNext = next && next.startsWith("/") && !next.startsWith("//") ? next : "/";
    // Hard navigation: avoids Next's client router cache (which may hold a stale
    // redirect-to-/login for "/") and guarantees the new cookie is used.
    window.location.assign(safeNext);
  };

  if (verificationSent) {
    return (
      <div className="text-center space-y-4 animate-fade">
        <StatusMark tone="accent">
          <FileIcon size={24} />
        </StatusMark>
        <div className="eyebrow">VERIFICATION REQUIRED</div>
        <h1 className="font-display text-3xl font-semibold">Check your inbox</h1>
        <p className="text-sm text-muted max-w-sm mx-auto">
          We sent a verification link to <strong className="text-text font-medium">{email}</strong>.
          The link expires in 24 hours.
        </p>
        <div className="pt-2 flex justify-center">
          <ResendVerification email={email} />
        </div>
        <div className="ornament pt-4">
          <span>◆</span>
        </div>
        <p className="text-xs text-muted">
          Already verified?{" "}
          <Link href="/login" className={linkClass}>
            Log in
          </Link>
        </p>
      </div>
    );
  }

  const isLogin = mode === "login";

  return (
    <div className="w-full max-w-md mx-auto">
      {/* Header */}
      <div className="space-y-1">
        <div className="eyebrow">{isLogin ? "MEMBERS’ ENTRANCE" : "NEW READER"}</div>
        <h1 className="font-display text-[2.6rem] font-semibold leading-tight text-text">
          {isLogin ? "Welcome back" : "Join the library"}
        </h1>
        <p className="text-sm text-muted">
          {isLogin
            ? "Log in to pick up where you left off."
            : "Create an account to start asking."}
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        {error && (
          <Notice tone="error">
            <p>{error}</p>
            {isUnverified && (
              <div className="mt-2">
                <ResendVerification email={email} />
              </div>
            )}
          </Notice>
        )}

        {!isLogin && (
          <div className="space-y-1">
            <label htmlFor="name" className="text-xs font-semibold uppercase tracking-wider text-muted">
              Name
            </label>
            <input
              id="name"
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Hypatia of Alexandria"
              className={inputClass}
            />
          </div>
        )}

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

        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <label htmlFor="password" className="text-xs font-semibold uppercase tracking-wider text-muted">
              Password
            </label>
            {isLogin && (
              <Link href="/forgot-password" className="text-xs link">
                Forgot password?
              </Link>
            )}
          </div>
          <input
            id="password"
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••••••"
            className={inputClass}
          />
          {!isLogin && <p className="text-xs text-faint">At least 8 characters.</p>}
        </div>

        <button type="submit" disabled={loading} className={buttonClass}>
          {loading ? (
            "One moment…"
          ) : (
            <>
              <span>{isLogin ? "Log in" : "Create account"}</span>
              <ArrowRightIcon size={16} />
            </>
          )}
        </button>
      </form>

      {/* Footer */}
      <div className="ornament my-6">
        <span>◆</span>
      </div>

      <p className="text-center text-xs text-muted">
        {isLogin ? (
          <>
            New here?{" "}
            <Link href="/register" className={linkClass}>
              Create an account
            </Link>
          </>
        ) : (
          <>
            Already have an account?{" "}
            <Link href="/login" className={linkClass}>
              Log in
            </Link>
          </>
        )}
      </p>
    </div>
  );
}

