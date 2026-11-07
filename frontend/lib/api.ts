export interface User {
  id: string;
  name: string;
  email: string;
  is_admin: boolean;
}

export interface DocSummary {
  slug: string;
  title: string;
  category: string;
  format: string;
  preview: string;
  words: number;
}

export interface Table {
  name: string;
  columns: string[];
  rows: (string | number)[][];
  totalRows: number;
}

export interface Doc {
  slug: string;
  title: string;
  category: string;
  format: string;
  text: string;
  tables: Table[] | null;
}

export interface Source {
  slug: string;
  section: string;
  category: string;
  distance: number | null;
}

export interface Conversation {
  id: string;
  title: string;
  updated_at: string;
}

export type Rating = 1 | -1;

export type FeedbackReason =
  | "wrong"
  | "not_in_documents"
  | "incomplete"
  | "bad_sources"
  | "other";

export interface ChatMessage {
  id?: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  rating?: Rating;
  reason?: FeedbackReason;
}

export interface AdminStats {
  users: {
    total: number;
    verified: number;
    admins: number;
    new_7d: number;
  };
  questions: {
    total: number;
    today: number;
    last_7d: number;
    per_day: { date: string; count: number }[];
  };
  conversations: number;
  documents: {
    total: number;
    by_format: Record<string, number>;
    by_category: Record<string, number>;
  };
  chunks: number;
  feedback: {
    helpful: number;
    not_helpful: number;
    open: number;
  };
}

export interface AdminUser {
  id: string;
  name: string;
  email: string;
  is_admin: boolean;
  verified: boolean;
  joined: string;
  conversations: number;
  questions: number;
  last_active: string | null;
}

export interface AdminDoc extends DocSummary {
  file: string;
  size: number;
  modified: string | null;
  chunks: number;
  editable: boolean;
  index_state: string;
  index_detail: string;
}

export interface AdminFeedback {
  id: string;
  rating: number;
  reason: FeedbackReason | null;
  comment: string | null;
  question: string;
  answer: string;
  sources: Source[] | null;
  status: "open" | "resolved";
  admin_note: string | null;
  user: { name: string; email: string } | null;
  created_at: string;
  updated_at: string;
}

export const reasonLabels: Record<FeedbackReason, string> = {
  wrong: "Wrong answer",
  not_in_documents: "Said it's not in the documents",
  incomplete: "Incomplete",
  bad_sources: "Wrong sources",
  other: "Other",
};

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function api<T>(
  path: string,
  init?: RequestInit & { json?: unknown }
): Promise<T> {
  const headers = new Headers(init?.headers);
  let body = init?.body;

  if (init?.json !== undefined) {
    headers.set("Content-Type", "application/json");
    body = JSON.stringify(init.json);
  }

  const url = path.startsWith("/api") ? path : `/api${path}`;
  const res = await fetch(url, {
    ...init,
    headers,
    body,
  });

  if (res.status === 204) {
    return undefined as unknown as T;
  }

  if (res.status === 401 && !path.includes("/auth/login")) {
    try {
      await fetch("/api/auth/logout", { method: "POST" });
    } catch {}
    if (typeof window !== "undefined") {
      const next = encodeURIComponent(window.location.pathname + window.location.search);
      window.location.href = `/login?next=${next}`;
    }
  }

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const errorJson = await res.json();
      if (typeof errorJson.detail === "string") {
        detail = errorJson.detail;
      } else if (Array.isArray(errorJson.detail) && errorJson.detail.length > 0) {
        detail = errorJson.detail[0].msg || JSON.stringify(errorJson.detail[0]);
      } else if (errorJson.message) {
        detail = errorJson.message;
      }
    } catch {}
    throw new ApiError(res.status, detail);
  }

  return (await res.json()) as T;
}

export interface StreamChatHandlers {
  onMeta?: (data: { conversation_id: string; sources: Source[] }) => void;
  onToken?: (text: string) => void;
  onError?: (err: string) => void;
  onDone?: (data: { message_id?: string }) => void;
}

export async function streamChat(
  body: { message: string; conversation_id?: string },
  handlers: StreamChatHandlers,
  signal?: AbortSignal
): Promise<void> {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });

  if (!res.ok) {
    let errMessage = `Error ${res.status}`;
    try {
      const errorJson = await res.json();
      errMessage = errorJson.detail || errMessage;
    } catch {}
    handlers.onError?.(errMessage);
    return;
  }

  const reader = res.body?.getReader();
  if (!reader) {
    handlers.onError?.("No response stream available");
    return;
  }

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() || "";

    for (const evt of events) {
      if (!evt.trim()) continue;
      const lines = evt.split("\n");
      let eventType = "message";
      let eventData = "";

      for (const line of lines) {
        if (line.startsWith("event:")) {
          eventType = line.slice(6).trim();
        } else if (line.startsWith("data:")) {
          eventData = line.slice(5).trim();
        }
      }

      try {
        const parsed = eventData ? JSON.parse(eventData) : {};
        if (eventType === "meta") {
          handlers.onMeta?.(parsed);
        } else if (eventType === "token") {
          handlers.onToken?.(parsed.text ?? "");
        } else if (eventType === "error") {
          handlers.onError?.(parsed.message ?? "Unknown error");
        } else if (eventType === "done") {
          handlers.onDone?.(parsed);
        }
      } catch (err) {
        console.error("SSE parse error", err, evt);
      }
    }
  }
}

export function categoryLabel(category: string): string {
  if (!category) return "General";
  return category.charAt(0).toUpperCase() + category.slice(1).toLowerCase();
}

export function sectionAnchor(section: string): string {
  return section
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function sourceHref(source: Source): string {
  const parts = source.section ? source.section.split(" > ") : [];
  const lastPart = parts.length > 0 ? parts[parts.length - 1] : "";
  const anchor = sectionAnchor(lastPart);
  return anchor ? `/documents/${source.slug}#${anchor}` : `/documents/${source.slug}`;
}

export function sourceLabel(source: Source): string {
  const slug = source.slug;
  const raw = slug.includes("__") ? slug.split("__")[1] : slug;
  return raw.replace(/[-_]+/g, " ").trim();
}

