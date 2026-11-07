import { Suspense } from "react";
import { AuthShell } from "@/components/AuthShell";
import { AuthForm } from "@/components/AuthForm";

export default function RegisterPage() {
  return (
    <AuthShell>
      <Suspense fallback={<div className="text-center text-muted">Loading…</div>}>
        <AuthForm mode="register" />
      </Suspense>
    </AuthShell>
  );
}

