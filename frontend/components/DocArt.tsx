"use client";

import React, { useId } from "react";
import { categoryShades, seededRandom, titleFromSlug } from "@/lib/docArt";

export interface DocArtProps {
  slug: string;
  category: string;
  className?: string;
  portrait?: boolean;
}

export function DocArt({ slug, category, className = "", portrait = false }: DocArtProps) {
  const idPrefix = useId().replace(/:/g, "_");
  const rand = seededRandom(slug || "default-seed");

  const shades = categoryShades[category?.toLowerCase()] || categoryShades.general;
  const clothColor = shades[Math.floor(rand() * shades.length)];
  const gold = "#d9b46a";

  const W = portrait ? 180 : 240;
  const H = portrait ? 240 : 120;
  const medY = portrait ? 100 : 60;
  const medX = W / 2;

  const title = titleFromSlug(slug);
  const initial = title.charAt(0).toUpperCase() || "A";

  // Pick 1 of 5 patterns
  const patternIndex = Math.floor(rand() * 5);
  // Pick 1 of 3 layouts: 0 = full, 1 = side panels, 2 = top/bottom bands
  const layoutIndex = Math.floor(rand() * 3);

  const weaveId = `${idPrefix}-weave`;
  const ornId = `${idPrefix}-orn`;
  const vigId = `${idPrefix}-vig`;
  const goldGradId = `${idPrefix}-gold`;

  // Pattern definition
  let patternContent = null;
  let patW = 16;
  let patH = 16;

  if (patternIndex === 0) {
    // Diamond lattice
    patW = 16;
    patH = 16;
    patternContent = <path d="M8 0L16 8L8 16L0 8Z" fill="none" stroke={gold} strokeWidth="0.6" />;
  } else if (patternIndex === 1) {
    // Dots
    patW = 14;
    patH = 14;
    patternContent = <circle cx="7" cy="7" r="1.5" fill={gold} />;
  } else if (patternIndex === 2) {
    // Cross grid
    patW = 20;
    patH = 20;
    patternContent = <path d="M10 0v20M0 10h20" stroke={gold} strokeWidth="0.4" />;
  } else if (patternIndex === 3) {
    // Fan arcs
    patW = 24;
    patH = 24;
    patternContent = <path d="M0 24A24 24 0 0 1 24 0" fill="none" stroke={gold} strokeWidth="0.5" />;
  } else {
    // Four-point stars
    patW = 18;
    patH = 18;
    patternContent = <path d="M9 3Q9 9 3 9Q9 9 9 15Q9 9 15 9Q9 9 9 3Z" fill={gold} />;
  }

  // Wrap title for portrait
  const titleLines: string[] = [];
  if (portrait) {
    const words = title.split(" ");
    let currentLine = "";
    for (const w of words) {
      if ((currentLine + " " + w).trim().length <= 16) {
        currentLine = (currentLine + " " + w).trim();
      } else {
        if (currentLine) titleLines.push(currentLine);
        currentLine = w;
        if (titleLines.length >= 2) break;
      }
    }
    if (currentLine && titleLines.length < 3) {
      titleLines.push(currentLine);
    }
  }

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
      className={className}
    >
      <defs>
        {/* Linen Weave Pattern */}
        <pattern id={weaveId} width="3" height="3" patternUnits="userSpaceOnUse">
          <path d="M0 0h3M0 0v3" stroke="#ffffff" strokeWidth="0.35" opacity="0.18" />
        </pattern>

        {/* Gold Ornament Pattern */}
        <pattern id={ornId} width={patW} height={patH} patternUnits="userSpaceOnUse">
          {patternContent}
        </pattern>

        {/* Gold Linear Gradient */}
        <linearGradient id={goldGradId} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#f1d79b" />
          <stop offset="50%" stopColor="#d9b46a" />
          <stop offset="100%" stopColor="#a8823e" />
        </linearGradient>

        {/* Vignette Radial Gradient */}
        <radialGradient id={vigId} cx="50%" cy="50%" r="50%">
          <stop offset="55%" stopColor="#000000" stopOpacity="0" />
          <stop offset="100%" stopColor="#000000" stopOpacity="0.38" />
        </radialGradient>
      </defs>

      {/* Layer 1: Cloth Base */}
      <rect width={W} height={H} fill={clothColor} />

      {/* Layer 2: Linen Weave */}
      <rect width={W} height={H} fill={`url(#${weaveId})`} />

      {/* Layer 3: Gold Ornament Pattern based on layout */}
      {layoutIndex === 0 && (
        <rect width={W} height={H} fill={`url(#${ornId})`} opacity="0.22" />
      )}
      {layoutIndex === 1 && (
        <>
          <rect x="0" y="0" width={W * 0.26} height={H} fill={`url(#${ornId})`} opacity="0.3" />
          <rect x={W * 0.74} y="0" width={W * 0.26} height={H} fill={`url(#${ornId})`} opacity="0.3" />
        </>
      )}
      {layoutIndex === 2 && (
        <>
          <rect x="0" y="0" width={W} height={H * 0.22} fill={`url(#${ornId})`} opacity="0.32" />
          <rect x="0" y={H * 0.78} width={W} height={H * 0.22} fill={`url(#${ornId})`} opacity="0.32" />
        </>
      )}

      {/* Layer 4: Vignette */}
      <rect width={W} height={H} fill={`url(#${vigId})`} />

      {/* Layer 5: Double Gold Frame */}
      <rect x="9" y="9" width={W - 18} height={H - 18} fill="none" stroke={gold} strokeWidth="0.9" opacity="0.75" />
      <rect x="12.5" y="12.5" width={W - 25} height={H - 25} fill="none" stroke={gold} strokeWidth="0.5" opacity="0.55" />

      {/* Layer 6: Central Medallion */}
      <g transform={`translate(${medX}, ${medY})`}>
        <circle cx="0" cy="0" r="27" fill={clothColor} stroke={`url(#${goldGradId})`} strokeWidth="1.5" />
        <circle cx="0" cy="0" r="23.5" fill="none" stroke={gold} strokeWidth="0.45" />

        {/* First Letter in Cormorant Display Font */}
        <text
          x="0"
          y="11"
          textAnchor="middle"
          fontFamily="var(--font-cormorant), serif"
          fontSize="34"
          fontWeight="600"
          fontStyle="italic"
          fill={`url(#${goldGradId})`}
        >
          {initial}
        </text>

        {/* Landscape Ornaments */}
        {!portrait && (
          <>
            <path d="M-48 0h15M33 0h15" stroke={gold} strokeWidth="0.8" opacity="0.8" />
            <path d="M-53 0l3-3 3 3-3 3zM53 0l-3-3-3 3 3 3z" fill={gold} opacity="0.85" />
          </>
        )}
      </g>

      {/* Layer 7: Portrait Details */}
      {portrait && (
        <>
          {/* Gold Rule */}
          <line x1={medX - 30} y1="145" x2={medX + 30} y2="145" stroke={gold} strokeWidth="0.8" opacity="0.8" />

          {/* Title Lines */}
          <text
            x={medX}
            y="165"
            textAnchor="middle"
            fontFamily="var(--font-cormorant), serif"
            fontSize="15"
            fontWeight="600"
            fill={gold}
          >
            {titleLines.map((line, idx) => (
              <tspan key={idx} x={medX} dy={idx === 0 ? 0 : 17}>
                {line}
              </tspan>
            ))}
          </text>

          {/* Bottom Diamond */}
          <path d={`M${medX} 222l3-3 3 3-3 3z`} fill={gold} opacity="0.7" />
        </>
      )}
    </svg>
  );
}

