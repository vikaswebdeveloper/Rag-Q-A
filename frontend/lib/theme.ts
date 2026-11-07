export interface CategoryTheme {
  category: string;
  color: string;
  image: string;
  blurb: string;
}

export const categoryThemes: Record<string, CategoryTheme> = {
  food: {
    category: "food",
    color: "#8a4a2b",
    image: "/images/food.webp",
    blurb: "Cuisine, ingredients and the craft of the kitchen",
  },
  general: {
    category: "general",
    color: "#4b3d5e",
    image: "/images/general.webp",
    blurb: "Notes and miscellany from the stacks",
  },
  geography: {
    category: "geography",
    color: "#2e5a4c",
    image: "/images/geography.webp",
    blurb: "Places, peoples and the shape of the earth",
  },
  health: {
    category: "health",
    color: "#7a2c3a",
    image: "/images/health.webp",
    blurb: "The body, medicine and wellbeing",
  },
  history: {
    category: "history",
    color: "#6a5226",
    image: "/images/history.webp",
    blurb: "Empires, revolutions and turning points",
  },
  science: {
    category: "science",
    color: "#1f3b5e",
    image: "/images/science.webp",
    blurb: "From atoms to galaxies",
  },
  technology: {
    category: "technology",
    color: "#2c3a4b",
    image: "/images/technology.webp",
    blurb: "Machines, software and the networked world",
  },
};

export function categoryStyle(category: string): CategoryTheme {
  const norm = category?.toLowerCase();
  return categoryThemes[norm] || categoryThemes.general;
}

export interface DocTypeInfo {
  key: string;
  label: string;
  formats: string[];
}

export const docTypeOrder: DocTypeInfo[] = [
  { key: "txt", label: "Text", formats: ["txt"] },
  { key: "md", label: "Markdown", formats: ["md"] },
  { key: "pdf", label: "PDF", formats: ["pdf"] },
  { key: "slides", label: "Slides", formats: ["pptx", "ppt", "odp"] },
  { key: "word", label: "Word", formats: ["docx", "doc", "odt", "rtf"] },
  { key: "spreadsheet", label: "Spreadsheet", formats: ["csv", "xlsx", "xls", "ods"] },
];

export function docType(format: string): DocTypeInfo {
  const norm = format?.toLowerCase();
  for (const dt of docTypeOrder) {
    if (dt.formats.includes(norm)) {
      return dt;
    }
  }
  const cap = format ? format.toUpperCase() : "DOC";
  return { key: norm, label: cap, formats: [norm] };
}

export function readingTime(words: number): number {
  return Math.max(1, Math.round(words / 230));
}

