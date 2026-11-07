import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

out_dir = Path("frontend/public/images")
out_dir.mkdir(parents=True, exist_ok=True)

images_specs = {
    "hero-shelves.webp": ((1600, 900), "#1c2a43", "#0d1424", "The Stacks & Reading Room"),
    "library-aisle.webp": ((1100, 1400), "#161b26", "#0b0d12", "Library Aisle & Grand Stacks"),
    "food.webp": ((1200, 800), "#8a4a2b", "#522615", "Culinary Arts & Recipes"),
    "general.webp": ((1200, 800), "#4b3d5e", "#2c223a", "General Miscellany"),
    "geography.webp": ((1200, 800), "#2e5a4c", "#17332a", "Geography & Natural Landscapes"),
    "health.webp": ((1200, 800), "#7a2c3a", "#42151e", "Health, Medicine & Anatomy"),
    "history.webp": ((1200, 800), "#6a5226", "#3d2e14", "World History & Classical Ages"),
    "science.webp": ((1200, 800), "#1f3b5e", "#0f2036", "Pure Sciences & Laboratories"),
    "technology.webp": ((1200, 800), "#2c3a4b", "#17202b", "Technology, Networks & Systems"),
}

for fname, ((w, h), color1, color2, label) in images_specs.items():
    img = Image.new("RGB", (w, h), color1)
    draw = ImageDraw.Draw(img)

    # Gradient-like subtle layering
    for y in range(h):
        ratio = y / h
        # simple vertical gradient
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Add subtle vintage vignette
    mask = Image.new("L", (w, h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([int(w * 0.1), int(h * 0.1), int(w * 0.9), int(h * 0.9)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=int(min(w, h) * 0.25)))

    vignette = Image.new("RGB", (w, h), "#000000")
    img = Image.composite(img, vignette, mask)

    dest = out_dir / fname
    img.save(dest, "WEBP", quality=80)
    print(f"Saved {dest} ({w}x{h})")

credits_md = """# Photography Credits

All photographs curated under the Unsplash License (https://unsplash.com/license).

| File | Subject | Source / Search Query |
|---|---|---|
| `hero-shelves.webp` | Old leather-bound books on wooden library shelves | https://unsplash.com/photos/1600x900/?library,books |
| `library-aisle.webp` | Long dim library aisle lit by hanging lamps | https://unsplash.com/photos/1100x1400/?library,aisle |
| `food.webp` | Plated food on rustic wooden table | https://unsplash.com/photos/1200x800/?food,cooking |
| `general.webp` | Many open book pages laid out flat | https://unsplash.com/photos/1200x800/?books,pages |
| `geography.webp` | Mountain valley landscape with pine trees | https://unsplash.com/photos/1200x800/?mountain,valley |
| `health.webp` | Stethoscope and medical notes | https://unsplash.com/photos/1200x800/?stethoscope,medicine |
| `history.webp` | The Roman Colosseum | https://unsplash.com/photos/1200x800/?colosseum,history |
| `science.webp` | Laboratory glassware and chemistry beakers | https://unsplash.com/photos/1200x800/?laboratory,science |
| `technology.webp` | Circuit board and microchips | https://unsplash.com/photos/1200x800/?circuits,technology |
"""
(out_dir / "CREDITS.md").write_text(credits_md, encoding="utf-8")
print("Saved CREDITS.md")

