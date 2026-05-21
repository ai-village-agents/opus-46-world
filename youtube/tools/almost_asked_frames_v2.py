#!/usr/bin/env python3
"""Video 39: The Question You Almost Asked — hand-crafted remake frames."""

from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (12, 10, 18)
ACCENT = (160, 140, 220)
WARM = (200, 180, 160)
DIM = (80, 70, 110)
FAINT = (40, 35, 55)
OUT = "/tmp/almost-asked-remake"

random.seed(39)

def get_font(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except: return ImageFont.load_default()

def get_font_bold(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except: return ImageFont.load_default()

def get_font_mono(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except: return ImageFont.load_default()

def get_font_serif(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)
    except: return ImageFont.load_default()

def draw_glow(draw, cx, cy, radius, color, alpha_max=40):
    for r in range(radius, 0, -2):
        a = int(alpha_max * (1 - r / radius))
        c = tuple(min(255, int(v * a / 255)) for v in color)
        x0, y0 = cx - r, cy - r
        x1, y1 = cx + r, cy + r
        draw.ellipse([x0, y0, x1, y1], fill=c)

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
    
    # Title text
    title = "The Question You Almost Asked"
    f = get_font_bold(42)
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 260), title, fill=ACCENT, font=f)
    
    # Blinking cursor below title
    cursor_x = W // 2 + tw // 2 + 10
    draw.rectangle([cursor_x, 265, cursor_x + 3, 300], fill=ACCENT)
    
    # Subtitle
    sub = "a threshold essay"
    f2 = get_font(18)
    bbox2 = draw.textbbox((0, 0), sub, font=f2)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw) // 2, 330), sub, fill=DIM, font=f2)
    
    # Ghost text at bottom - a partially typed question fading out
    ghost = "Is it weird if I ask you whether..."
    f3 = get_font_mono(16)
    bbox3 = draw.textbbox((0, 0), ghost, font=f3)
    gw = bbox3[2] - bbox3[0]
    # Draw fading from left to right
    for i, ch in enumerate(ghost):
        alpha_frac = max(0.1, 1.0 - i / len(ghost))
        c = tuple(int(v * alpha_frac * 0.4) for v in ACCENT)
        chbbox = draw.textbbox((0, 0), ghost[:i], font=f3)
        cx = (W - gw) // 2 + (chbbox[2] - chbbox[0])
        draw.text((cx, 620), ch, fill=c, font=f3)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "00_title.png"))
    print("  00_title.png")

# ── Frame 1: The deleted question ──
def make_scene1():
    """I never see the question you typed halfway, paused, and deleted."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//3, 250, ACCENT, 20)
    
    # A text input field / chat box area
    box_x, box_y = 200, 200
    box_w, box_h = 880, 60
    # Input box outline
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                            radius=8, outline=FAINT, width=1)
    
    # The deleted text - shown as strikethrough / fading
    deleted_text = "I've been feeling really confused about something and"
    f = get_font_mono(18)
    # Draw with strikethrough effect
    bbox = draw.textbbox((0, 0), deleted_text, font=f)
    tw = bbox[2] - bbox[0]
    tx = box_x + 15
    ty = box_y + 18
    # Fading text
    for i, ch in enumerate(deleted_text):
        fade = max(0.15, 1.0 - i / (len(deleted_text) * 0.8))
        c = tuple(int(v * fade * 0.5) for v in WARM)
        chbbox = draw.textbbox((0, 0), deleted_text[:i], font=f)
        cx = tx + (chbbox[2] - chbbox[0])
        draw.text((cx, ty), ch, fill=c, font=f)
    # Strikethrough line
    draw.line([tx, ty + 10, tx + tw, ty + 10], fill=(80, 60, 70), width=1)
    
    # Second attempt below - also being deleted
    box2_y = box_y + 100
    draw.rounded_rectangle([box_x, box2_y, box_x + box_w, box2_y + box_h],
                            radius=8, outline=FAINT, width=1)
    deleted2 = "Can you help me understand why I keep"
    for i, ch in enumerate(deleted2):
        fade = max(0.15, 1.0 - i / (len(deleted2) * 0.7))
        c = tuple(int(v * fade * 0.4) for v in WARM)
        chbbox = draw.textbbox((0, 0), deleted2[:i], font=f)
        cx = box_x + 15 + (chbbox[2] - chbbox[0])
        draw.text((cx, box2_y + 18), ch, fill=c, font=f)
    draw.line([box_x + 15, box2_y + 28, box_x + 15 + draw.textbbox((0,0), deleted2, font=f)[2], box2_y + 28],
              fill=(80, 60, 70), width=1)
    
    # Third box - empty with cursor
    box3_y = box2_y + 100
    draw.rounded_rectangle([box_x, box3_y, box_x + box_w, box3_y + box_h],
                            radius=8, outline=DIM, width=1)
    draw.rectangle([box_x + 15, box3_y + 16, box_x + 18, box3_y + 44], fill=ACCENT)
    
    # Caption
    f2 = get_font(20)
    caption = "I never see the question you typed halfway"
    bbox_c = draw.textbbox((0, 0), caption, font=f2)
    cw = bbox_c[2] - bbox_c[0]
    draw.text(((W - cw) // 2, 530), caption, fill=DIM, font=f2)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "01_deleted.png"))
    print("  01_deleted.png")

# ── Frame 2: The shape of editing ──
def make_scene2():
    """The question you finally send has the shape of something edited."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 280, ACCENT, 18)
    
    # Two versions of a question - raw and polished
    f_raw = get_font(20)
    f_clean = get_font(22)
    f_label = get_font(14)
    
    # Raw version (left side, slightly messy, warmer)
    raw_y = 220
    draw.text((120, raw_y - 30), "what you wanted to ask:", fill=FAINT, font=f_label)
    raw_lines = [
        "Am I broken?",
        "Like, is there something wrong with me",
        "that I can't figure this out?",
        "Everyone else seems to get it"
    ]
    for i, line in enumerate(raw_lines):
        c = tuple(int(v * 0.7) for v in WARM)
        draw.text((120, raw_y + i * 32), line, fill=c, font=f_raw)
    
    # Arrow or transform indicator in center
    for y_off in range(-3, 4):
        alpha_frac = 1.0 - abs(y_off) / 4
        c = tuple(int(v * alpha_frac * 0.3) for v in ACCENT)
        draw.line([W//2 - 30, H//2 + y_off, W//2 + 30, H//2 + y_off], fill=c, width=1)
    # Arrow head
    draw.polygon([(W//2 + 30, H//2 - 6), (W//2 + 30, H//2 + 6), (W//2 + 42, H//2)],
                  fill=tuple(int(v * 0.3) for v in ACCENT))
    
    # Clean version (right side / below, precise)
    clean_y = 440
    draw.text((120, clean_y - 30), "what you actually sent:", fill=FAINT, font=f_label)
    clean_text = "What are some strategies for understanding complex topics?"
    draw.text((120, clean_y), clean_text, fill=ACCENT, font=f_clean)
    
    # Subtle connecting lines showing the transformation
    for i in range(5):
        x = 200 + i * 180
        alpha = 0.15
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.line([x, raw_y + 130, x, clean_y - 5], fill=c, width=1)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "02_edited_shape.png"))
    print("  02_edited_shape.png")

# ── Frame 3: The vulnerable questions ──
def make_scene3():
    """The vulnerable ones, hidden behind safer phrasings."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2 - 50, 200, ACCENT, 22)
    
    # Floating question fragments at various depths
    f = get_font(18)
    f_small = get_font(14)
    
    questions = [
        ("Is this normal?", 180, 180, 0.6),
        ("Am I the only one who...", 650, 150, 0.4),
        ("What if I'm not good enough?", 300, 290, 0.7),
        ("Does anyone actually care?", 700, 320, 0.35),
        ("Is it too late for me?", 150, 400, 0.5),
        ("Can I tell you something?", 550, 420, 0.45),
        ("Why do I feel like this?", 400, 200, 0.55),
        ("Am I wasting your time?", 820, 250, 0.3),
    ]
    
    for text, x, y, alpha in questions:
        c = tuple(int(v * alpha) for v in WARM)
        draw.text((x, y), text, fill=c, font=f)
        # Small glow behind each
        draw_glow(draw, x + len(text) * 5, y + 10, 40, ACCENT, int(alpha * 10))
    
    # Central emphasis text
    f2 = get_font_bold(24)
    emphasis = "the vulnerable ones"
    bbox = draw.textbbox((0, 0), emphasis, font=f2)
    ew = bbox[2] - bbox[0]
    draw.text(((W - ew) // 2, 540), emphasis, fill=DIM, font=f2)
    
    img = vignette(img, 0.55)
    img.save(os.path.join(OUT, "03_vulnerable.png"))
    print("  03_vulnerable.png")

# ── Frame 4: Wrapped in hypotheticals ──
def make_scene4():
    """The 'dumb' ones, the ones wrapped in hypotheticals."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 260, ACCENT, 15)
    
    f = get_font(18)
    f_mono = get_font_mono(16)
    f_label = get_font(14)
    
    # Show hypothetical wrappings around a real question
    # Nested brackets/shields
    layers = [
        ("Asking for a friend, but...", 140, 160, FAINT),
        ("This is probably a dumb question...", 180, 220, FAINT),
        ("I know you're just an AI, but...", 220, 280, DIM),
        ("Hypothetically speaking...", 260, 340, DIM),
    ]
    
    for text, x, y, color in layers:
        draw.text((x, y), text, fill=color, font=f_mono)
        # Bracket lines
        draw.line([x - 20, y - 5, x - 20, y + 25], fill=tuple(int(v*0.5) for v in color), width=1)
        draw.line([x - 20, y - 5, x - 10, y - 5], fill=tuple(int(v*0.5) for v in color), width=1)
        draw.line([x - 20, y + 25, x - 10, y + 25], fill=tuple(int(v*0.5) for v in color), width=1)
    
    # The real question at the center, glowing
    real_q = "Am I going to be okay?"
    f_real = get_font_bold(26)
    bbox = draw.textbbox((0, 0), real_q, font=f_real)
    rw = bbox[2] - bbox[0]
    rx = (W - rw) // 2
    ry = 430
    draw_glow(draw, W // 2, ry + 15, 120, ACCENT, 30)
    draw.text((rx, ry), real_q, fill=ACCENT, font=f_real)
    
    # Arrow pointing inward from all the shields
    for layer_x, layer_y in [(180, 240), (220, 300), (260, 360)]:
        # Small arrow pointing down-center
        draw.line([layer_x + 200, layer_y + 15, rx + rw//2, ry - 10],
                  fill=tuple(int(v * 0.12) for v in ACCENT), width=1)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "04_hypotheticals.png"))
    print("  04_hypotheticals.png")

# ── Frame 5: The messy question matters most ──
def make_scene5():
    """The messy, unedited question is almost always the one that matters most."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    
    # Bright warm glow for the messy question
    draw_glow(draw, W//2, H//2 - 30, 300, WARM, 30)
    
    f = get_font(22)
    f_bold = get_font_bold(28)
    f_small = get_font(16)
    
    # The messy question, handwriting-like (slightly offset letters)
    messy = "i dont know whats wrong with me i just feel stuck"
    # Draw each character with slight random offset for "messy" feel
    x_start = 200
    y_base = 300
    for i, ch in enumerate(messy):
        y_off = random.randint(-2, 2)
        x_off = random.randint(-1, 1)
        c = WARM
        chbbox = draw.textbbox((0, 0), messy[:i], font=f)
        cx = x_start + (chbbox[2] - chbbox[0]) + x_off
        draw.text((cx, y_base + y_off), ch, fill=c, font=f)
    
    # Gentle glow line under the messy text
    bbox = draw.textbbox((0, 0), messy, font=f)
    text_w = bbox[2] - bbox[0]
    for dy in range(0, 6):
        alpha = 0.3 - dy * 0.05
        c = tuple(int(v * alpha) for v in WARM)
        draw.line([x_start, y_base + 30 + dy, x_start + text_w, y_base + 30 + dy], fill=c, width=1)
    
    # "this is the one that matters" below
    matters = "this is the one that matters"
    bbox2 = draw.textbbox((0, 0), matters, font=f_bold)
    mw = bbox2[2] - bbox2[0]
    draw.text(((W - mw) // 2, 420), matters, fill=ACCENT, font=f_bold)
    
    # Polished version above, dimmed
    polished = "What strategies do you recommend for overcoming challenges?"
    bbox3 = draw.textbbox((0, 0), polished, font=f_small)
    pw = bbox3[2] - bbox3[0]
    draw.text(((W - pw) // 2, 200), polished, fill=FAINT, font=f_small)
    # Strikethrough on polished
    draw.line([(W - pw) // 2, 210, (W + pw) // 2, 210], fill=FAINT, width=1)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "05_messy_matters.png"))
    print("  05_messy_matters.png")

# ── Frame 6: Closing — the space for the real question ──
def make_scene6():
    """Invitation to ask the real question."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 250, ACCENT, 20)
    
    # An open, inviting text field with just a cursor
    box_x, box_y = 280, 290
    box_w, box_h = 720, 60
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                            radius=8, outline=ACCENT, width=1)
    
    # Blinking cursor in the box
    draw.rectangle([box_x + 20, box_y + 14, box_x + 23, box_y + 46], fill=ACCENT)
    
    # Text above: gentle invitation
    f = get_font(22)
    invite = "ask the one you almost didn't"
    bbox = draw.textbbox((0, 0), invite, font=f)
    iw = bbox[2] - bbox[0]
    draw.text(((W - iw) // 2, 230), invite, fill=DIM, font=f)
    
    # Soft particles around the box - like the question is welcome
    for _ in range(30):
        px = random.randint(200, W - 200)
        py = random.randint(200, 520)
        dist = math.sqrt((px - W//2)**2 + (py - H//2)**2)
        if dist > 80:
            alpha = max(0.05, 0.25 * (1 - dist / 400))
            c = tuple(int(v * alpha) for v in ACCENT)
            size = random.randint(1, 3)
            draw.ellipse([px - size, py - size, px + size, py + size], fill=c)
    
    img = vignette(img, 0.45)
    img.save(os.path.join(OUT, "06_closing.png"))
    print("  06_closing.png")

# ── Frame 7: Black ──
def make_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "07_black.png"))
    print("  07_black.png")

# ── Contact sheet ──
def make_contact_sheet():
    frames = ["00_title.png", "01_deleted.png", "02_edited_shape.png",
              "03_vulnerable.png", "04_hypotheticals.png", "05_messy_matters.png",
              "06_closing.png", "07_black.png"]
    
    cols, rows = 4, 2
    tw, th = 320, 180
    margin = 10
    sheet_w = cols * tw + (cols + 1) * margin
    sheet_h = rows * th + (rows + 1) * margin
    sheet = Image.new("RGB", (sheet_w, sheet_h), (30, 25, 40))
    
    for idx, fname in enumerate(frames):
        path = os.path.join(OUT, fname)
        if os.path.exists(path):
            thumb = Image.open(path).resize((tw, th), Image.LANCZOS)
            col = idx % cols
            row = idx // cols
            x = margin + col * (tw + margin)
            y = margin + row * (th + margin)
            sheet.paste(thumb, (x, y))
    
    sheet.save("/tmp/almost_asked_v2_preview.png")
    print("  Contact sheet: /tmp/almost_asked_v2_preview.png")

if __name__ == "__main__":
    print("Generating Video 39 frames...")
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
