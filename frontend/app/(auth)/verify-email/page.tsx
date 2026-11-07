"use client";

import React, { Suspense, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { AuthShell, Notice, StatusMark, inputClass, linkClass } from "@/components/AuthShell";
import { ResendVerification } from "@/components/ResendVerification";
import { BookIcon } from "@/components/icons";
import { api } from "@/lib/api";

function VerifyEmailContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resendEmail, setResendEmail] = useState("");

  const calledRef = useRef(false);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      setError("No verification token was provided.");
      return;
    }

    if (calledRef.current) return;
    calledRef.current = true;

    api("/auth/verify-email", {
      method: "POST",
      json: { token },
    })
      .then(() => {
        setSuccess(true);
        setTimeout(() => {
          router.push("/");
        }, 1500);
      })
      .catch((err: any) => {
        setError(err.message || "This verification link is invalid or has expired.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token, router]);

  if (loading) {
    return (
      <div className="text-center space-y-4 animate-pulse">
        <StatusMark tone="accent">
          <BookIcon size={24} />
        </StatusMark>
        <h1 className="font-display text-3xl font-semibold">Verifying your email…</h1>
        <p className="text-sm text-muted">Confirming your reader credentials with the library.</p>
      </div>
    );
  }

  if (success) {
    return (
      <div className="text-center space-y-4 animate-fade">
        <StatusMark tone="success">
          <BookIcon size={24} />
        </StatusMark>
        <h1 className="font-display text-3xl font-semibold">Email verified</h1>
        <p className="text-sm text-muted">Your account is active. Redirecting to the reading room…</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-md mx-auto space-y-4 animate-fade text-center">
      <StatusMark tone="danger">
        <BookIcon size={24} />
      </StatusMark>
      <h1 className="font-display text-3xl font-semibold">Link not valid</h1>
      <Notice tone="error">
        <p>{error}</p>
      </Notice>

      <div className="pt-4 text-left space-y-3">
        <p className="text-xs text-muted text-center">
          Enter your email address to receive a fresh verification link:
        </p>
        <input
          type="email"
          value={resendEmail}
          onChange={(e) => setResendEmail(e.target.value)}
          placeholder="reader@library.org"
          className={inputClass}
        />
        <div className="flex justify-center pt-1">
          <ResendVerification email={resendEmail} />
        </div>
      </div>

      <div className="ornament my-6">
        <span>◆</span>
      </div>

      <p className="text-xs text-muted">
        <Link href="/login" className={linkClass}>
          ← Return to log in
        </Link>
      </p>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <AuthShell>
      <Suspense fallback={<div className="text-center text-muted">Loading…</div>}>
        <VerifyEmailContent />
      </Suspense>
    </AuthShell>
  );
}

