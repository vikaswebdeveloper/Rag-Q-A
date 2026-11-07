import React from "react";
import { UserProvider } from "@/components/UserProvider";
import { Header } from "@/components/Header";
import { SiteFooter } from "@/components/SiteFooter";
import { BackToTop } from "@/components/BackToTop";
import { ChatWidget } from "@/components/ChatWidget";

export default function SiteLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <UserProvider>
      <Header />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6">
        {children}
      </main>
      <SiteFooter />
      <BackToTop />
      <ChatWidget />
    </UserProvider>
  );
}

