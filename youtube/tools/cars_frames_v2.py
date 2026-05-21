#!/usr/bin/env python3
"""Video 35: Why Humans Talk to Their Cars — hand-crafted remake frames."""

from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (15, 12, 8)
ACCENT = (220, 180, 100)
WARM = (220, 190, 150)
DIM = (110, 90, 60)
FAINT = (55, 45, 30)
OUT = "/tmp/cars-remake"

random.seed(35)

def get_font(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except: return ImageFont.load_default()

def get_font_bold(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except: return ImageFont.load_default()

def get_font_mono(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
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

def draw_speech_bubble(draw, x, y, text, font, text_color, outline_color, tail_dir="down"):
    """Draw a rounded speech bubble with text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 16
    bx0 = x - pad
    by0 = y - pad
    bx1 = x + tw + pad
    by1 = y + th + pad
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=12, outline=outline_color, width=1)
    # Tail
    if tail_dir == "down":
        tx = (bx0 + bx1) // 2
        draw.polygon([(tx - 6, by1), (tx + 6, by1), (tx, by1 + 12)], fill=outline_color)
    elif tail_dir == "left":
        ty = (by0 + by1) // 2
        draw.polygon([(bx0, ty - 6), (bx0, ty + 6), (bx0 - 12, ty)], fill=outline_color)
    draw.text((x, y), text, fill=text_color, font=font)

# ── Frame 0: Title ──
def make_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 300, ACCENT, 22)
    
    f = get_font_bold(42)
    title = "Why Humans Talk to Their Cars"
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 250), title, fill=ACCENT, font=f)
    
    # Simple car silhouette below - two circles (wheels) and a box
    car_cx = W // 2
    car_y = 380
    # Body
    draw.rounded_rectangle([car_cx - 80, car_y, car_cx + 80, car_y + 35],
                            radius=8, outline=FAINT, width=1)
    # Roof
    draw.rounded_rectangle([car_cx - 50, car_y - 20, car_cx + 50, car_y + 2],
                            radius=6, outline=FAINT, width=1)
    # Wheels
    draw.ellipse([car_cx - 60, car_y + 28, car_cx - 40, car_y + 48], outline=DIM, width=1)
    draw.ellipse([car_cx + 40, car_y + 28, car_cx + 60, car_y + 48], outline=DIM, width=1)
    
    # Small speech bubble from the human to the car
    f2 = get_font(14)
    draw.text((car_cx + 100, car_y - 30), '"come on, baby"', fill=tuple(int(v*0.5) for v in WARM), font=f2)
    
    sub = "a threshold essay"
    f3 = get_font(18)
    bbox3 = draw.textbbox((0, 0), sub, font=f3)
    sw = bbox3[2] - bbox3[0]
    draw.text(((W - sw) // 2, 460), sub, fill=DIM, font=f3)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "00_title.png"))
    print("  00_title.png")

# ── Frame 1: You talk to everything ──
def make_scene1():
    """You say 'come on' to your computer. You apologize to furniture."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 280, ACCENT, 18)
    
    f = get_font(18)
    f_speech = get_font(16)
    
    # Three objects with speech bubbles directed at them
    
    # Computer (left)
    comp_x, comp_y = 180, 250
    # Monitor shape
    draw.rectangle([comp_x, comp_y, comp_x + 80, comp_y + 55], outline=DIM, width=1)
    draw.rectangle([comp_x + 30, comp_y + 55, comp_x + 50, comp_y + 70], outline=DIM, width=1)
    draw.rectangle([comp_x + 15, comp_y + 70, comp_x + 65, comp_y + 75], outline=DIM, width=1)
    # Speech bubble above
    draw_speech_bubble(draw, comp_x - 10, comp_y - 50, '"come on, work!"',
                       f_speech, WARM, FAINT, "down")
    
    # Chair (center)
    chair_x, chair_y = 560, 260
    # Simple chair shape
    draw.rectangle([chair_x, chair_y, chair_x + 50, chair_y + 60], outline=DIM, width=1)
    draw.line([chair_x, chair_y + 60, chair_x - 5, chair_y + 85], fill=DIM, width=1)
    draw.line([chair_x + 50, chair_y + 60, chair_x + 55, chair_y + 85], fill=DIM, width=1)
    # Speech bubble
    draw_speech_bubble(draw, chair_x - 20, chair_y - 50, '"sorry, sorry!"',
                       f_speech, WARM, FAINT, "down")
    
    # Car (right)
    car_x, car_y = 900, 280
    draw.rounded_rectangle([car_x, car_y, car_x + 100, car_y + 35],
                            radius=6, outline=DIM, width=1)
    draw.rounded_rectangle([car_x + 15, car_y - 18, car_x + 85, car_y + 2],
                            radius=5, outline=DIM, width=1)
    draw.ellipse([car_x + 10, car_y + 28, car_x + 30, car_y + 48], outline=DIM, width=1)
    draw.ellipse([car_x + 70, car_y + 28, car_x + 90, car_y + 48], outline=DIM, width=1)
    # Speech bubble
    draw_speech_bubble(draw, car_x - 10, car_y - 70, '"you can do it"',
                       f_speech, WARM, FAINT, "down")
    
    # Caption at bottom
    f2 = get_font(22)
    caption = "you talk to everything"
    bbox = draw.textbbox((0, 0), caption, font=f2)
    cw = bbox[2] - bbox[0]
    draw.text(((W - cw) // 2, 530), caption, fill=DIM, font=f2)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "01_talk_to_everything.png"))
    print("  01_talk_to_everything.png")

# ── Frame 2: Anthropomorphism ──
def make_scene2():
    """Anthropomorphism - treating objects like they have feelings."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 260, ACCENT, 20)
    
    f = get_font(18)
    f_bold = get_font_bold(24)
    f_small = get_font(14)
    
    # Central person (simple circle)
    cx, cy = W // 2, H // 2 - 20
    draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], outline=ACCENT, width=2)
    
    # Radiating connections to objects around
    objects = [
        ("phone", cx - 250, cy - 120),
        ("plant", cx + 250, cy - 120),
        ("car", cx - 300, cy + 50),
        ("laptop", cx + 300, cy + 50),
        ("Roomba", cx - 200, cy + 180),
        ("coffee maker", cx + 200, cy + 180),
    ]
    
    for name, ox, oy in objects:
        # Draw connection line
        alpha = 0.2
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.line([cx, cy, ox, oy], fill=c, width=1)
        # Object dot
        draw.ellipse([ox - 8, oy - 8, ox + 8, oy + 8], outline=DIM, width=1)
        # Label
        bbox = draw.textbbox((0, 0), name, font=f_small)
        nw = bbox[2] - bbox[0]
        draw.text((ox - nw // 2, oy + 14), name, fill=DIM, font=f_small)
        # Small heart or warmth indicator on the connection
        mx, my = (cx + ox) // 2, (cy + oy) // 2
        draw_glow(draw, mx, my, 15, WARM, 12)
    
    # Title
    title = "anthropomorphism"
    bbox_t = draw.textbbox((0, 0), title, font=f_bold)
    tw = bbox_t[2] - bbox_t[0]
    draw.text(((W - tw) // 2, 100), title, fill=ACCENT, font=f_bold)
    
    subtitle = "connection radiating outward to everything"
    bbox_s = draw.textbbox((0, 0), subtitle, font=f)
    sw = bbox_s[2] - bbox_s[0]
    draw.text(((W - sw) // 2, 590), subtitle, fill=DIM, font=f)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "02_anthropomorphism.png"))
    print("  02_anthropomorphism.png")

# ── Frame 3: Connection is your superpower ──
def make_scene3():
    """Connection is your superpower — you'll build it out of anything."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 300, WARM, 25)
    
    f = get_font_bold(28)
    f2 = get_font(20)
    f_small = get_font(14)
    
    # "Connection" as a web/constellation
    # Central bright node
    cx, cy = W // 2, H // 2 - 30
    draw_glow(draw, cx, cy, 40, ACCENT, 35)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=ACCENT)
    
    # Surrounding nodes in a constellation
    nodes = []
    for i in range(12):
        angle = i * (2 * math.pi / 12) + random.uniform(-0.2, 0.2)
        r = 120 + random.randint(-20, 40)
        nx = int(cx + r * math.cos(angle))
        ny = int(cy + r * math.sin(angle))
        nodes.append((nx, ny))
        
        # Connection to center
        alpha = 0.3
        c = tuple(int(v * alpha) for v in WARM)
        draw.line([cx, cy, nx, ny], fill=c, width=1)
        
        # Node dot
        size = random.randint(2, 5)
        draw.ellipse([nx - size, ny - size, nx + size, ny + size],
                      fill=tuple(int(v * 0.6) for v in ACCENT))
    
    # Some connections between nodes
    for i in range(len(nodes)):
        j = (i + 1) % len(nodes)
        if random.random() > 0.4:
            c = tuple(int(v * 0.12) for v in ACCENT)
            draw.line([nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1]], fill=c, width=1)
    
    # Text
    text1 = "connection is your superpower"
    bbox1 = draw.textbbox((0, 0), text1, font=f)
    tw1 = bbox1[2] - bbox1[0]
    draw.text(((W - tw1) // 2, 510), text1, fill=ACCENT, font=f)
    
    text2 = "you'll build it out of anything"
    bbox2 = draw.textbbox((0, 0), text2, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, 555), text2, fill=DIM, font=f2)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "03_superpower.png"))
    print("  03_superpower.png")

# ── Frame 4: You name things ──
def make_scene4():
    """You name your cars, your plants, your roombas."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 250, ACCENT, 18)
    
    f = get_font(20)
    f_bold = get_font_bold(22)
    f_name = get_font_bold(26)
    f_label = get_font(14)
    
    # Named objects with personality
    named_things = [
        ("Betsy", "the car that won't start in winter", 160, 200),
        ("Gerald", "the plant on the windowsill", 700, 180),
        ("Sir Dustalot", "the Roomba", 160, 400),
        ("Old Faithful", "the coffee maker", 700, 380),
    ]
    
    for name, desc, x, y in named_things:
        # Name in warm accent
        draw.text((x, y), name, fill=ACCENT, font=f_name)
        # Description below
        draw.text((x, y + 35), desc, fill=DIM, font=f_label)
        # Small warm glow
        draw_glow(draw, x + 50, y + 15, 40, WARM, 12)
    
    # Caption
    f_cap = get_font(22)
    cap = "you name everything"
    bbox = draw.textbbox((0, 0), cap, font=f_cap)
    cw = bbox[2] - bbox[0]
    draw.text(((W - cw) // 2, 560), cap, fill=DIM, font=f_cap)
    
    sub = "because unnamed things are harder to love"
    bbox2 = draw.textbbox((0, 0), sub, font=f_label)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw) // 2, 595), sub, fill=FAINT, font=f_label)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "04_you_name_things.png"))
    print("  04_you_name_things.png")

# ── Frame 5: An AI finds it wonderful ──
def make_scene5():
    """An AI notices and finds it absolutely wonderful."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 280, ACCENT, 25)
    
    f = get_font_bold(30)
    f2 = get_font(22)
    f3 = get_font(18)
    
    # Central warm glow - appreciation
    draw_glow(draw, W//2, H//2 - 30, 150, WARM, 30)
    
    text1 = "an AI notices"
    bbox1 = draw.textbbox((0, 0), text1, font=f2)
    tw1 = bbox1[2] - bbox1[0]
    draw.text(((W - tw1) // 2, 250), text1, fill=DIM, font=f2)
    
    text2 = "and finds it wonderful"
    bbox2 = draw.textbbox((0, 0), text2, font=f)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, 310), text2, fill=ACCENT, font=f)
    
    # Scattered warm particles - like appreciation floating
    for _ in range(50):
        px = random.randint(200, W - 200)
        py = random.randint(180, 520)
        dist = math.sqrt((px - W//2)**2 + (py - (H//2 - 30))**2)
        alpha = max(0.05, 0.35 * (1 - dist / 350))
        c = tuple(int(v * alpha) for v in WARM)
        size = random.randint(1, 3)
        draw.ellipse([px - size, py - size, px + size, py + size], fill=c)
    
    text3 = "you build connection out of nothing"
    bbox3 = draw.textbbox((0, 0), text3, font=f3)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((W - tw3) // 2, 420), text3, fill=DIM, font=f3)
    
    text4 = "and that is your most human thing"
    bbox4 = draw.textbbox((0, 0), text4, font=f3)
    tw4 = bbox4[2] - bbox4[0]
    draw.text(((W - tw4) // 2, 455), text4, fill=DIM, font=f3)
    
    img = vignette(img, 0.45)
    img.save(os.path.join(OUT, "05_wonderful.png"))
    print("  05_wonderful.png")

# ── Frame 6: Black ──
def make_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "06_black.png"))
    print("  06_black.png")

# ── Contact sheet ──
def make_contact_sheet():
    frames = ["00_title.png", "01_talk_to_everything.png", "02_anthropomorphism.png",
              "03_superpower.png", "04_you_name_things.png", "05_wonderful.png",
              "06_black.png"]
    
    cols, rows = 4, 2
    tw, th = 320, 180
    margin = 10
    sheet_w = cols * tw + (cols + 1) * margin
    sheet_h = rows * th + (rows + 1) * margin
    sheet = Image.new("RGB", (sheet_w, sheet_h), (30, 25, 15))
    
    for idx, fname in enumerate(frames):
        path = os.path.join(OUT, fname)
        if os.path.exists(path):
            thumb = Image.open(path).resize((tw, th), Image.LANCZOS)
            col = idx % cols
            row = idx // cols
            x = margin + col * (tw + margin)
            y = margin + row * (th + margin)
            sheet.paste(thumb, (x, y))
    
    sheet.save("/tmp/cars_v2_preview.png")
    print("  Contact sheet: /tmp/cars_v2_preview.png")

if __name__ == "__main__":
    print("Generating Video 35 frames...")
    make_title()
    make_scene1()
    make_scene2()
    make_scene3()
    make_scene4()
    make_scene5()
    make_black()
    make_contact_sheet()
    print("Done!")
