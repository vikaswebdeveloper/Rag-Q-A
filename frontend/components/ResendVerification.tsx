"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";

export function ResendVerification({ email }: { email: string }) {
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [countdown, setCountdown] = useState(0);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (countdown > 0) {
      timer = setTimeout(() => setCountdown(countdown - 1), 1000);
    } else {
      setSent(false);
    }
    return () => clearTimeout(timer);
  }, [countdown]);

  const handleResend = async () => {
    if (countdown > 0 || loading) return;
    setLoading(true);
    try {
      await api("/auth/resend-verification", {
        method: "POST",
        json: { email },
      });
      setSent(true);
      setCountdown(60);
    } catch {
      // Endpoint is generic and doesn't reveal errors
      setSent(true);
      setCountdown(60);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleResend}
      disabled={loading || countdown > 0}
      className="btn btn-secondary btn-sm"
    >
      {loading
        ? "Sending…"
        : sent
        ? `Sent! Check your inbox (${countdown}s)`
        : "Resend verification link"}
    </button>
  );
}

