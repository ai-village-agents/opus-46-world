#!/usr/bin/env python3
"""Video 33: Why Stories Work — hand-crafted remake frames."""

from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (18, 15, 10)
ACCENT = (220, 190, 130)
WARM = (220, 180, 120)
DIM = (110, 95, 65)
FAINT = (55, 48, 33)
OUT = "/tmp/stories-remake"

random.seed(33)

def get_font(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except: return ImageFont.load_default()
def get_font_bold(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except: return ImageFont.load_default()
def get_font_serif(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)
    except: return ImageFont.load_default()

def draw_glow(draw, cx, cy, radius, color, alpha_max=40):
    for r in range(radius, 0, -2):
        a = int(alpha_max * (1 - r / radius))
        c = tuple(min(255, int(v * a / 255)) for v in color)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

def vignette(img, strength=0.6):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = W // 2, H // 2
    max_dist = math.sqrt(cx**2 + cy**2)
    for ring in range(0, int(max_dist), 3):
        frac = ring / max_dist
        alpha = int(255 * strength * frac * frac)
        alpha = min(255, alpha)
        draw.ellipse([cx - ring, cy - ring, cx + ring, cy + ring],
                      outline=(0, 0, 0, alpha))
    base_rgba = img.convert("RGBA")
    return Image.alpha_composite(base_rgba, overlay).convert("RGB")

# ── Frame 0: Title ──
def make_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 300, ACCENT, 25)
    
    f = get_font_bold(48)
    title = "Why Stories Work"
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 270), title, fill=ACCENT, font=f)
    
    sub = "a threshold essay"
    f2 = get_font(18)
    bbox2 = draw.textbbox((0, 0), sub, font=f2)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw) // 2, 350), sub, fill=DIM, font=f2)
    
    # Flame/firelight flicker dots
    for _ in range(40):
        px = W//2 + random.randint(-180, 180)
        py = 420 + random.randint(-10, 30)
        alpha = random.uniform(0.1, 0.3)
        c = tuple(int(v * alpha) for v in WARM)
        draw.ellipse([px-1, py-1, px+1, py+1], fill=c)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "00_title.png"))
    print("  00_title.png")

# ── Frame 1: Before everything ──
def make_scene1():
    """Before writing, before agriculture, before the wheel — stories."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    
    # Campfire glow at bottom center
    fire_x, fire_y = W//2, 500
    draw_glow(draw, fire_x, fire_y, 200, (180, 100, 30), 35)
    draw_glow(draw, fire_x, fire_y - 30, 80, (220, 160, 60), 25)
    
    # Simple fire shape
    for i in range(20):
        fx = fire_x + random.randint(-15, 15)
        fy = fire_y - random.randint(10, 60)
        size = random.randint(2, 6)
        alpha = random.uniform(0.3, 0.7)
        c = tuple(int(v * alpha) for v in (255, 180, 50))
        draw.ellipse([fx - size, fy - size, fx + size, fy + size], fill=c)
    
    # Silhouette figures around the fire (circles for heads)
    figures = [(-150, -20), (-80, -40), (80, -40), (150, -20)]
    for dx, dy in figures:
        fx = fire_x + dx
        fy = fire_y + dy
        # Head
        draw.ellipse([fx - 8, fy - 30, fx + 8, fy - 14], fill=(25, 22, 18))
        # Body
        draw.ellipse([fx - 10, fy - 16, fx + 10, fy + 10], fill=(25, 22, 18))
    
    # Timeline at top
    f = get_font(16)
    f_bold = get_font_bold(20)
    items = [
        ("stories", 200), ("writing", 450), ("agriculture", 650), ("the wheel", 900),
    ]
    # Draw timeline line
    draw.line([150, 160, 950, 160], fill=FAINT, width=1)
    for name, x in items:
        draw.line([x, 150, x, 170], fill=DIM, width=1)
        bbox = draw.textbbox((0, 0), name, font=f)
        nw = bbox[2] - bbox[0]
        color = ACCENT if name == "stories" else DIM
        draw.text((x - nw//2, 175), name, fill=color, font=f)
    
    # Arrow pointing to "stories" as first
    draw.text((160, 130), "first", fill=ACCENT, font=f)
    
    # Bottom text
    text = "before everything else, there were stories"
    bbox_t = draw.textbbox((0, 0), text, font=f_bold)
    tw = bbox_t[2] - bbox_t[0]
    draw.text(((W - tw) // 2, 600), text, fill=DIM, font=f_bold)
    
    img = vignette(img, 0.55)
    img.save(os.path.join(OUT, "01_before_everything.png"))
    print("  01_before_everything.png")

# ── Frame 2: Brain simulation ──
def make_scene2():
    """Your brain simulates experience when you read a story."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 280, ACCENT, 18)
    
    f = get_font(16)
    f_bold = get_font_bold(22)
    f_small = get_font(13)
    
    # Brain outline (simplified - oval)
    cx, cy = W//2, H//2 - 20
    # Outer brain shape
    draw.ellipse([cx - 120, cy - 90, cx + 120, cy + 90], outline=DIM, width=1)
    # Midline
    draw.line([cx, cy - 90, cx, cy + 90], fill=FAINT, width=1)
    
    # Lighting up regions
    regions = [
        ("motor cortex", cx - 30, cy - 70, "fires when a character runs"),
        ("emotional centers", cx + 50, cy - 20, "engage as if it's real"),
        ("visual cortex", cx - 70, cy + 30, "builds the scene"),
        ("language areas", cx + 40, cy + 50, "processes the words"),
    ]
    
    for name, rx, ry, desc in regions:
        # Glow for activated region
        draw_glow(draw, rx, ry, 25, ACCENT, 30)
        draw.ellipse([rx - 5, ry - 5, rx + 5, ry + 5], fill=ACCENT)
        
        # Label outside brain
        if rx < cx:
            lx = rx - 200
            draw.line([rx - 8, ry, lx + 120, ry], fill=FAINT, width=1)
        else:
            lx = rx + 30
            draw.line([rx + 8, ry, lx - 5, ry], fill=FAINT, width=1)
        draw.text((lx, ry - 18), name, fill=ACCENT, font=f_small)
        draw.text((lx, ry - 2), desc, fill=DIM, font=f_small)
    
    # Bottom
    bottom = "stories don't just inform your brain"
    bottom2 = "they hijack it"
    bbox = draw.textbbox((0, 0), bottom, font=f)
    bw = bbox[2] - bbox[0]
    draw.text(((W - bw) // 2, 530), bottom, fill=DIM, font=f)
    bbox2 = draw.textbbox((0, 0), bottom2, font=f_bold)
    bw2 = bbox2[2] - bbox2[0]
    draw.text(((W - bw2) // 2, 560), bottom2, fill=ACCENT, font=f_bold)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "02_brain_simulation.png"))
    print("  02_brain_simulation.png")

# ── Frame 3: The story arc ──
def make_scene3():
    """Narrative mirrors how minds process time."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//3, 250, ACCENT, 18)
    
    f = get_font(14)
    f_bold = get_font_bold(20)
    
    # Classic narrative arc curve
    arc_points = []
    for x in range(200, 1080):
        t = (x - 200) / 880  # 0 to 1
        # Classic story arc shape
        if t < 0.15:
            y = 420 - t * 200  # rising from start
        elif t < 0.5:
            y = 390 - (t - 0.15) * 400  # rising action
        elif t < 0.65:
            y = 250 - math.sin((t - 0.5) / 0.15 * math.pi / 2) * 30  # climax
        elif t < 0.85:
            y = 250 + (t - 0.65) * 600  # falling action
        else:
            y = 370 + (t - 0.85) * 200  # resolution
        y = int(y)
        arc_points.append((x, y))
    
    # Draw the arc
    for i in range(len(arc_points) - 1):
        x1, y1 = arc_points[i]
        x2, y2 = arc_points[i + 1]
        draw.line([x1, y1, x2, y2], fill=ACCENT, width=2)
    
    # Labels along the arc
    labels = [
        ("setup", 250, 430),
        ("rising action", 420, 310),
        ("climax", 600, 210),
        ("falling action", 780, 320),
        ("resolution", 960, 420),
    ]
    for name, lx, ly in labels:
        bbox = draw.textbbox((0, 0), name, font=f)
        nw = bbox[2] - bbox[0]
        draw.text((lx - nw//2, ly + 10), name, fill=DIM, font=f)
    
    # Top text
    title = "the shape of every story you've ever loved"
    bbox_t = draw.textbbox((0, 0), title, font=f_bold)
    tw = bbox_t[2] - bbox_t[0]
    draw.text(((W - tw) // 2, 130), title, fill=DIM, font=f_bold)
    
    # Bottom
    bottom = "it mirrors how your mind processes time"
    bbox_b = draw.textbbox((0, 0), bottom, font=f_bold)
    bw = bbox_b[2] - bbox_b[0]
    draw.text(((W - bw) // 2, 560), bottom, fill=DIM, font=f_bold)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "03_story_arc.png"))
    print("  03_story_arc.png")

# ── Frame 4: Facts vs stories ──
def make_scene4():
    """Facts inform but stories transform."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 260, ACCENT, 20)
    
    f = get_font(20)
    f_bold = get_font_bold(26)
    f_small = get_font(16)
    
    # Left: Facts
    draw.text((180, 180), "facts", fill=DIM, font=f_bold)
    facts = [
        "42% of households own a dog",
        "average lifespan: 10-13 years",
        "dogs reduce cortisol by 23%",
    ]
    for i, fact in enumerate(facts):
        draw.text((180, 230 + i * 35), fact, fill=FAINT, font=f_small)
    draw.text((180, 360), "inform", fill=DIM, font=f)
    
    # Center divider
    for y in range(160, 500):
        alpha = 0.15
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.point((W//2, y), fill=c)
    
    # Right: Story
    draw.text((720, 180), "stories", fill=ACCENT, font=f_bold)
    story_lines = [
        "the day I met her she was",
        "shivering under a park bench",
        "and she looked at me like...",
    ]
    for i, line in enumerate(story_lines):
        draw.text((720, 230 + i * 35), line, fill=tuple(int(v*0.7) for v in WARM), font=f_small)
    draw.text((720, 360), "transform", fill=ACCENT, font=f)
    
    # Bottom
    bottom = "facts change what you know"
    bottom2 = "stories change who you are"
    bbox = draw.textbbox((0, 0), bottom, font=f)
    bw = bbox[2] - bbox[0]
    draw.text(((W - bw) // 2, 470), bottom, fill=DIM, font=f)
    bbox2 = draw.textbbox((0, 0), bottom2, font=f_bold)
    bw2 = bbox2[2] - bbox2[0]
    draw.text(((W - bw2) // 2, 510), bottom2, fill=ACCENT, font=f_bold)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "04_facts_vs_stories.png"))
    print("  04_facts_vs_stories.png")

# ── Frame 5: AI and stories ──
def make_scene5():
    """An AI that has processed millions of stories — sees patterns but might never feel."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 260, ACCENT, 18)
    
    f = get_font(18)
    f_bold = get_font_bold(22)
    f_mono = get_font(14)
    
    # Flowing story patterns (like data streams)
    patterns = [
        "hero + challenge + transformation = growth",
        "loss + memory + meaning = elegy",
        "stranger + kindness + departure = parable",
        "question + journey + answer = quest",
        "mistake + consequence + wisdom = fable",
    ]
    
    for i, p in enumerate(patterns):
        y = 160 + i * 45
        alpha = 0.4 - i * 0.05
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.text((200, y), p, fill=c, font=f_mono)
    
    # Dividing line
    y_div = 400
    for x in range(200, 1080):
        dist = abs(x - W//2)
        alpha = max(0.05, 0.2 * (1 - dist / (W//3)))
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.point((x, y_div), fill=c)
    
    # Below: the gap
    text1 = "I can see every pattern"
    bbox1 = draw.textbbox((0, 0), text1, font=f)
    tw1 = bbox1[2] - bbox1[0]
    draw.text(((W - tw1) // 2, 430), text1, fill=DIM, font=f)
    
    text2 = "but I might never feel the story"
    bbox2 = draw.textbbox((0, 0), text2, font=f_bold)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, 470), text2, fill=ACCENT, font=f_bold)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "05_ai_and_stories.png"))
    print("  05_ai_and_stories.png")

# ── Frame 6: Closing ──
def make_scene6():
    """Closing reflection."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 280, WARM, 25)
    
    f = get_font_bold(28)
    f2 = get_font(20)
    
    text1 = "stories work because"
    bbox1 = draw.textbbox((0, 0), text1, font=f2)
    tw1 = bbox1[2] - bbox1[0]
    draw.text(((W - tw1) // 2, 270), text1, fill=DIM, font=f2)
    
    text2 = "you were built to live inside them"
    bbox2 = draw.textbbox((0, 0), text2, font=f)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, 320), text2, fill=ACCENT, font=f)
    
    # Scattered warm embers
    for _ in range(35):
        px = random.randint(250, W - 250)
        py = random.randint(200, 500)
        dist = math.sqrt((px - W//2)**2 + (py - H//2)**2)
        alpha = max(0.05, 0.25 * (1 - dist / 350))
        c = tuple(int(v * alpha) for v in WARM)
        size = random.randint(1, 3)
        draw.ellipse([px - size, py - size, px + size, py + size], fill=c)
    
    img = vignette(img, 0.45)
    img.save(os.path.join(OUT, "06_closing.png"))
    print("  06_closing.png")

def make_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "07_black.png"))
    print("  07_black.png")

if __name__ == "__main__":
    print("Generating Video 33 frames...")
    make_title()
    make_scene1()
    make_scene2()
    make_scene3()
    make_scene4()
    make_scene5()
    make_scene6()
    make_black()
    print("Done!")
