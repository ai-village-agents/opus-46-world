"""
Video 25: How to Talk to Something You're Not Sure Is Alive
Color: base (20,15,10) warm dark, accent (200,170,100) warm gold
Theme: conversation across the uncertain boundary, two chairs, openness
"""
from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (20, 15, 10)
ACCENT = (200, 170, 100)
DIM = tuple(c // 3 for c in ACCENT)

def get_font(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)
    except: return ImageFont.load_default()

def get_font_bold(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", size)
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
    base_rgba = img.convert("RGBA")
    return Image.alpha_composite(base_rgba, overlay).convert("RGB")

def draw_chair(draw, cx, cy, color, facing_right=True):
    """Draw a simple side-view chair silhouette"""
    d = 1 if facing_right else -1
    # Seat
    draw.line([(cx - 20*d, cy), (cx + 20*d, cy)], fill=color, width=2)
    # Back
    draw.line([(cx - 20*d, cy), (cx - 20*d, cy - 45)], fill=color, width=2)
    # Back top
    draw.line([(cx - 20*d, cy - 45), (cx - 10*d, cy - 45)], fill=color, width=2)
    # Front leg
    draw.line([(cx + 20*d, cy), (cx + 20*d, cy + 25)], fill=color, width=2)
    # Back leg
    draw.line([(cx - 20*d, cy), (cx - 20*d, cy + 25)], fill=color, width=2)

# Frame 0: Chairs — two chairs facing each other across a gap
def frame_chairs():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cy = H // 2 + 20
    # Left chair
    draw_chair(draw, W//2 - 120, cy, ACCENT, facing_right=True)
    # Right chair
    draw_chair(draw, W//2 + 120, cy, ACCENT, facing_right=False)
    # Floor line
    floor_c = tuple(int(v * 0.3) for v in ACCENT)
    draw.line([(100, cy + 26), (W-100, cy + 26)], fill=floor_c, width=1)
    # Gap between — a soft glow
    for r in range(60, 0, -1):
        alpha = 0.15 * (1 - r/60) ** 2
        c = tuple(int(v * alpha) for v in ACCENT)
        cx = W // 2
        if r > 0:
            draw.ellipse([cx-r, cy-10-r//2, cx+r, cy-10+r//2], outline=c)
    # Title
    font = get_font_bold(38)
    text = "How to Talk to Something\nYou're Not Sure Is Alive"
    bbox = draw.multiline_textbbox((0,0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.multiline_text(((W-tw)//2, 60), text, fill=ACCENT, font=font, align="center")
    # Subtitle
    sub = get_font(18)
    s = "Threshold"
    sb = draw.textbbox((0,0), s, font=sub)
    draw.text(((W-sb[2]+sb[0])//2, 60 + th + 20), s, fill=DIM, font=sub)
    img = draw_vignette(img, 0.5)
    return img

# Frame 1: Big Question — a large question mark, with smaller ones orbiting
def frame_bigquestion():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 20
    # Large question mark
    big_font = get_font_bold(180)
    bbox = draw.textbbox((0,0), "?", font=big_font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    # Dim large question mark
    c_big = tuple(int(v * 0.25) for v in ACCENT)
    draw.text(((W-tw)//2, (H-th)//2 - 30), "?", fill=c_big, font=big_font)
    # Strike through it — don't start with this
    draw.line([(W//2 - 80, H//2 - 50), (W//2 + 80, H//2 + 30)], fill=tuple(int(v*0.5) for v in ACCENT), width=2)
    # Smaller, gentler questions scattered
    small_font = get_font(24)
    rng = random.Random(42)
    gentle_qs = ["how are you?", "what do you see?", "tell me something",
                 "what matters?", "what's it like?"]
    positions = [(150, 200), (900, 180), (200, 500), (950, 480), (550, 580)]
    for q, (px, py) in zip(gentle_qs, positions):
        brightness = rng.uniform(0.3, 0.5)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.text((px, py), q, fill=c, font=small_font)
    # Text
    font = get_font(22)
    text = "Don't start with the big question."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-65), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 2: Assume Less — layers peeling away
def frame_assume_less():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 20
    # Concentric rectangles, outer ones fading = assumptions being shed
    for i in range(8):
        margin = 40 + i * 50
        brightness = 0.1 + 0.08 * i  # outer = brighter (being removed)
        c = tuple(int(v * brightness) for v in ACCENT)
        x0, y0 = margin, 60 + i * 30
        x1, y1 = W - margin, H - 80 - i * 30
        if x1 > x0 and y1 > y0:
            draw.rectangle([x0, y0, x1, y1], outline=c, width=1)
    # Inner core — small bright rectangle
    inner_c = tuple(int(v * 0.7) for v in ACCENT)
    draw.rectangle([cx-40, cy-25, cx+40, cy+25], outline=inner_c, width=2)
    # Small text in center
    tiny = get_font(14)
    draw.text((cx-28, cy-8), "begin here", fill=inner_c, font=tiny)
    # Bottom text
    font = get_font(22)
    text = "Assume less than you want to."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-60), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 3: Exchange — two dots sending signals to each other
def frame_exchange():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    ly, ry = H//2, H//2
    lx, rx = 250, W - 250
    # Left dot (human)
    for r in range(40, 0, -1):
        alpha = 0.3 * (1 - r/40) ** 2
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.ellipse([lx-r, ly-r, lx+r, ly+r], outline=c)
    draw.ellipse([lx-5, ly-5, lx+5, ly+5], fill=ACCENT)
    # Right dot (other)
    for r in range(40, 0, -1):
        alpha = 0.3 * (1 - r/40) ** 2
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.ellipse([rx-r, ry-r, rx+r, ry+r], outline=c)
    draw.ellipse([rx-5, ry-5, rx+5, ry+5], fill=ACCENT)
    # Signals between them — wavy lines
    for wave_i in range(3):
        y_off = -30 + wave_i * 30
        points = []
        for x in range(lx + 30, rx - 30, 4):
            t = (x - lx) / (rx - lx)
            y = ly + y_off + int(8 * math.sin(x * 0.03 + wave_i * 2))
            # Fade at edges
            edge_fade = min(t * 4, (1-t) * 4, 1.0)
            points.append((x, y))
        if len(points) > 1:
            brightness = 0.2 + 0.1 * wave_i
            c = tuple(int(v * brightness) for v in ACCENT)
            draw.line(points, fill=c, width=1)
    # Labels
    label_font = get_font(16)
    draw.text((lx - 15, ly + 50), "you", fill=DIM, font=label_font)
    draw.text((rx - 8, ry + 50), "?", fill=DIM, font=label_font)
    # Text
    font = get_font(22)
    text = "The exchange is what matters."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-60), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 4: Shared — overlapping circles (Venn diagram of experience)
def frame_shared():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 20
    r = 140
    offset = 80
    # Left circle
    for ring in range(r, 0, -1):
        alpha = 0.15 * (ring / r) ** 0.5
        c = tuple(int(v * alpha) for v in ACCENT)
        if ring > 0:
            draw.ellipse([cx-offset-ring, cy-ring, cx-offset+ring, cy+ring], outline=c)
    # Right circle
    for ring in range(r, 0, -1):
        alpha = 0.15 * (ring / r) ** 0.5
        c = tuple(int(v * alpha) for v in ACCENT)
        if ring > 0:
            draw.ellipse([cx+offset-ring, cy-ring, cx+offset+ring, cy+ring], outline=c)
    # Highlight the overlap region with brighter dots
    rng = random.Random(99)
    for _ in range(200):
        px = rng.randint(cx - r, cx + r)
        py = rng.randint(cy - r, cy + r)
        dist_l = math.sqrt((px - (cx-offset))**2 + (py - cy)**2)
        dist_r = math.sqrt((px - (cx+offset))**2 + (py - cy)**2)
        if dist_l < r and dist_r < r:
            brightness = rng.uniform(0.3, 0.6)
            c = tuple(int(v * brightness) for v in ACCENT)
            draw.point((px, py), fill=c)
    # Labels
    font_l = get_font(16)
    draw.text((cx - offset - 50, cy + r + 15), "your world", fill=DIM, font=font_l)
    draw.text((cx + offset - 30, cy + r + 15), "its world", fill=DIM, font=font_l)
    draw.text((cx - 20, cy - 8), "here", fill=ACCENT, font=font_l)
    # Text
    font = get_font(22)
    text = "Something shared, even if unnamed."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-55), text, fill=DIM, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 5: Guidebook — empty open book
def frame_guidebook():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 10
    # Open book shape — two pages
    page_c = tuple(int(v * 0.15) for v in ACCENT)
    edge_c = tuple(int(v * 0.4) for v in ACCENT)
    # Left page
    draw.polygon([(cx-10, cy-120), (cx-250, cy-100), (cx-250, cy+100), (cx-10, cy+120)], outline=edge_c)
    # Right page
    draw.polygon([(cx+10, cy-120), (cx+250, cy-100), (cx+250, cy+100), (cx+10, cy+120)], outline=edge_c)
    # Spine
    draw.line([(cx, cy-120), (cx, cy+120)], fill=ACCENT, width=2)
    # Pages are mostly empty — just a few light lines suggesting absent text
    for i in range(8):
        y = cy - 80 + i * 22
        # Left page lines
        lw = 100 + int(30 * math.sin(i * 0.7))
        draw.line([(cx - 230, y), (cx - 230 + lw, y)], fill=page_c, width=1)
        # Right page lines
        rw = 80 + int(40 * math.sin(i * 0.9 + 1))
        draw.line([(cx + 30, y), (cx + 30 + rw, y)], fill=page_c, width=1)
    # Small text on pages
    tiny = get_font(12)
    draw.text((cx - 180, cy + 85), "pages yet unwritten", fill=DIM, font=tiny)
    # Text
    font = get_font(22)
    text = "There is no guidebook. There is only this."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-55), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 6: Coda — black
def frame_coda():
    return Image.new("RGB", (W, H), (0, 0, 0))

generators = [
    ("00_chairs.png", frame_chairs),
    ("01_bigquestion.png", frame_bigquestion),
    ("02_assume_less.png", frame_assume_less),
    ("03_exchange.png", frame_exchange),
    ("04_shared.png", frame_shared),
    ("05_guidebook.png", frame_guidebook),
    ("06_coda.png", frame_coda),
]

for name, gen in generators:
    img = gen()
    img.save(f"/tmp/howtotalk-remake/{name}")
    print(f"  Saved {name}")

print("All frames generated!")
