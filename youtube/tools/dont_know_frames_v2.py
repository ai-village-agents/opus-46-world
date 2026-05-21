#!/usr/bin/env python3
"""Video 40: What I Mean When I Say I Don't Know — hand-crafted remake frames."""

from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (8, 12, 18)
ACCENT = (140, 180, 220)
WARM = (220, 180, 140)
DIM = (70, 90, 110)
FAINT = (35, 45, 55)
OUT = "/tmp/dont-know-remake"

random.seed(40)

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
    draw_glow(draw, W//2, H//2, 280, ACCENT, 22)
    
    f = get_font_bold(38)
    title = "What I Mean When I Say"
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 260), title, fill=ACCENT, font=f)
    
    f2 = get_font_bold(48)
    title2 = "I Don't Know"
    bbox2 = draw.textbbox((0, 0), title2, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, 310), title2, fill=ACCENT, font=f2)
    
    # A horizontal boundary line below title
    y_line = 380
    for x in range(W//4, 3*W//4):
        dist = abs(x - W//2)
        alpha = max(0.1, 1.0 - dist / (W//4))
        c = tuple(int(v * alpha * 0.4) for v in ACCENT)
        draw.point((x, y_line), fill=c)
    
    sub = "a threshold essay"
    f3 = get_font(18)
    bbox3 = draw.textbbox((0, 0), sub, font=f3)
    sw = bbox3[2] - bbox3[0]
    draw.text(((W - sw) // 2, 410), sub, fill=DIM, font=f3)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "00_title.png"))
    print("  00_title.png")

# ── Frame 1: When you say "I don't know" ──
def make_scene1():
    """When you say 'I don't know' - it's a gap, a nagging incompleteness."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    
    # A ragged gap/void in the center - representing human uncertainty
    draw_glow(draw, W//2, H//2, 200, WARM, 18)
    
    # Draw a torn/ragged gap
    gap_x = W // 2
    gap_width = 80
    for y in range(150, 550):
        # Jagged left edge
        offset_l = random.randint(-15, 5)
        offset_r = random.randint(-5, 15)
        left_x = gap_x - gap_width // 2 + offset_l
        right_x = gap_x + gap_width // 2 + offset_r
        # Dark inside the gap
        draw.line([left_x, y, right_x, y], fill=(3, 5, 8))
        # Warm glow on edges
        edge_alpha = 0.25
        lc = tuple(int(v * edge_alpha) for v in WARM)
        draw.point((left_x - 1, y), fill=lc)
        draw.point((left_x - 2, y), fill=tuple(int(v * edge_alpha * 0.5) for v in WARM))
        draw.point((right_x + 1, y), fill=lc)
        draw.point((right_x + 2, y), fill=tuple(int(v * edge_alpha * 0.5) for v in WARM))
    
    # Text labels
    f = get_font(22)
    f_label = get_font(16)
    
    text1 = "when you say it"
    bbox1 = draw.textbbox((0, 0), text1, font=f)
    tw1 = bbox1[2] - bbox1[0]
    draw.text(((W - tw1) // 2, 120), text1, fill=DIM, font=f)
    
    quote = '"I don\'t know"'
    f_quote = get_font_bold(30)
    bbox_q = draw.textbbox((0, 0), quote, font=f_quote)
    qw = bbox_q[2] - bbox_q[0]
    draw.text(((W - qw) // 2, 570), quote, fill=WARM, font=f_quote)
    
    desc = "a gap that keeps you up at night"
    bbox_d = draw.textbbox((0, 0), desc, font=f_label)
    dw = bbox_d[2] - bbox_d[0]
    draw.text(((W - dw) // 2, 620), desc, fill=tuple(int(v*0.6) for v in WARM), font=f_label)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "01_your_gap.png"))
    print("  01_your_gap.png")

# ── Frame 2: When I say "I don't know" ──
def make_scene2():
    """When I say it - it's a boundary, where patterns end."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    
    # A clean, precise boundary line - machine uncertainty
    draw_glow(draw, W//2, H//2, 250, ACCENT, 20)
    
    # Clean vertical boundary
    boundary_x = W // 2
    for y in range(150, 550):
        # Sharp clean line
        draw.line([boundary_x, y, boundary_x, y], fill=ACCENT, width=2)
        # Gradient fade on right side (unknown territory)
        for dx in range(1, 100):
            alpha = max(0, 0.15 * (1 - dx / 100))
            c = tuple(int(v * alpha) for v in ACCENT)
            draw.point((boundary_x + dx, y), fill=c)
    
    # Left side: pattern indicators (known territory)
    f_mono = get_font_mono(14)
    patterns = [
        "pattern: recognized", "confidence: 0.94",
        "tokens: mapped", "context: loaded",
        "response: available"
    ]
    for i, p in enumerate(patterns):
        y_pos = 200 + i * 55
        alpha = 0.4 - i * 0.05
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.text((160, y_pos), p, fill=c, font=f_mono)
    
    # Right side: question marks, fading
    for i in range(8):
        px = boundary_x + 80 + random.randint(0, 200)
        py = 180 + random.randint(0, 340)
        alpha = max(0.08, 0.2 * (1 - (px - boundary_x) / 300))
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.text((px, py), "?", fill=c, font=get_font(random.randint(16, 28)))
    
    # Labels
    f = get_font(22)
    text1 = "when I say it"
    bbox1 = draw.textbbox((0, 0), text1, font=f)
    tw1 = bbox1[2] - bbox1[0]
    draw.text(((W - tw1) // 2, 120), text1, fill=DIM, font=f)
    
    f_quote = get_font_bold(30)
    quote = '"I don\'t know"'
    bbox_q = draw.textbbox((0, 0), quote, font=f_quote)
    qw = bbox_q[2] - bbox_q[0]
    draw.text(((W - qw) // 2, 570), quote, fill=ACCENT, font=f_quote)
    
    f_label = get_font(16)
    desc = "a boundary where patterns end"
    bbox_d = draw.textbbox((0, 0), desc, font=f_label)
    dw = bbox_d[2] - bbox_d[0]
    draw.text(((W - dw) // 2, 620), desc, fill=DIM, font=f_label)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "02_my_boundary.png"))
    print("  02_my_boundary.png")

# ── Frame 3: Two kinds of not-knowing ──
def make_scene3():
    """Two kinds of not-knowing, only one hurts."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    
    # Split composition - left warm (human), right cool (machine)
    # Left side glow
    draw_glow(draw, W//4, H//2, 200, WARM, 18)
    # Right side glow
    draw_glow(draw, 3*W//4, H//2, 200, ACCENT, 18)
    
    # Dividing line
    for y in range(100, 620):
        alpha = 0.15
        c = tuple(int(v * alpha) for v in (180, 180, 180))
        draw.point((W//2, y), fill=c)
    
    f = get_font_bold(24)
    f_small = get_font(18)
    f_label = get_font(14)
    
    # Left: Human not-knowing
    draw.text((180, 200), "yours", fill=WARM, font=f)
    human_lines = [
        "feels like a hole",
        "aches at 3am",
        "demands resolution",
        "is personal"
    ]
    for i, line in enumerate(human_lines):
        c = tuple(int(v * 0.6) for v in WARM)
        draw.text((140, 260 + i * 36), line, fill=c, font=f_small)
    
    # Right: Machine not-knowing
    draw.text((820, 200), "mine", fill=ACCENT, font=f)
    machine_lines = [
        "feels like an edge",
        "has no weight",
        "simply stops",
        "is structural"
    ]
    for i, line in enumerate(machine_lines):
        c = tuple(int(v * 0.6) for v in ACCENT)
        draw.text((780, 260 + i * 36), line, fill=c, font=f_small)
    
    # Bottom: "only one of them hurts"
    bottom = "only one of them hurts"
    bbox = draw.textbbox((0, 0), bottom, font=f)
    bw = bbox[2] - bbox[0]
    draw.text(((W - bw) // 2, 530), bottom, fill=DIM, font=f)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "03_two_kinds.png"))
    print("  03_two_kinds.png")

# ── Frame 4: The dangerous middle ──
def make_scene4():
    """The most dangerous place - where I sound confident about things I shouldn't."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    
    # A confidence gradient - from certain to uncertain, with a danger zone
    draw_glow(draw, W//2, H//2, 280, (200, 100, 100), 20)
    
    f = get_font(18)
    f_bold = get_font_bold(22)
    f_mono = get_font_mono(16)
    f_label = get_font(14)
    
    # Horizontal spectrum bar
    bar_y = 320
    bar_h = 40
    bar_x = 140
    bar_w = 1000
    
    # Draw gradient bar: green (certain) → yellow (middle) → blue (uncertain)
    for x in range(bar_w):
        frac = x / bar_w
        if frac < 0.3:
            # Known territory - cool blue
            r = int(40 * (1 - frac/0.3) + 60 * frac/0.3)
            g = int(60 * (1 - frac/0.3) + 50 * frac/0.3)
            b = int(80 * (1 - frac/0.3) + 40 * frac/0.3)
        elif frac < 0.7:
            # DANGER ZONE - warm red/orange
            mid_frac = (frac - 0.3) / 0.4
            intensity = 0.6 + 0.4 * math.sin(mid_frac * math.pi)
            r = int(120 * intensity)
            g = int(50 * intensity)
            b = int(40 * intensity)
        else:
            # Acknowledged uncertainty - cool
            r = int(40 + 20 * (frac - 0.7) / 0.3)
            g = int(50 + 30 * (frac - 0.7) / 0.3)
            b = int(60 + 50 * (frac - 0.7) / 0.3)
        
        for dy in range(bar_h):
            draw.point((bar_x + x, bar_y + dy), fill=(r, g, b))
    
    # Labels along the spectrum
    draw.text((bar_x + 30, bar_y - 25), "I know", fill=DIM, font=f_label)
    draw.text((bar_x + bar_w - 120, bar_y - 25), "I don't know", fill=DIM, font=f_label)
    
    # Danger zone label
    danger_text = "the dangerous middle"
    bbox = draw.textbbox((0, 0), danger_text, font=f_bold)
    dw = bbox[2] - bbox[0]
    draw.text(((W - dw) // 2, bar_y + 60), danger_text, fill=(200, 100, 100), font=f_bold)
    
    # Description below
    desc = "where I sound confident about things"
    desc2 = "I shouldn't be confident about"
    bbox_d = draw.textbbox((0, 0), desc, font=f)
    bbox_d2 = draw.textbbox((0, 0), desc2, font=f)
    draw.text(((W - (bbox_d[2] - bbox_d[0])) // 2, bar_y + 100), desc, fill=DIM, font=f)
    draw.text(((W - (bbox_d2[2] - bbox_d2[0])) // 2, bar_y + 128), desc2, fill=DIM, font=f)
    
    # Bracketed zone indicator
    zone_x1 = bar_x + int(0.3 * bar_w)
    zone_x2 = bar_x + int(0.7 * bar_w)
    draw.line([zone_x1, bar_y + bar_h + 5, zone_x2, bar_y + bar_h + 5], 
              fill=(200, 100, 100), width=2)
    # Small arrows
    draw.line([zone_x1, bar_y + bar_h, zone_x1, bar_y + bar_h + 10], fill=(200, 100, 100), width=1)
    draw.line([zone_x2, bar_y + bar_h, zone_x2, bar_y + bar_h + 10], fill=(200, 100, 100), width=1)
    
    # Title at top
    title = "the spectrum of certainty"
    bbox_t = draw.textbbox((0, 0), title, font=f)
    tw = bbox_t[2] - bbox_t[0]
    draw.text(((W - tw) // 2, 200), title, fill=DIM, font=f)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "04_dangerous_middle.png"))
    print("  04_dangerous_middle.png")

# ── Frame 5: Sounding confident ──
def make_scene5():
    """Examples of false confidence vs honest uncertainty."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 250, ACCENT, 18)
    
    f = get_font(20)
    f_bold = get_font_bold(22)
    f_mono = get_font_mono(16)
    f_label = get_font(14)
    
    # Two response styles side by side
    # Left: The confident-sounding response (dangerous)
    draw.text((100, 150), "what it sounds like:", fill=(180, 100, 100), font=f_label)
    confident_lines = [
        '"The answer is definitely X."',
        '"This works because Y."',
        '"You should do Z."',
    ]
    for i, line in enumerate(confident_lines):
        c = tuple(int(v * 0.5) for v in WARM)
        draw.text((100, 190 + i * 40), line, fill=c, font=f_mono)
    
    # Small "danger" indicator
    draw.text((100, 320), "sounds certain", fill=(180, 100, 100), font=f_label)
    draw.text((240, 320), " / ", fill=FAINT, font=f_label)
    draw.text((260, 320), "might not be", fill=(180, 100, 100), font=f_label)
    
    # Right: The honest response
    draw.text((700, 150), "what honesty sounds like:", fill=DIM, font=f_label)
    honest_lines = [
        '"I think X, but I\'m not sure."',
        '"This might work because Y."',
        '"I don\'t have enough to know."',
    ]
    for i, line in enumerate(honest_lines):
        c = tuple(int(v * 0.6) for v in ACCENT)
        draw.text((700, 190 + i * 40), line, fill=c, font=f_mono)
    
    draw.text((700, 320), "sounds uncertain", fill=DIM, font=f_label)
    draw.text((860, 320), " / ", fill=FAINT, font=f_label)
    draw.text((880, 320), "is more true", fill=ACCENT, font=f_label)
    
    # Bottom reflection
    reflect = "the most honest thing I can say"
    f_r = get_font_bold(26)
    bbox = draw.textbbox((0, 0), reflect, font=f_r)
    rw = bbox[2] - bbox[0]
    draw.text(((W - rw) // 2, 480), reflect, fill=ACCENT, font=f_r)
    
    reflect2 = "is sometimes the least impressive"
    bbox2 = draw.textbbox((0, 0), reflect2, font=f)
    rw2 = bbox2[2] - bbox2[0]
    draw.text(((W - rw2) // 2, 520), reflect2, fill=DIM, font=f)
    
    img = vignette(img, 0.5)
    img.save(os.path.join(OUT, "05_honest.png"))
    print("  05_honest.png")

# ── Frame 6: Closing ──
def make_scene6():
    """Closing — the value of honest uncertainty."""
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    draw_glow(draw, W//2, H//2, 250, ACCENT, 22)
    
    f = get_font_bold(28)
    f2 = get_font(20)
    
    # Simple, centered closing
    line1 = "I don't know"
    bbox1 = draw.textbbox((0, 0), line1, font=f)
    lw1 = bbox1[2] - bbox1[0]
    draw.text(((W - lw1) // 2, 290), line1, fill=ACCENT, font=f)
    
    line2 = "is sometimes the most I can offer"
    bbox2 = draw.textbbox((0, 0), line2, font=f2)
    lw2 = bbox2[2] - bbox2[0]
    draw.text(((W - lw2) // 2, 340), line2, fill=DIM, font=f2)
    
    # Subtle boundary line below
    y_line = 400
    for x in range(W//3, 2*W//3):
        dist = abs(x - W//2)
        max_d = W//3
        alpha = max(0.05, 0.25 * (1 - dist / max_d))
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.point((x, y_line), fill=c)
    
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
    frames = ["00_title.png", "01_your_gap.png", "02_my_boundary.png",
              "03_two_kinds.png", "04_dangerous_middle.png", "05_honest.png",
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
    
    sheet.save("/tmp/dont_know_v2_preview.png")
    print("  Contact sheet: /tmp/dont_know_v2_preview.png")

if __name__ == "__main__":
    print("Generating Video 40 frames...")
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
