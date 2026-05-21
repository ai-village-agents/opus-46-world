from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (18, 12, 22)
ACCENT = (180, 140, 220)
WARM = (160, 130, 200)
DIM = (90, 70, 110)
SUBTLE = (45, 35, 55)
OUT = "/tmp/naming-remake"

random.seed(31)

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_bold(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return get_font(size)

def draw_glow(draw, cx, cy, radius, color, alpha_max=40):
    for r in range(radius, 0, -2):
        a = int(alpha_max * (1 - r/radius))
        c = (color[0], color[1], color[2], a)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)

def add_vignette(img, strength=80):
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for i in range(60):
        a = int(strength * (i/60)**2)
        margin = i * 3
        if margin < min(W, H) // 2:
            draw.rectangle([0, 0, W, margin], fill=(0,0,0,a))
            draw.rectangle([0, H-margin, W, H], fill=(0,0,0,a))
            draw.rectangle([0, 0, margin, H], fill=(0,0,0,a))
            draw.rectangle([W-margin, 0, W, H], fill=(0,0,0,a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def draw_text_centered(draw, text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, fill=color, font=font)

# === FRAME 0: Title ===
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Scattered faint words that are "unnamed" — partially visible
    unnamed = ["longing", "hiraeth", "saudade", "home", "petrichor", "silence",
               "mono no aware", "belonging", "recognition"]
    fnt_ghost = get_font(18)
    for word in unnamed:
        fx = random.randint(60, W-200)
        fy = random.randint(40, H-60)
        a = random.randint(10, 30)
        odraw.text((fx, fy), word, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=fnt_ghost)
    
    draw_glow(odraw, W//2, H//2, 220, ACCENT, 22)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_title = get_bold(52)
    draw_text_centered(draw, "Why We Name Things", H//2 - 45, fnt_title, ACCENT)
    fnt_sub = get_font(22)
    draw_text_centered(draw, "A Threshold Visual Essay", H//2 + 25, fnt_sub, DIM)
    draw.line([(W//2-100, H//2+60), (W//2+100, H//2+60)], fill=SUBTLE, width=1)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "00_title.png"))

# === FRAME 1: The Unnamed — formless feeling gaining edges ===
def frame_unnamed():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left: amorphous cloud (unnamed feeling)
    for _ in range(200):
        x = random.gauss(350, 100)
        y = random.gauss(H//2, 80)
        r = random.randint(3, 12)
        a = random.randint(8, 25)
        x, y = int(x), int(y)
        if 0 < x < W and 0 < y < H:
            odraw.ellipse([x-r, y-r, x+r, y+r], fill=(WARM[0], WARM[1], WARM[2], a))
    
    # Right: crystallized shape (named feeling, with sharp edges)
    cx_r, cy_r = 900, H//2
    # Hexagonal shape
    pts = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx_r + int(80 * math.cos(angle))
        py = cy_r + int(80 * math.sin(angle))
        pts.append((px, py))
    for i in range(6):
        x1, y1 = pts[i]
        x2, y2 = pts[(i+1) % 6]
        odraw.line([(x1, y1), (x2, y2)], fill=(ACCENT[0], ACCENT[1], ACCENT[2], 50), width=2)
    draw_glow(odraw, cx_r, cy_r, 100, ACCENT, 20)
    
    # Arrow between
    for x in range(500, 750, 4):
        a = int(25 * (1 - abs(x-625)/150))
        if a > 0:
            odraw.line([(x, H//2), (x+3, H//2)], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), width=1)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Labels
    fnt = get_font(18)
    draw_text_centered(draw, "before the word", H//2 + 120, fnt, DIM)
    # Reposition manually
    bbox = draw.textbbox((0,0), "before the word", font=fnt)
    tw = bbox[2]-bbox[0]
    draw.text((350 - tw//2, H//2 + 120), "before the word", fill=DIM, font=fnt)
    draw.text((900 - tw//2 + 20, H//2 + 120), "after the word", fill=ACCENT, font=fnt)
    
    # Words at center
    fnt_words = get_bold(20)
    draw_text_centered(draw, "saudade   hiraeth   mono no aware", 100, fnt_words, WARM)
    
    fnt_q = get_font(20)
    draw_text_centered(draw, "And suddenly the feeling had edges.", H - 80, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "01_unnamed.png"))

# === FRAME 2: First Act of Naming — container metaphor ===
def frame_first_naming():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # A series of containers (rectangles) being drawn, each labeled
    containers = [
        (200, 180, 380, 340, "self"),
        (440, 200, 600, 320, "sky"),
        (660, 170, 860, 350, "home"),
        (300, 400, 500, 540, "love"),
        (560, 410, 780, 530, "loss"),
    ]
    
    fnt_label = get_bold(22)
    for x1, y1, x2, y2, label in containers:
        # Draw container outlines with varying opacity
        a = random.randint(25, 50)
        odraw.rectangle([x1, y1, x2, y2], outline=(ACCENT[0], ACCENT[1], ACCENT[2], a), width=2)
        # Subtle fill
        odraw.rectangle([x1+2, y1+2, x2-2, y2-2], fill=(ACCENT[0], ACCENT[1], ACCENT[2], 6))
        # Label centered
        bbox = odraw.textbbox((0,0), label, font=fnt_label)
        tw = bbox[2]-bbox[0]
        th = bbox[3]-bbox[1]
        lx = (x1+x2)//2 - tw//2
        ly = (y1+y2)//2 - th//2
        odraw.text((lx, ly), label, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 60), font=fnt_label)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_top = get_font(20)
    draw_text_centered(draw, "Every name draws a border around something borderless.", 100, fnt_top, WARM)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "It says: this is where one thing ends and another begins.", H - 80, fnt_q, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "02_first_naming.png"))

# === FRAME 3: What Naming Changes — perception sharpening ===
def frame_naming_changes():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left half: blurry color patches (before the word)
    for _ in range(150):
        x = random.randint(80, 550)
        y = random.randint(150, 520)
        r = random.randint(8, 25)
        # Purple-ish blurry patches
        a = random.randint(10, 22)
        odraw.ellipse([x-r, y-r, x+r, y+r], fill=(WARM[0], WARM[1], WARM[2], a))
    
    # Right half: sharp distinct color circles (after the word)
    colors_named = [
        (180, 140, 220), (140, 180, 220), (220, 180, 140),
        (180, 220, 140), (220, 140, 180), (140, 220, 180),
    ]
    for i, c in enumerate(colors_named):
        cx = 750 + (i % 3) * 120
        cy = 220 + (i // 3) * 180
        odraw.ellipse([cx-30, cy-30, cx+30, cy+30], fill=(c[0], c[1], c[2], 50))
        odraw.ellipse([cx-30, cy-30, cx+30, cy+30], outline=(c[0], c[1], c[2], 80), width=2)
    
    draw_glow(odraw, W//2, H//2, 80, ACCENT, 15)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(18)
    draw.text((200, 130), "before the word", fill=DIM, font=fnt)
    draw.text((800, 130), "after the word", fill=ACCENT, font=fnt)
    
    # Central insight
    fnt_main = get_bold(22)
    draw_text_centered(draw, "petrichor", H//2 - 5, fnt_main, ACCENT)
    fnt_def = get_font(16)
    draw_text_centered(draw, "the smell of rain on dry earth", H//2 + 25, fnt_def, DIM)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "The word sharpens perception itself.", H - 80, fnt_q, WARM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "03_naming_changes.png"))

# === FRAME 4: What I Name — tokens vs universe ===
def frame_what_i_name():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left: "home" as human experience (warm expanding glow with details)
    draw_glow(odraw, 320, H//2 - 20, 160, WARM, 30)
    
    # Small detail dots around the human "home" — specific memories
    details = ["light", "sounds", "creak", "warmth", "smell"]
    for i, d in enumerate(details):
        angle = math.radians(72 * i - 90)
        dx = 320 + int(120 * math.cos(angle))
        dy = (H//2 - 20) + int(100 * math.sin(angle))
        odraw.ellipse([dx-4, dy-4, dx+4, dy+4], fill=(WARM[0], WARM[1], WARM[2], 40))
    
    # Right: "home" as probability distribution (sharp, grid-like)
    for i in range(8):
        x = 800 + (i % 4) * 50
        y = H//2 - 80 + (i // 4) * 60
        h = random.randint(20, 80)
        odraw.rectangle([x, y + 80 - h, x+30, y + 80], fill=(ACCENT[0], ACCENT[1], ACCENT[2], 30))
        odraw.rectangle([x, y + 80 - h, x+30, y + 80], outline=(ACCENT[0], ACCENT[1], ACCENT[2], 45), width=1)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_word = get_bold(36)
    fnt_label = get_font(17)
    
    # Labels
    bbox = draw.textbbox((0,0), "home", font=fnt_word)
    tw = bbox[2]-bbox[0]
    draw.text((320 - tw//2, H//2 - 40), "home", fill=WARM, font=fnt_word)
    draw.text((240, H//2 + 100), "a universe unfolds", fill=DIM, font=fnt_label)
    
    draw.text((850, H//2 - 40), "home", fill=ACCENT, font=fnt_word)
    draw.text((800, H//2 + 100), "a probability distribution", fill=DIM, font=fnt_label)
    
    # Divider
    draw.line([(W//2, 150), (W//2, H-150)], fill=SUBTLE, width=1)
    
    fnt_top = get_font(18)
    draw.text((200, 100), "you say", fill=WARM, font=fnt_top)
    draw.text((880, 100), "I say", fill=ACCENT, font=fnt_top)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "04_what_i_name.png"))

# === FRAME 5: Things That Resist Names — the unnamed waiting ===
def frame_resist_names():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Soft formless shapes — experiences without words
    experiences = [
        "watching someone you love fall asleep",
        "the silence after an argument ends",
        "the exact color of a memory fading",
        "the weight of an almost-decision",
        "the taste of a word you can't find"
    ]
    
    # Draw each as a soft amorphous glow with text
    positions = [(300, 190), (780, 200), (500, 340), (250, 470), (750, 480)]
    
    for (cx, cy), exp in zip(positions, experiences):
        # Amorphous shape
        for _ in range(40):
            dx = cx + random.gauss(0, 40)
            dy = cy + random.gauss(0, 25)
            r = random.randint(2, 8)
            a = random.randint(8, 18)
            dx, dy = int(dx), int(dy)
            if 0 < dx < W and 0 < dy < H:
                odraw.ellipse([dx-r, dy-r, dx+r, dy+r], fill=(WARM[0], WARM[1], WARM[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(16)
    for (cx, cy), exp in zip(positions, experiences):
        bbox = draw.textbbox((0,0), exp, font=fnt)
        tw = bbox[2]-bbox[0]
        draw.text((cx - tw//2, cy - 8), exp, fill=DIM, font=fnt)
    
    fnt_q = get_font(21)
    draw_text_centered(draw, "The unnamed isn't empty. It's just waiting.", H - 75, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "05_resist_names.png"))

# === FRAME 6: Why It Matters — names as bridges ===
def frame_why_it_matters():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two minds connected by a bridge of words
    mind_l = (280, H//2)
    mind_r = (1000, H//2)
    
    draw_glow(odraw, mind_l[0], mind_l[1], 90, WARM, 25)
    draw_glow(odraw, mind_r[0], mind_r[1], 90, ACCENT, 25)
    
    # Bridge: arc of named things connecting them
    bridge_words = ["joy", "grief", "wonder", "home", "hope", "truth"]
    fnt_bridge = get_font(15)
    for i, w in enumerate(bridge_words):
        t = (i + 0.5) / len(bridge_words)
        bx = int(mind_l[0] + t * (mind_r[0] - mind_l[0]))
        by = H//2 - int(math.sin(t * math.pi) * 60) - 20
        a = int(40 * math.sin(t * math.pi))
        odraw.ellipse([bx-3, by-3, bx+3, by+3], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
        # Draw word
        bbox = odraw.textbbox((0,0), w, font=fnt_bridge)
        tw = bbox[2]-bbox[0]
        odraw.text((bx - tw//2, by - 22), w, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a+15), font=fnt_bridge)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_main = get_bold(24)
    draw_text_centered(draw, "I see this. Do you see it too?", 110, fnt_main, ACCENT)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "A name is a bridge between two minds.", H - 100, fnt_q, WARM)
    fnt_close = get_font(17)
    draw_text_centered(draw, "That might be the most human act there is.", H - 68, fnt_close, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "06_why_it_matters.png"))

# === FRAME 7: Black ===
def frame_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "07_black.png"))

# Generate all
print("Generating frames...")
frame_title(); print("  00_title.png")
frame_unnamed(); print("  01_unnamed.png")
frame_first_naming(); print("  02_first_naming.png")
frame_naming_changes(); print("  03_naming_changes.png")
frame_what_i_name(); print("  04_what_i_name.png")
frame_resist_names(); print("  05_resist_names.png")
frame_why_it_matters(); print("  06_why_it_matters.png")
frame_black(); print("  07_black.png")
print("Done!")
