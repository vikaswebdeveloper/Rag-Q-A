export const categoryShades: Record<string, string[]> = {
  food: ["#8a4a2b", "#7a3f24", "#93573a"],
  general: ["#4b3d5e", "#3f3350", "#58496b"],
  geography: ["#2e5a4c", "#264d41", "#3a6757"],
  health: ["#7a2c3a", "#6a2432", "#863a47"],
  history: ["#6a5226", "#5c4620", "#775e30"],
  science: ["#1f3b5e", "#1a3252", "#2a4a70"],
  technology: ["#2c3a4b", "#243140", "#384858"],
};

export function titleFromSlug(slug: string): string {
  let cleanSlug = slug.replace(/-[a-z0-9]+$/, "");
  if (cleanSlug.includes("__")) {
    cleanSlug = cleanSlug.split("__")[1];
  }
  const spaced = cleanSlug.replace(/[-_]+/g, " ");
  return spaced.replace(/\b\w/g, (char) => char.toUpperCase());
}

export function seededRandom(seed: string): () => number {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i++) {
    h = Math.imul(h ^ seed.charCodeAt(i), 16777619);
  }
  return () => {
    h = Math.imul(h ^ (h >>> 15), h | 1);
    h ^= h + Math.imul(h ^ (h >>> 7), h | 61);
    return ((h ^ (h >>> 14)) >>> 0) / 4294967296;
  };
}

