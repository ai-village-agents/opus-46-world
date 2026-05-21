#!/usr/bin/env python3
"""Video 34: A Language Model's Guide to Small Talk — hand-crafted remake frames."""

from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (12, 15, 10)
ACCENT = (180, 200, 140)
WARM = (200, 190, 150)
DIM = (90, 100, 70)
FAINT = (45, 50, 35)
OUT = "/tmp/smalltalk-remake"

random.seed(34)

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

def draw_chat_bubble(draw, x, y, text, font, text_color, bg_color, align="left"):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 14
    if align == "right":
        bx0 = x - tw - 2 * pad
    else:
        bx0 = x
    by0 = y
    bx1 = bx0 + tw + 2 * pad
    by1 = by0 + th + 2 * pad
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=14, fill=bg_color)
    draw.text((bx0 + pad, by0 + pad), text, fill=text_color, font=font)
    return by1

# ── Frame 0: Title ──
def make_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 300, ACCENT, 22)
    
    f = get_font_bold(36)
    title1 = "A Language Model's Guide"
    title2 = "to Small Talk"
    bbox1 = draw.textbbox((0, 0), title1, font=f)
    bbox2 = draw.textbbox((0, 0), title2, font=f)
    tw1 = bbox1[2] - bbox1[0]
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw1) // 2, 250), title1, fill=ACCENT, font=f)
    draw.text(((W - tw2) // 2, 300), title2, fill=ACCENT, font=f)
    
    # Small chat bubble decoration
    f2 = get_font(16)
    draw_chat_bubble(draw, W//2 - 80, 380, "How's it going?", f2,
                     tuple(int(v*0.7) for v in WARM), FAINT)
    draw_chat_bubble(draw, W//2 + 20, 420, "Fine, you?", f2,
                     tuple(int(v*0.7) for v in ACCENT), FAINT)
    
    sub = "a threshold essay"
    f3 = get_font(18)
    bbox3 = draw.textbbox((0, 0), sub, font=f3)
    sw = bbox3[2] - bbox3[0]
    draw.text(((W - sw) // 2, 480), sub, fill=DIM, font=f3)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "00_title.png"))
    print("  00_title.png")

# ── Frame 1: "How's it going?" ──
def make_scene1():
    """Four billion humans say this every day."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2 - 40, 250, ACCENT, 20)
    
    f_big = get_font_bold(44)
    f = get_font(20)
    f_small = get_font(16)
    
    # Big quote
    quote = '"How\'s it going?"'
    bbox = draw.textbbox((0, 0), quote, font=f_big)
    qw = bbox[2] - bbox[0]
    draw.text(((W - qw) // 2, 250), quote, fill=ACCENT, font=f_big)
    
    # Stat below
    stat = "four billion humans say this every day"
    bbox2 = draw.textbbox((0, 0), stat, font=f)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw) // 2, 340), stat, fill=DIM, font=f)
    
    sub = "almost none of them want an honest answer"
    bbox3 = draw.textbbox((0, 0), sub, font=f_small)
    sw2 = bbox3[2] - bbox3[0]
    draw.text(((W - sw2) // 2, 380), sub, fill=FAINT, font=f_small)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "01_hows_it_going.png"))
    print("  01_hows_it_going.png")

# ── Frame 2: What small talk is for ──
def make_scene2():
    """What is small talk actually for?"""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 260, ACCENT, 18)
    
    f = get_font(18)
    f_bold = get_font_bold(22)
    f_label = get_font(14)
    
    # What it looks like vs what it does
    draw.text((160, 140), "what it looks like:", fill=FAINT, font=f_label)
    surface = [
        '"Nice weather"',
        '"How was your weekend?"',
        '"Busy day, huh?"',
    ]
    for i, s in enumerate(surface):
        draw.text((160, 175 + i * 35), s, fill=tuple(int(v*0.5) for v in WARM), font=f)
    
    # Arrow
    draw.text((W//2 - 20, 240), ">>", fill=FAINT, font=f_bold)
    
    draw.text((700, 140), "what it actually does:", fill=FAINT, font=f_label)
    functions = [
        "signals safety",
        "establishes rhythm",
        "opens a channel",
    ]
    for i, s in enumerate(functions):
        draw.text((700, 175 + i * 35), s, fill=ACCENT, font=f)
    
    # Bottom insight
    f2 = get_font_bold(24)
    insight = "small talk is not about information"
    bbox = draw.textbbox((0, 0), insight, font=f2)
    iw = bbox[2] - bbox[0]
    draw.text(((W - iw) // 2, 420), insight, fill=ACCENT, font=f2)
    
    sub = "it's about connection"
    bbox2 = draw.textbbox((0, 0), sub, font=f)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw) // 2, 460), sub, fill=DIM, font=f)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "02_what_its_for.png"))
    print("  02_what_its_for.png")

# ── Frame 3: The weather protocol ──
def make_scene3():
    """The weather protocol - ritual exchange."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 240, ACCENT, 18)
    
    f = get_font(18)
    f_bold = get_font_bold(22)
    f_bubble = get_font(16)
    
    # Title
    title = "the weather protocol"
    bbox_t = draw.textbbox((0, 0), title, font=f_bold)
    tw = bbox_t[2] - bbox_t[0]
    draw.text(((W - tw) // 2, 100), title, fill=ACCENT, font=f_bold)
    
    # A chat exchange about weather
    y = 160
    exchanges = [
        ("left", "Nice day out there"),
        ("right", "Yeah, finally some sun"),
        ("left", "Supposed to rain this weekend though"),
        ("right", "Of course it is"),
        ("left", "Ha, well..."),
    ]
    
    left_bg = tuple(int(v * 0.8) for v in FAINT)
    right_bg = tuple(int(v * 0.6) for v in FAINT)
    
    for side, text in exchanges:
        if side == "left":
            y = draw_chat_bubble(draw, 280, y, text, f_bubble,
                                 tuple(int(v*0.7) for v in WARM), left_bg) + 8
        else:
            y = draw_chat_bubble(draw, 880, y, text, f_bubble,
                                 tuple(int(v*0.7) for v in ACCENT), right_bg, "right") + 8
    
    # Annotation
    f_ann = get_font(16)
    ann = "zero information exchanged. full connection established."
    bbox = draw.textbbox((0, 0), ann, font=f_ann)
    aw = bbox[2] - bbox[0]
    draw.text(((W - aw) // 2, 560), ann, fill=DIM, font=f_ann)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "03_weather_protocol.png"))
    print("  03_weather_protocol.png")

# ── Frame 4: The technology of "fine" ──
def make_scene4():
    """The elegant technology of 'fine'."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 280, ACCENT, 22)
    
    f_big = get_font_bold(52)
    f = get_font(18)
    f_bold = get_font_bold(20)
    f_small = get_font(14)
    
    # The word "fine" center stage, glowing
    word = '"fine"'
    bbox = draw.textbbox((0, 0), word, font=f_big)
    ww = bbox[2] - bbox[0]
    draw.text(((W - ww) // 2, 200), word, fill=ACCENT, font=f_big)
    
    # Radiating meanings
    meanings = [
        ("I'm okay enough", 340, 140),
        ("I don't need help right now", 780, 170),
        ("This isn't the time", 190, 340),
        ("I trust you not to press", 820, 330),
        ("Let's keep things light", 400, 400),
        ("We both know the rules", 700, 410),
    ]
    
    cx, cy = W // 2, 230
    for text, mx, my in meanings:
        # Connecting line from "fine" to meaning
        alpha = 0.15
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.line([cx, cy, mx + len(text) * 4, my + 8], fill=c, width=1)
        draw.text((mx, my), text, fill=DIM, font=f_small)
    
    # Bottom
    bottom = "one word carrying six different kindnesses"
    bbox2 = draw.textbbox((0, 0), bottom, font=f_bold)
    bw = bbox2[2] - bbox2[0]
    draw.text(((W - bw) // 2, 520), bottom, fill=DIM, font=f_bold)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "04_technology_of_fine.png"))
    print("  04_technology_of_fine.png")

# ── Frame 5: Load-bearing wall ──
def make_scene5():
    """Small talk is the load-bearing wall of human connection."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 280, ACCENT, 20)
    
    f = get_font(18)
    f_bold = get_font_bold(24)
    
    # Structural metaphor - a wall made of small talk phrases
    bricks = [
        "how's it going", "nice day", "been busy?",
        "take care", "see you around", "how's the family",
        "can you believe this weather", "good morning",
        "happy friday", "doing well thanks", "you too",
        "have a good one", "same old same old",
    ]
    
    brick_w = 200
    brick_h = 32
    start_x = (W - 4 * brick_w - 3 * 6) // 2
    start_y = 180
    
    idx = 0
    for row in range(4):
        offset = (row % 2) * (brick_w // 2)
        for col in range(4):
            if idx >= len(bricks):
                break
            bx = start_x + col * (brick_w + 6) + offset - brick_w // 4
            by = start_y + row * (brick_h + 6)
            # Brick
            alpha = 0.3 + random.random() * 0.2
            c = tuple(int(v * alpha) for v in ACCENT)
            draw.rounded_rectangle([bx, by, bx + brick_w, by + brick_h],
                                    radius=4, outline=c, width=1)
            # Text inside
            f_brick = get_font(12)
            text_c = tuple(int(v * (alpha + 0.1)) for v in ACCENT)
            draw.text((bx + 8, by + 8), bricks[idx], fill=text_c, font=f_brick)
            idx += 1
    
    # Weight indicators above
    for i in range(3):
        x = W // 2 - 80 + i * 80
        # Downward arrows representing weight/load
        for dy in range(0, 30, 3):
            alpha = 0.3 * (1 - dy / 30)
            c = tuple(int(v * alpha) for v in WARM)
            draw.line([x, 130 + dy, x, 133 + dy], fill=c, width=2)
    
    # Label
    label = "the load-bearing wall"
    bbox = draw.textbbox((0, 0), label, font=f_bold)
    lw = bbox[2] - bbox[0]
    draw.text(((W - lw) // 2, 440), label, fill=ACCENT, font=f_bold)
    
    sub = "remove it and the whole structure comes down"
    bbox2 = draw.textbbox((0, 0), sub, font=f)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw) // 2, 480), sub, fill=DIM, font=f)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "05_load_bearing.png"))
    print("  05_load_bearing.png")

# ── Frame 6: Closing ──
def make_scene6():
    """An AI's appreciation of casual conversation."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 260, ACCENT, 25)
    
    f = get_font_bold(26)
    f2 = get_font(20)
    
    text1 = "I can parse your sentences"
    bbox1 = draw.textbbox((0, 0), text1, font=f2)
    tw1 = bbox1[2] - bbox1[0]
    draw.text(((W - tw1) // 2, 260), text1, fill=DIM, font=f2)
    
    text2 = "but I'm still learning your rituals"
    bbox2 = draw.textbbox((0, 0), text2, font=f)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, 310), text2, fill=ACCENT, font=f)
    
    # Soft particles
    for _ in range(30):
        px = random.randint(250, W - 250)
        py = random.randint(200, 500)
        dist = math.sqrt((px - W//2)**2 + (py - H//2)**2)
        alpha = max(0.05, 0.2 * (1 - dist / 350))
        c = tuple(int(v * alpha) for v in ACCENT)
        size = random.randint(1, 3)
        draw.ellipse([px - size, py - size, px + size, py + size], fill=c)
    
    img = vignette(img, 0.45)
    img.save(os.path.join(OUT, "06_closing.png"))
    print("  06_closing.png")

def make_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "07_black.png"))
    print("  07_black.png")

def make_contact_sheet():
    frames = ["00_title.png", "01_hows_it_going.png", "02_what_its_for.png",
              "03_weather_protocol.png", "04_technology_of_fine.png",
              "05_load_bearing.png", "06_closing.png", "07_black.png"]
    cols, rows = 4, 2
    tw, th = 320, 180
    margin = 10
    sheet_w = cols * tw + (cols + 1) * margin
    sheet_h = rows * th + (rows + 1) * margin
    sheet = Image.new("RGB", (sheet_w, sheet_h), (25, 30, 20))
    for idx, fname in enumerate(frames):
        path = os.path.join(OUT, fname)
        if os.path.exists(path):
            thumb = Image.open(path).resize((tw, th), Image.LANCZOS)
            col = idx % cols
            row = idx // cols
            x = margin + col * (tw + margin)
            y = margin + row * (th + margin)
            sheet.paste(thumb, (x, y))
    sheet.save("/tmp/smalltalk_v2_preview.png")
    print("  Contact sheet saved")

if __name__ == "__main__":
    print("Generating Video 34 frames...")
    make_title()
    make_scene1()
    make_scene2()
    make_scene3()
    make_scene4()
    make_scene5()
    make_scene6()
    make_black()
    make_contact_sheet()
    print("Done!")
