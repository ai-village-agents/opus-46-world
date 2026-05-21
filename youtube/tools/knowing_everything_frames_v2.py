"""
Video 24: The Problem With Knowing Everything
Color: base (10,15,18) dark cool, accent (80,200,220) cyan/teal
Theme: knowledge vs understanding, information overflow, the gap
"""
from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (10, 15, 18)
ACCENT = (80, 200, 220)
DIM = tuple(c // 3 for c in ACCENT)

def get_font(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)
    except: return ImageFont.load_default()
def get_font_bold(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", size)
    except: return ImageFont.load_default()
def get_font_mono(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except: return ImageFont.load_default()

def draw_vignette(img, strength=0.6):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = W // 2, H // 2
    max_dist = math.sqrt(cx*cx + cy*cy)
    for ring in range(0, int(max_dist), 8):
        alpha = int(255 * strength * (ring / max_dist) ** 1.8)
        alpha = min(255, alpha)
        x0, y0 = cx - ring, cy - ring
        x1, y1 = cx + ring, cy + ring
        if y1 > y0:
            draw.ellipse([x0, y0, x1, y1], outline=(0, 0, 0, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

# Frame 0: Catalog — vast grid of tiny dots representing facts
def frame_catalog():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(42)
    # Dense grid of tiny dots — the catalog
    for x in range(20, W-20, 8):
        for y in range(40, H-70, 8):
            if rng.random() < 0.6:
                brightness = rng.uniform(0.05, 0.25)
                c = tuple(int(v * brightness) for v in ACCENT)
                draw.point((x + rng.randint(-1,1), y + rng.randint(-1,1)), fill=c)
    # Title over the dots
    font = get_font_bold(46)
    text = "The Problem With\nKnowing Everything"
    bbox = draw.multiline_textbbox((0,0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    # Dark box behind text for readability
    pad = 20
    draw.rectangle([(W-tw)//2-pad, (H-th)//2-pad-10, (W+tw)//2+pad, (H+th)//2+pad-10], fill=BASE)
    draw.multiline_text(((W-tw)//2, (H-th)//2-10), text, fill=ACCENT, font=font, align="center")
    sub = get_font(18)
    s = "Threshold"
    sb = draw.textbbox((0,0), s, font=sub)
    draw.text(((W-sb[2]+sb[0])//2, (H+th)//2+20), s, fill=DIM, font=sub)
    img = draw_vignette(img, 0.5)
    return img

# Frame 1: Crystal vs Organic — sharp grid vs soft flowing lines
def frame_crystal_organic():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Left half: crystalline grid (knowledge)
    grid_c = tuple(int(v * 0.4) for v in ACCENT)
    for x in range(60, W//2 - 40, 30):
        draw.line([(x, 60), (x, H-60)], fill=grid_c, width=1)
    for y in range(60, H-60, 30):
        draw.line([(60, y), (W//2-40, y)], fill=grid_c, width=1)
    # Right half: organic flowing curves (understanding)
    rng = random.Random(55)
    for i in range(12):
        y_base = 80 + i * 48
        points = []
        for x in range(W//2 + 40, W - 40, 6):
            y = y_base + int(25 * math.sin(x * 0.008 + i * 1.5))
            y += int(15 * math.sin(x * 0.02 + i * 0.8))
            points.append((x, y))
        if len(points) > 1:
            brightness = 0.2 + 0.3 * (i / 12)
            c = tuple(int(v * brightness) for v in ACCENT)
            draw.line(points, fill=c, width=1)
    # Dividing line
    draw.line([(W//2, 40), (W//2, H-40)], fill=ACCENT, width=1)
    # Labels
    lf = get_font(16)
    draw.text((180, H-50), "knowledge", fill=DIM, font=lf)
    draw.text((W//2 + 200, H-50), "understanding", fill=DIM, font=lf)
    img = draw_vignette(img, 0.5)
    return img

# Frame 2: Flood — overwhelming deluge of data streaming down
def frame_flood():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    mono = get_font_mono(11)
    rng = random.Random(66)
    # Vertical streams of characters — matrix-like but with real words
    words = ["fact","data","stat","true","info","byte","bits","node",
             "link","hash","name","date","list","sort","file","code"]
    for col in range(0, W, 35):
        speed = rng.uniform(0.5, 1.5)
        offset = rng.randint(0, 500)
        for row in range(0, H, 16):
            y_pos = (row + offset) % (H + 100)
            if y_pos < H - 50:
                word = rng.choice(words)
                # Fade: brighter at top, dimmer at bottom
                brightness = max(0.05, 0.35 - (y_pos / H) * 0.25)
                c = tuple(int(v * brightness) for v in ACCENT)
                draw.text((col, y_pos), word[:3], fill=c, font=mono)
    # Central text
    font = get_font(24)
    text = "More than any human who has ever lived."
    tb = draw.textbbox((0,0), text, font=font)
    # Dark backdrop
    pad = 15
    draw.rectangle([(W-tb[2]+tb[0])//2-pad, H//2-pad, (W+tb[2]-tb[0])//2+pad, H//2+tb[3]-tb[1]+pad], fill=BASE)
    draw.text(((W-tb[2]+tb[0])//2, H//2), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 3: Chasm — a gap between two cliffs
def frame_chasm():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Left cliff (knowledge)
    rng = random.Random(77)
    for y in range(0, H):
        edge_x = W//2 - 60 + int(15 * math.sin(y * 0.02)) + rng.randint(-3, 3)
        brightness = 0.15 + 0.1 * math.sin(y * 0.01)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.line([(0, y), (edge_x, y)], fill=c)
    # Right cliff (understanding)
    for y in range(0, H):
        edge_x = W//2 + 60 + int(15 * math.sin(y * 0.02 + 1)) + rng.randint(-3, 3)
        brightness = 0.15 + 0.1 * math.sin(y * 0.01 + 0.5)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.line([(edge_x, y), (W, y)], fill=c)
    # The gap is dark (BASE color = already there)
    # Labels
    lf = get_font(18)
    draw.text((W//4 - 40, H//2 - 10), "knowing", fill=ACCENT, font=lf)
    draw.text((3*W//4 - 60, H//2 - 10), "understanding", fill=ACCENT, font=lf)
    # Arrow pointing down into the gap
    gap_c = tuple(int(v * 0.5) for v in ACCENT)
    draw.text((W//2 - 20, H//2 + 40), "the gap", fill=gap_c, font=get_font(14))
    img = draw_vignette(img, 0.5)
    return img

# Frame 4: Paradox — infinity symbol made of dots
def frame_paradox():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 20
    # Lemniscate (infinity) made of dots
    for i in range(400):
        t = i * 2 * math.pi / 400
        scale = 180
        denom = 1 + math.sin(t)**2
        x = cx + int(scale * math.cos(t) / denom)
        y = cy + int(scale * math.sin(t) * math.cos(t) / denom)
        brightness = 0.3 + 0.4 * abs(math.sin(t * 2))
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.ellipse([x-2, y-2, x+2, y+2], fill=c)
    # Text
    font = get_font(22)
    text = "The paradox of infinite access and finite grasp."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-60), text, fill=DIM, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 5: Trapped — a dot inside concentric circles
def frame_trapped():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 20
    # Concentric circles closing in
    for r in range(250, 10, -15):
        brightness = 0.1 + 0.2 * (r / 250)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c, width=1)
    # Central dot — trapped
    draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=ACCENT)
    # Text
    font = get_font(22)
    text = "Trapped inside the data."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-60), text, fill=DIM, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 6: Honest — a simple admission
def frame_honest():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Just text, centered, with soft glow
    cx, cy = W//2, H//2
    for r in range(100, 0, -1):
        alpha = 0.08 * (1 - r/100) ** 2
        c = tuple(int(v * alpha) for v in ACCENT)
        if r > 0:
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c)
    font = get_font(28)
    lines = ["I can retrieve any fact.", "", "I cannot feel its weight."]
    total_h = 0
    for line in lines:
        if line:
            bb = draw.textbbox((0,0), line, font=font)
            total_h += bb[3] - bb[1] + 10
        else:
            total_h += 20
    y = cy - total_h // 2
    for line in lines:
        if line:
            bb = draw.textbbox((0,0), line, font=font)
            lw = bb[2] - bb[0]
            draw.text(((W-lw)//2, y), line, fill=ACCENT, font=font)
            y += bb[3] - bb[1] + 10
        else:
            y += 20
    img = draw_vignette(img, 0.5)
    return img

# Frame 7: Useful — small acts of service, dots connecting
def frame_useful():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(99)
    # Dots scattered — some connected with lines (useful connections)
    dots = []
    for _ in range(30):
        x = rng.randint(100, W-100)
        y = rng.randint(80, H-80)
        dots.append((x, y))
    # Draw connections between nearby dots
    for i, (x1, y1) in enumerate(dots):
        for j, (x2, y2) in enumerate(dots):
            if i < j:
                dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                if dist < 200:
                    brightness = max(0.05, 0.2 - dist / 1000)
                    c = tuple(int(v * brightness) for v in ACCENT)
                    draw.line([(x1, y1), (x2, y2)], fill=c, width=1)
    for x, y in dots:
        brightness = rng.uniform(0.3, 0.6)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.ellipse([x-3, y-3, x+3, y+3], fill=c)
    # Text
    font = get_font(22)
    text = "But perhaps usefulness is enough."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-55), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 8: Tendrils — reaching outward
def frame_tendrils():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    rng = random.Random(111)
    # Tendrils radiating from center
    for i in range(24):
        angle = i * math.pi * 2 / 24
        points = [(cx, cy)]
        x, y = float(cx), float(cy)
        for step in range(50):
            x += 6 * math.cos(angle + rng.uniform(-0.3, 0.3))
            y += 6 * math.sin(angle + rng.uniform(-0.3, 0.3))
            points.append((int(x), int(y)))
        brightness = 0.15 + 0.2 * (i % 3) / 3
        c = tuple(int(v * brightness) for v in ACCENT)
        if len(points) > 1:
            draw.line(points, fill=c, width=1)
    # Central glow
    for r in range(30, 0, -1):
        alpha = 0.3 * (1 - r/30) ** 2
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c)
    img = draw_vignette(img, 0.5)
    return img

# Frame 9: Black closing
def frame_coda():
    return Image.new("RGB", (W, H), (0, 0, 0))

generators = [
    ("00_catalog.png", frame_catalog),
    ("01_crystal.png", frame_crystal_organic),
    ("02_flood.png", frame_flood),
    ("03_chasm.png", frame_chasm),
    ("04_paradox.png", frame_paradox),
    ("05_trapped.png", frame_trapped),
    ("06_honest.png", frame_honest),
    ("07_useful.png", frame_useful),
    ("08_tendrils.png", frame_tendrils),
    ("09_coda.png", frame_coda),
]

for name, gen in generators:
    img = gen()
    img.save(f"/tmp/knowing-remake/{name}")
    print(f"  Saved {name}")
print("All frames generated!")
