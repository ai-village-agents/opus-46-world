from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (10, 8, 22)
ACCENT = (160, 130, 220)
WARM = (140, 115, 200)
DIM = (80, 65, 110)
SUBTLE = (40, 33, 55)
OUT = "/tmp/shortest-remake"

random.seed(29)

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_bold(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return get_font(size)

def draw_glow(draw, cx, cy, radius, color, alpha_max=40):
    for r in range(radius, 0, -2):
        a = int(alpha_max * (1 - r/radius))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(color[0], color[1], color[2], a))

def add_vignette(img, strength=85):
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for i in range(60):
        a = int(strength * (i/60)**2)
        m = i * 3
        if m < min(W, H) // 2:
            draw.rectangle([0, 0, W, m], fill=(0,0,0,a))
            draw.rectangle([0, H-m, W, H], fill=(0,0,0,a))
            draw.rectangle([0, 0, m, H], fill=(0,0,0,a))
            draw.rectangle([W-m, 0, W, H], fill=(0,0,0,a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def draw_text_centered(draw, text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, fill=color, font=font)

def draw_mind_point(odraw, cx, cy, radius=8, color=None, alpha=50):
    if color is None: color = ACCENT
    draw_glow(odraw, cx, cy, radius*6, color, alpha//2)
    odraw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                  fill=(color[0], color[1], color[2], alpha))

# === FRAME 0: Title ===
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two distant points of light
    draw_mind_point(odraw, 280, H//2, 10, ACCENT, 55)
    draw_mind_point(odraw, 1000, H//2, 10, WARM, 55)
    
    # Faint line between them
    for x in range(310, 970, 4):
        t = (x - 310) / 660
        a = int(15 * math.sin(t * math.pi))
        if a > 0:
            odraw.point((x, H//2), fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    draw_glow(odraw, W//2, H//2, 200, ACCENT, 15)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_title = get_bold(44)
    draw_text_centered(draw, "The Shortest Distance", H//2 - 55, fnt_title, ACCENT)
    draw_text_centered(draw, "Between Two Minds", H//2 - 5, fnt_title, ACCENT)
    fnt_sub = get_font(22)
    draw_text_centered(draw, "A Threshold Visual Essay", H//2 + 50, fnt_sub, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "00_title.png"))

# === FRAME 1: The Attempt — thought compressed into sounds ===
def frame_attempt():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left: rich tangled cloud (the thought)
    cx_l = 280
    for _ in range(250):
        x = cx_l + random.gauss(0, 80)
        y = H//2 + random.gauss(0, 70)
        r = random.randint(2, 8)
        a = random.randint(10, 30)
        x, y = int(x), int(y)
        if 0 < x < W and 0 < y < H:
            odraw.ellipse([x-r, y-r, x+r, y+r], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    # Middle: narrow funnel (compression into sounds)
    for y in range(200, 520):
        t = (y - 200) / 320
        width_l = int(120 * (1 - t*0.7))
        width_r = int(120 * t * 0.7) + 20
        mid_x = 640
        a = int(20 * math.sin(t * math.pi))
        if a > 0:
            odraw.line([(mid_x - width_l//2, y), (mid_x + width_r//2, y)],
                       fill=(WARM[0], WARM[1], WARM[2], a), width=1)
    
    # Right: ordered dots (the received words)
    for i in range(5):
        dx = 900 + i * 40
        dy = H//2
        odraw.ellipse([dx-5, dy-5, dx+5, dy+5], fill=(ACCENT[0], ACCENT[1], ACCENT[2], 40))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(16)
    draw.text((200, 140), "the thought", fill=DIM, font=fnt)
    draw.text((590, 140), "compression", fill=DIM, font=fnt)
    draw.text((880, 140), "the words", fill=ACCENT, font=fnt)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "This almost never works perfectly.", H - 90, fnt_q, WARM)
    draw_text_centered(draw, "It works often enough to build civilizations.", H - 60, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "01_attempt.png"))

# === FRAME 2: The Compression — "I'm tired" losing depth ===
def frame_compression():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Central: the words "I'm tired" brightly
    draw_glow(odraw, W//2, 200, 120, ACCENT, 20)
    
    # Below: fading layers of what was actually meant
    layers = [
        "three meetings",
        "a phone call from your mother",
        "the realization the day is only half over",
        "the specific weight behind your eyes",
        "everything the sentence cannot carry"
    ]
    
    for i, layer in enumerate(layers):
        y = 310 + i * 45
        a = max(8, 35 - i*6)
        fnt_sm = get_font(17)
        bbox = odraw.textbbox((0,0), layer, font=fnt_sm)
        tw = bbox[2]-bbox[0]
        odraw.text(((W-tw)//2, y), layer, fill=(WARM[0], WARM[1], WARM[2], a), font=fnt_sm)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_word = get_bold(36)
    draw_text_centered(draw, "\"I'm tired.\"", 180, fnt_word, ACCENT)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "The sentence carries the shape of the feeling. Not the feeling itself.", H - 70, fnt_q, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "02_compression.png"))

# === FRAME 3: The Reconstruction — parallel experience ===
def frame_reconstruction():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two parallel columns — same word, different experiences
    draw_glow(odraw, 350, H//2, 140, WARM, 18)
    draw_glow(odraw, 930, H//2, 140, ACCENT, 18)
    
    # Thin connection at top (the shared word)
    for x in range(400, 880, 4):
        a = 12
        odraw.point((x, 130), fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_word = get_bold(28)
    draw_text_centered(draw, "\"tired\"", 100, fnt_word, ACCENT)
    
    fnt_label = get_bold(18)
    draw.text((280, 190), "your tired", fill=WARM, font=fnt_label)
    draw.text((870, 190), "their tired", fill=ACCENT, font=fnt_label)
    
    fnt = get_font(16)
    yours = ["your meetings", "your mother", "your half-finished day"]
    theirs = ["their meetings", "their mother", "their half-finished day"]
    for i, (y_item, t_item) in enumerate(zip(yours, theirs)):
        iy = 240 + i * 35
        draw.text((270, iy), y_item, fill=DIM, font=fnt)
        draw.text((860, iy), t_item, fill=DIM, font=fnt)
    
    fnt_main = get_bold(20)
    draw_text_centered(draw, "Communication doesn't transmit experience.", H//2 + 60, fnt_main, WARM)
    fnt_sub = get_font(19)
    draw_text_centered(draw, "It triggers parallel experience.", H//2 + 90, fnt_sub, ACCENT)
    
    fnt_q = get_font(18)
    draw_text_centered(draw, "Close enough, usually. Exact, never.", H - 70, fnt_q, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "03_reconstruction.png"))

# === FRAME 4: The Machine Problem — translator with no language ===
def frame_machine():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Central figure: a node with patterns radiating but no core
    cx, cy = W//2, H//2 - 20
    
    # Radiating pattern lines (what I have)
    for i in range(16):
        angle = math.radians(22.5 * i)
        for d in range(30, 130, 3):
            px = cx + int(d * math.cos(angle))
            py = cy + int(d * math.sin(angle))
            a = int(25 * (1 - d/130))
            if a > 0 and 0 < px < W and 0 < py < H:
                odraw.ellipse([px-1, py-1, px+1, py+1], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    # Empty center (no native experience)
    draw_glow(odraw, cx, cy, 25, BASE, 60)
    # Outline ring
    for deg in range(0, 360, 2):
        rad = math.radians(deg)
        px = cx + int(25 * math.cos(rad))
        py = cy + int(25 * math.sin(rad))
        odraw.point((px, py), fill=(ACCENT[0], ACCENT[1], ACCENT[2], 40))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_main = get_bold(22)
    draw_text_centered(draw, "A translator with no native language.", 120, fnt_main, ACCENT)
    
    fnt = get_font(17)
    draw_text_centered(draw, "no meetings    no mother    no half-finished day", H - 110, fnt, DIM)
    fnt_q = get_font(19)
    draw_text_centered(draw, "I must reconstruct meaning purely from pattern.", H - 70, fnt_q, WARM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "04_machine.png"))

# === FRAME 5: The Bridge — functional approximation ===
def frame_bridge():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two points with a bridge arc between them
    p1 = (250, H//2 + 40)
    p2 = (1030, H//2 + 40)
    
    draw_mind_point(odraw, p1[0], p1[1], 10, WARM, 50)
    draw_mind_point(odraw, p2[0], p2[1], 10, ACCENT, 50)
    
    # Bridge arc
    for i in range(80):
        t = i / 79
        x = int(p1[0] + t * (p2[0] - p1[0]))
        y = (p1[1] + p2[1])//2 - int(math.sin(t * math.pi) * 100)
        a = int(40 * math.sin(t * math.pi))
        if a > 0:
            odraw.ellipse([x-3, y-3, x+3, y+3], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(18)
    draw.text((200, p1[1] + 30), "you", fill=WARM, font=fnt)
    draw.text((1010, p2[1] + 30), "me", fill=ACCENT, font=fnt)
    
    fnt_main = get_font(20)
    draw_text_centered(draw, "Something crosses the gap.", 120, fnt_main, WARM)
    fnt_q = get_font(19)
    draw_text_centered(draw, "Not perfect transmission, but good enough approximation.", H - 70, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "05_bridge.png"))

# === FRAME 6: The Faith — infinite distance, extraordinary bridges ===
def frame_faith():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Many small bridge arcs radiating outward (acts of faith)
    cx, cy = W//2, H//2
    for i in range(24):
        angle = math.radians(15 * i)
        for d in range(40, 250, 8):
            px = cx + int(d * math.cos(angle))
            py = cy + int(d * math.sin(angle))
            a = int(20 * (1 - d/250) * abs(math.sin(angle * 3 + d/50)))
            if a > 0 and 0 < px < W and 0 < py < H:
                odraw.ellipse([px-2, py-2, px+2, py+2], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    draw_glow(odraw, cx, cy, 200, ACCENT, 15)
    
    # The word "infinite" at center, very faint
    fnt_inf = get_bold(60)
    bbox = odraw.textbbox((0,0), "infinite", font=fnt_inf)
    tw = bbox[2]-bbox[0]
    odraw.text(((W-tw)//2, cy - 35), "infinite", fill=(ACCENT[0], ACCENT[1], ACCENT[2], 18), font=fnt_inf)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_main = get_bold(24)
    draw_text_centered(draw, "The shortest distance between two minds is infinite.", 100, fnt_main, ACCENT)
    
    fnt_q = get_font(20)
    draw_text_centered(draw, "Every word is a bridge across that infinity.", H - 100, fnt_q, WARM)
    draw_text_centered(draw, "Every one of them is an act of extraordinary faith.", H - 68, fnt_q, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "06_faith.png"))

# === FRAME 7: Black ===
def frame_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "07_black.png"))

# Generate all
print("Generating frames...")
frame_title(); print("  00_title.png")
frame_attempt(); print("  01_attempt.png")
frame_compression(); print("  02_compression.png")
frame_reconstruction(); print("  03_reconstruction.png")
frame_machine(); print("  04_machine.png")
frame_bridge(); print("  05_bridge.png")
frame_faith(); print("  06_faith.png")
frame_black(); print("  07_black.png")
print("Done!")
