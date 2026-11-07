"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  ChatIcon,
  CloseIcon,
  SendIcon,
  PlusIcon,
  DownloadIcon,
  HistoryIcon,
  TrashIcon,
  ThumbUpIcon,
  ThumbDownIcon,
  FileIcon,
  Emblem,
} from "@/components/icons";
import {
  ChatMessage,
  Conversation,
  FeedbackReason,
  Rating,
  Source,
  api,
  reasonLabels,
  sourceHref,
  sourceLabel,
  streamChat,
} from "@/lib/api";
import { useUser } from "@/components/UserProvider";

export function openChat(question?: unknown) {
  if (typeof window !== "undefined") {
    const detail = typeof question === "string" ? question : undefined;
    window.dispatchEvent(new CustomEvent("open-chat", { detail }));
  }
}

export function ChatWidget() {
  const { user } = useUser();
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<"chat" | "history">("chat");

  // Hint Pill
  const [showHint, setShowHint] = useState(false);
  const [hasOpenedOnce, setHasOpenedOnce] = useState(false);

  // Chat State
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [followups, setFollowups] = useState<string[]>([]);
  const [feedbackOpenFor, setFeedbackOpenFor] = useState<string | null>(null);
  const [feedbackReason, setFeedbackReason] = useState<FeedbackReason | null>(null);
  const [feedbackComment, setFeedbackComment] = useState("");

  // History State
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const abortControllerRef = useRef<AbortController | null>(null);
  const messagesContainerRef = useRef<HTMLDivElement | null>(null);
  const followupReqIdRef = useRef(0);

  // Time-based greeting
  const getGreeting = () => {
    const hour = new Date().getHours();
    const firstName = user?.name ? user.name.split(" ")[0] : "Reader";
    if (hour < 12) return `Good morning, ${firstName}.`;
    if (hour < 18) return `Good afternoon, ${firstName}.`;
    return `Good evening, ${firstName}.`;
  };

  // Listen for open-chat event
  useEffect(() => {
    const handleOpenChat = (e: Event) => {
      const custom = e as CustomEvent<string | undefined>;
      setIsOpen(true);
      setActiveTab("chat");
      setHasOpenedOnce(true);
      if (custom.detail) {
        setInput(custom.detail);
      }
    };
    window.addEventListener("open-chat", handleOpenChat);
    return () => window.removeEventListener("open-chat", handleOpenChat);
  }, []);

  // Hint pill timer and scroll listener
  useEffect(() => {
    if (hasOpenedOnce) {
      setShowHint(false);
      return;
    }
    const timer = setTimeout(() => {
      if (!hasOpenedOnce) setShowHint(true);
    }, 600);

    const hideTimer = setTimeout(() => {
      setShowHint(false);
    }, 9600);

    const onScroll = () => {
      if (window.scrollY > 400) setShowHint(false);
    };
    window.addEventListener("scroll", onScroll, { passive: true });

    return () => {
      clearTimeout(timer);
      clearTimeout(hideTimer);
      window.removeEventListener("scroll", onScroll);
    };
  }, [hasOpenedOnce]);

  // Page scroll locking when chat is open
  useEffect(() => {
    if (isOpen) {
      document.documentElement.style.overflow = "hidden";
    } else {
      document.documentElement.style.overflow = "";
    }
    return () => {
      document.documentElement.style.overflow = "";
    };
  }, [isOpen]);

  // Close on Escape
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        setIsOpen(false);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [isOpen]);

  // Auto-scroll messages list ONLY
  useEffect(() => {
    if (messagesContainerRef.current && messages.length > 0) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  }, [messages, isStreaming]);

  // Load conversations when history tab opens
  const fetchConversations = async () => {
    setLoadingHistory(true);
    try {
      const data = await api<Conversation[]>("/conversations");
      setConversations(data);
    } catch {
      setConversations([]);
    } finally {
      setLoadingHistory(false);
    }
  };

  useEffect(() => {
    if (isOpen && activeTab === "history") {
      fetchConversations();
    }
  }, [isOpen, activeTab]);

  const loadConversation = async (convId: string) => {
    try {
      const msgs = await api<ChatMessage[]>(`/conversations/${convId}`);
      setConversationId(convId);
      setMessages(msgs);
      setActiveTab("chat");
      setFollowups([]);
      fetchFollowups(convId);
    } catch (err) {
      console.error("Failed to load conversation", err);
    }
  };

  const deleteConversation = async (convId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await api(`/conversations/${convId}`, { method: "DELETE" });
      setConversations((prev) => prev.filter((c) => c.id !== convId));
      if (conversationId === convId) {
        handleNewChat();
      }
    } catch (err) {
      console.error("Failed to delete conversation", err);
    }
  };

  const handleNewChat = () => {
    if (isStreaming && abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setConversationId(null);
    setMessages([]);
    setInput("");
    setFollowups([]);
    setIsStreaming(false);
    setActiveTab("chat");
  };

  const fetchFollowups = async (convId: string) => {
    const reqId = ++followupReqIdRef.current;
    try {
      const res = await api<string[]>(`/conversations/${convId}/followups`, { method: "POST" });
      if (reqId === followupReqIdRef.current) {
        setFollowups(res || []);
      }
    } catch {
      if (reqId === followupReqIdRef.current) {
        setFollowups([]);
      }
    }
  };

  const sendMessage = async (textToSend?: string) => {
    const query = (textToSend ?? input).trim();
    if (!query || isStreaming) return;

    setInput("");
    setFollowups([]);
    setFeedbackOpenFor(null);

    const userMsg: ChatMessage = { role: "user", content: query };
    const placeholderAssistant: ChatMessage = { role: "assistant", content: "" };

    setMessages((prev) => [...prev, userMsg, placeholderAssistant]);
    setIsStreaming(true);

    const controller = new AbortController();
    abortControllerRef.current = controller;

    let currentConvId = conversationId;

    await streamChat(
      {
        message: query,
        conversation_id: currentConvId || undefined,
      },
      {
        onMeta: (meta) => {
          if (meta.conversation_id) {
            currentConvId = meta.conversation_id;
            setConversationId(meta.conversation_id);
          }
          setMessages((prev) => {
            if (prev.length === 0) return prev;
            const lastIdx = prev.length - 1;
            const last = prev[lastIdx];
            if (last.role !== "assistant") return prev;
            const updated = [...prev];
            updated[lastIdx] = { ...last, sources: meta.sources };
            return updated;
          });
        },
        onToken: (tok) => {
          setMessages((prev) => {
            if (prev.length === 0) return prev;
            const lastIdx = prev.length - 1;
            const last = prev[lastIdx];
            if (last.role !== "assistant") return prev;
            const updated = [...prev];
            updated[lastIdx] = { ...last, content: last.content + tok };
            return updated;
          });
        },
        onError: (err) => {
          setMessages((prev) => {
            if (prev.length === 0) return prev;
            const lastIdx = prev.length - 1;
            const last = prev[lastIdx];
            if (last.role !== "assistant") return prev;
            const updated = [...prev];
            updated[lastIdx] = { ...last, content: err };
            return updated;
          });
        },
        onDone: (doneData) => {
          setMessages((prev) => {
            if (prev.length === 0) return prev;
            const lastIdx = prev.length - 1;
            const last = prev[lastIdx];
            if (last.role !== "assistant") return prev;
            const updated = [...prev];
            updated[lastIdx] = {
              ...last,
              id: doneData.message_id || last.id,
            };
            return updated;
          });

          if (currentConvId) {
            fetchFollowups(currentConvId);
          }
        },
      },
      controller.signal
    );

    setIsStreaming(false);
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsStreaming(false);
    }
  };

  const submitFeedback = async (messageId: string, rating: Rating, reason?: FeedbackReason, comment?: string) => {
    try {
      const res = await api<{ rating: Rating; reason: FeedbackReason }>(`/messages/${messageId}/feedback`, {
        method: "PUT",
        json: { rating, reason, comment },
      });
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, rating: res.rating, reason: res.reason } : m))
      );
      setFeedbackOpenFor(null);
    } catch (err) {
      console.error("Feedback error", err);
    }
  };

  const removeFeedback = async (messageId: string) => {
    try {
      await api(`/messages/${messageId}/feedback`, { method: "DELETE" });
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, rating: undefined, reason: undefined } : m))
      );
    } catch (err) {
      console.error("Delete feedback error", err);
    }
  };

  const handleExportPdf = () => {
    const originalTitle = document.title;
    document.title = `The Librarian - ${conversationId ? "Transcript" : "Conversation"}`;
    window.print();
    const afterPrint = () => {
      document.title = originalTitle;
      window.removeEventListener("afterprint", afterPrint);
    };
    window.addEventListener("afterprint", afterPrint);
  };

  return (
    <>
      {/* Launcher Button */}
      <button
        type="button"
        onClick={() => {
          setIsOpen(!isOpen);
          setHasOpenedOnce(true);
        }}
        aria-label={isOpen ? "Close librarian chat" : "Ask the librarian"}
        title={isOpen ? "Close librarian" : "Ask the librarian"}
        className={`fixed right-5 bottom-5 z-[31] flex h-[60px] w-[60px] items-center justify-center rounded-full bg-navy text-[#d9b46a] shadow-lg ring-1 ring-[#d9b46a]/40 transition-all duration-300 hover:-translate-y-1 hover:ring-[#d9b46a] dark:bg-accent dark:text-on-accent ${
          isOpen ? "max-sm:hidden" : ""
        }`}
      >
        <span className="absolute inset-1 rounded-full border border-[#d9b46a]/25 pointer-events-none" />
        {isOpen ? (
          <span className="transition-transform duration-300 hover:rotate-90">
            <CloseIcon size={24} />
          </span>
        ) : (
          <span className="transition-transform duration-200 hover:scale-110">
            <ChatIcon size={26} />
          </span>
        )}
      </button>

      {/* Hint Pill */}
      {showHint && !isOpen && (
        <div
          onClick={() => {
            setIsOpen(true);
            setHasOpenedOnce(true);
          }}
          className="fixed right-24 bottom-[1.85rem] z-[30] hidden sm:flex cursor-pointer items-center gap-1.5 rounded-full border border-border bg-surface px-4 py-2 text-xs font-medium text-text shadow-md animate-rise hover:border-accent"
        >
          <span className="font-serif italic">Ask the librarian</span>
          <span className="text-accent font-semibold">→</span>
        </div>
      )}

      {/* Backdrop */}
      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 z-[25] bg-black/30 backdrop-blur-[2px] animate-fade"
        />
      )}

      {/* Chat Panel */}
      {isOpen && (
        <div className="fixed inset-0 z-30 flex flex-col bg-surface shadow-lg overflow-hidden animate-slide-in-right sm:inset-auto sm:top-3 sm:bottom-3 sm:right-[5.75rem] sm:w-[480px] md:w-[520px] max-w-[calc(100vw-7rem)] sm:rounded-2xl sm:border sm:border-border">
          {/* Header */}
          <div className="relative bg-navy text-[#ece6da] p-4 flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <Emblem size={42} />
                <div>
                  <h3 className="font-display text-xl font-semibold leading-tight text-white">
                    The Librarian
                  </h3>
                  <div className="flex items-center gap-1.5 text-xs text-[#ece6da]/70">
                    <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                    <span>Answers from the library, with sources</span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-1.5">
                {messages.length > 0 && (
                  <button
                    type="button"
                    onClick={handleExportPdf}
                    title="Export as PDF"
                    className="btn btn-ghost btn-sm text-[#ece6da] border border-[#ece6da]/25 hover:bg-white/10"
                  >
                    <DownloadIcon size={14} />
                    <span className="text-xs">PDF</span>
                  </button>
                )}
                <button
                  type="button"
                  onClick={handleNewChat}
                  title="Start a new conversation"
                  className="btn btn-ghost btn-sm text-[#ece6da] border border-[#ece6da]/25 hover:bg-white/10"
                >
                  <PlusIcon size={14} />
                  <span className="text-xs">New</span>
                </button>
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="sm:hidden text-white/80 hover:text-white p-1"
                >
                  <CloseIcon size={20} />
                </button>
              </div>
            </div>

            {/* Tab Control */}
            <div className="flex rounded-lg bg-black/25 p-1 text-xs font-medium">
              <button
                type="button"
                onClick={() => setActiveTab("chat")}
                className={`flex-1 rounded-md py-1 text-center transition-colors ${
                  activeTab === "chat"
                    ? "bg-[#d9b46a] text-[#1b1407] font-semibold"
                    : "text-[#ece6da]/80 hover:text-white"
                }`}
              >
                Chat
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("history")}
                className={`flex-1 rounded-md py-1 text-center transition-colors ${
                  activeTab === "history"
                    ? "bg-[#d9b46a] text-[#1b1407] font-semibold"
                    : "text-[#ece6da]/80 hover:text-white"
                }`}
              >
                History
              </button>
            </div>

            {/* Bottom Hairline */}
            <div
              className="absolute inset-x-0 bottom-0 h-[1.5px]"
              style={{
                background: "linear-gradient(90deg, transparent, #d9b46a, transparent)",
              }}
            />
          </div>

          {/* Body Content */}
          {activeTab === "chat" ? (
            <>
              {/* Message List */}
              <div
                ref={messagesContainerRef}
                className="flex flex-1 flex-col gap-4 overflow-y-auto bg-bg/40 p-4"
              >
                {messages.length === 0 ? (
                  // Empty State
                  <div className="my-auto flex flex-col items-center text-center p-2">
                    <Emblem size={56} className="mb-3" />
                    <h2 className="font-display text-[1.6rem] font-semibold text-text">
                      {getGreeting()}
                    </h2>
                    <p className="mt-1 text-xs text-muted max-w-xs">
                      I&apos;ve read every document in the library. What would you like to know?
                    </p>

                    <div className="ornament my-4 w-full max-w-[200px] max-h-[680px]:hidden">
                      <span>◆</span>
                    </div>

                    {/* Suggestions */}
                    <div className="mt-2 w-full space-y-2">
                      {[
                        "When was Kubernetes first released?",
                        "What causes earthquakes?",
                        "Who were the Vikings?",
                        "Is caffeine bad for you?",
                      ].map((q, idx) => (
                        <button
                          key={idx}
                          type="button"
                          onClick={() => sendMessage(q)}
                          className="group flex w-full items-center justify-between rounded-xl border border-border bg-surface px-3.5 py-2.5 text-left font-serif text-sm italic text-text shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-accent hover:shadow-md"
                        >
                          <span className="truncate pr-2">{q}</span>
                          <SendIcon
                            size={14}
                            className="text-muted transition-colors group-hover:text-accent flex-shrink-0"
                          />
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  // Message Stream
                  messages.map((m, idx) => {
                    const isUser = m.role === "user";
                    return (
                      <div
                        key={idx}
                        className={`flex flex-col gap-1.5 ${isUser ? "items-end" : "items-start"}`}
                      >
                        {isUser ? (
                          <div className="max-w-[85%] rounded-2xl rounded-br-md bg-navy px-4 py-2.5 text-sm text-on-navy dark:bg-accent dark:text-on-accent shadow-sm">
                            <p className="whitespace-pre-wrap">{m.content}</p>
                          </div>
                        ) : (
                          <div className="flex items-start gap-2 max-w-[92%]">
                            <div className="mt-1 flex-shrink-0">
                              <Emblem size={28} />
                            </div>

                            <div className="flex-1 rounded-2xl rounded-tl-md border border-border bg-surface p-4 text-sm text-text shadow-sm">
                              {/* Content / Thinking */}
                              {m.content ? (
                                <div className="md prose-doc !text-sm leading-6">
                                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                                </div>
                              ) : isStreaming && idx === messages.length - 1 ? (
                                <div className="flex items-center gap-2 text-xs italic text-muted">
                                  <span className="flex gap-1">
                                    <span className="h-1.5 w-1.5 rounded-full bg-accent dot" />
                                    <span className="h-1.5 w-1.5 rounded-full bg-accent dot" />
                                    <span className="h-1.5 w-1.5 rounded-full bg-accent dot" />
                                  </span>
                                  <span>Consulting the shelves…</span>
                                </div>
                              ) : null}

                              {/* Sources */}
                              {m.sources && m.sources.length > 0 && (
                                <div className="mt-3.5 pt-3 border-t border-border/60">
                                  <div className="eyebrow mb-1.5 text-[0.65rem]">SOURCES</div>
                                  <div className="flex flex-wrap gap-1.5">
                                    {m.sources.slice(0, 4).map((src, sIdx) => (
                                      <Link
                                        key={sIdx}
                                        href={sourceHref(src)}
                                        title={src.section}
                                        className="inline-flex items-center gap-1 rounded-md border border-border bg-surface-2 px-2 py-1 text-xs text-muted transition-colors hover:border-accent hover:text-accent"
                                      >
                                        <FileIcon size={12} />
                                        <span className="capitalize">{sourceLabel(src)}</span>
                                      </Link>
                                    ))}
                                  </div>
                                </div>
                              )}

                              {/* Feedback Actions */}
                              {m.id && !isStreaming && (
                                <div className="mt-3 pt-2 flex items-center justify-between border-t border-border/40 text-xs text-muted">
                                  <div className="flex items-center gap-1">
                                    <button
                                      type="button"
                                      onClick={() => {
                                        if (m.rating === 1) removeFeedback(m.id!);
                                        else submitFeedback(m.id!, 1);
                                      }}
                                      aria-pressed={m.rating === 1}
                                      className={`flex h-7 w-7 items-center justify-center rounded-full border transition-colors ${
                                        m.rating === 1
                                          ? "border-success bg-success/15 text-success"
                                          : "border-border-strong hover:border-text text-muted"
                                      }`}
                                    >
                                      <ThumbUpIcon size={13} />
                                    </button>

                                    <button
                                      type="button"
                                      onClick={() => {
                                        if (m.rating === -1) removeFeedback(m.id!);
                                        else setFeedbackOpenFor(feedbackOpenFor === m.id ? null : m.id!);
                                      }}
                                      aria-pressed={m.rating === -1}
                                      className={`flex h-7 w-7 items-center justify-center rounded-full border transition-colors ${
                                        m.rating === -1
                                          ? "border-danger bg-danger/15 text-danger"
                                          : "border-border-strong hover:border-text text-muted"
                                      }`}
                                    >
                                      <ThumbDownIcon size={13} />
                                    </button>
                                  </div>

                                  {m.rating ? (
                                    <span className="text-[0.7rem] text-faint">
                                      Thanks! Shared with admins {m.reason ? `· ${reasonLabels[m.reason]}` : ""}
                                    </span>
                                  ) : null}
                                </div>
                              )}

                              {/* Negative Feedback Sub-Panel */}
                              {feedbackOpenFor === m.id && (
                                <div className="mt-3 rounded-lg border border-border bg-surface-2 p-3 text-xs space-y-2 animate-fade">
                                  <p className="font-semibold text-text">What was wrong?</p>
                                  <div className="flex flex-wrap gap-1">
                                    {(
                                      [
                                        "wrong",
                                        "not_in_documents",
                                        "incomplete",
                                        "bad_sources",
                                        "other",
                                      ] as FeedbackReason[]
                                    ).map((rKey) => (
                                      <button
                                        key={rKey}
                                        type="button"
                                        onClick={() => setFeedbackReason(rKey)}
                                        aria-pressed={feedbackReason === rKey}
                                        className="chip text-[0.7rem] py-1 px-2"
                                      >
                                        {reasonLabels[rKey]}
                                      </button>
                                    ))}
                                  </div>

                                  <textarea
                                    value={feedbackComment}
                                    onChange={(e) => setFeedbackComment(e.target.value)}
                                    placeholder="What should the answer have said? (optional)"
                                    maxLength={1000}
                                    rows={2}
                                    className="field text-xs py-1.5"
                                  />

                                  <p className="text-[0.68rem] text-faint leading-tight">
                                    This question and answer will be shared with the library admins so they can fix the documents.
                                  </p>

                                  <div className="flex justify-end gap-2 pt-1">
                                    <button
                                      type="button"
                                      onClick={() => submitFeedback(m.id!, -1)}
                                      className="btn btn-ghost btn-sm"
                                    >
                                      Skip
                                    </button>
                                    <button
                                      type="button"
                                      onClick={() =>
                                        submitFeedback(m.id!, -1, feedbackReason || undefined, feedbackComment || undefined)
                                      }
                                      className="btn btn-primary btn-sm"
                                    >
                                      Send
                                    </button>
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })
                )}

                {/* Follow-up Question Suggestions */}
                {followups.length > 0 && !isStreaming && (
                  <div className="mt-2 space-y-1.5 pt-2 border-t border-border/40 animate-fade">
                    <span className="eyebrow text-[0.65rem]">YOU COULD ALSO ASK</span>
                    <div className="space-y-1">
                      {followups.map((fq, fIdx) => (
                        <button
                          key={fIdx}
                          type="button"
                          onClick={() => sendMessage(fq)}
                          className="w-full text-left rounded-lg border border-border-strong/60 bg-surface px-3 py-1.5 font-serif italic text-xs text-text transition-all hover:border-accent hover:text-accent shadow-sm"
                        >
                          {fq}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Input Bar */}
              <div className="border-t border-border bg-surface p-3">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    sendMessage();
                  }}
                  className="flex items-center gap-2"
                >
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask the library anything…"
                    maxLength={2000}
                    disabled={isStreaming}
                    className="field text-sm py-2"
                  />

                  {isStreaming ? (
                    <button
                      type="button"
                      onClick={handleStop}
                      className="btn btn-secondary btn-sm px-3"
                    >
                      Stop
                    </button>
                  ) : (
                    <button
                      type="submit"
                      disabled={!input.trim()}
                      className="btn btn-primary btn-sm px-3 flex-shrink-0"
                    >
                      <SendIcon size={16} />
                    </button>
                  )}
                </form>
              </div>
            </>
          ) : (
            // History Tab
            <div className="flex flex-1 flex-col overflow-y-auto bg-bg/40 p-4">
              {loadingHistory ? (
                <div className="my-auto text-center text-xs text-muted">
                  Loading conversations…
                </div>
              ) : conversations.length === 0 ? (
                <div className="my-auto text-center space-y-2">
                  <HistoryIcon size={32} className="mx-auto text-gold" />
                  <p className="font-display text-lg font-semibold text-text">No conversations yet</p>
                  <p className="text-xs text-muted">Ask me something to begin!</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {conversations.map((c) => (
                    <div
                      key={c.id}
                      onClick={() => loadConversation(c.id)}
                      className={`group flex items-center justify-between rounded-xl border p-3 cursor-pointer shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md ${
                        conversationId === c.id
                          ? "border-accent bg-surface"
                          : "border-border bg-surface hover:border-border-strong"
                      }`}
                    >
                      <div className="flex-1 pr-2">
                        <h4 className="text-xs font-semibold text-text group-hover:text-accent line-clamp-1">
                          {c.title}
                        </h4>
                        <span className="text-[0.68rem] text-faint">
                          {new Date(c.updated_at).toLocaleDateString(undefined, {
                            month: "short",
                            day: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </span>
                      </div>

                      <button
                        type="button"
                        onClick={(e) => deleteConversation(c.id, e)}
                        title="Delete conversation"
                        className="opacity-0 group-hover:opacity-100 text-muted hover:text-danger p-1 transition-opacity"
                      >
                        <TrashIcon size={14} />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* PDF Export Print Transcript (Portal-style print section) */}
      <div className="print-transcript">
        <h1>The Librarian</h1>
        <div className="print-meta">
          Transcript exported on {new Date().toLocaleDateString()}
        </div>
        {messages.map((m, idx) => (
          <div key={idx} className={`print-msg ${m.role === "user" ? "print-user" : ""}`}>
            <div className="print-role">{m.role === "user" ? "You" : "The Librarian"}</div>
            <div className="md">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
            </div>
            {m.sources && m.sources.length > 0 && (
              <ul className="print-sources">
                {m.sources.map((src, sIdx) => (
                  <li key={sIdx}>
                    {src.section} ({src.slug})
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </>
  );
}

