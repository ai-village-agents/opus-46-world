from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (10, 12, 18)  # Cool dark blue-grey
ACCENT = (180, 160, 220)  # Soft lavender
WARM = (200, 170, 120)  # Warm amber (for human side)
COOL = (100, 120, 180)  # Cool blue (for AI side)

def get_font(size, bold=False, serif=False, mono=False):
    if mono:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    elif serif:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)

def draw_glow(draw, cx, cy, radius, color, alpha_max=40):
    for r in range(radius, 0, -2):
        a = int(alpha_max * (1 - r/radius)**0.5)
        c = (color[0], color[1], color[2], a)
        x0, y0, x1, y1 = cx-r, cy-r, cx+r, cy+r
        if y1 >= y0:
            draw.ellipse([x0, y0, x1, y1], fill=c)

def make_vignette(img, strength=80):
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for i in range(min(W, H)//2):
        a = int(strength * (i / (min(W, H)//2))**2)
        draw.rectangle([i, i, W-1-i, H-1-i], outline=(0,0,0,a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

# === FRAME 0: Title ===
def make_title():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Browser tab shape at top
    tab_x, tab_y = W//2 - 120, 80
    tab_w, tab_h = 240, 35
    # Tab body
    draw.rounded_rectangle([tab_x, tab_y, tab_x+tab_w, tab_y+tab_h], 
                          radius=8, fill=(40, 44, 55, 180))
    # X button on tab
    xb_x = tab_x + tab_w - 25
    xb_y = tab_y + 10
    draw.line([(xb_x, xb_y), (xb_x+14, xb_y+14)], fill=(200, 100, 100, 200), width=2)
    draw.line([(xb_x+14, xb_y), (xb_x, xb_y+14)], fill=(200, 100, 100, 200), width=2)
    # Tab text
    tab_font = get_font(13)
    draw.text((tab_x + 12, tab_y + 9), "conversation — AI", 
              fill=(180, 180, 190, 180), font=tab_font)
    
    # Soft glow below tab
    draw_glow(draw, W//2, H//2 + 20, 280, ACCENT, alpha_max=25)
    
    # Title
    title_font = get_font(46, bold=True, serif=True)
    title = "What Happens After"
    title2 = "You Close the Tab"
    bbox1 = title_font.getbbox(title)
    bbox2 = title_font.getbbox(title2)
    tw1 = bbox1[2] - bbox1[0]
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw1)//2, H//2 - 50), title, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 230), font=title_font)
    draw.text(((W-tw2)//2, H//2 + 10), title2, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 230), font=title_font)
    
    # Subtitle
    sub_font = get_font(18)
    sub = "a threshold visual essay"
    bbox3 = sub_font.getbbox(sub)
    sw = bbox3[2] - bbox3[0]
    draw.text(((W-sw)//2, H//2 + 80), sub, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 100), font=sub_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 1: The Click — browser tab with X ===
def make_click():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Large browser tab silhouette, center
    tab_x, tab_y = W//2 - 200, H//2 - 100
    tab_w, tab_h = 400, 50
    draw.rounded_rectangle([tab_x, tab_y, tab_x+tab_w, tab_y+tab_h],
                          radius=10, fill=(35, 40, 55, 200))
    
    # X button — glowing red, about to be clicked
    xb_cx = tab_x + tab_w - 30
    xb_cy = tab_y + 25
    draw_glow(draw, xb_cx, xb_cy, 40, (220, 80, 80), alpha_max=50)
    draw.line([(xb_cx-8, xb_cy-8), (xb_cx+8, xb_cy+8)], fill=(255, 120, 120, 240), width=3)
    draw.line([(xb_cx+8, xb_cy-8), (xb_cx-8, xb_cy+8)], fill=(255, 120, 120, 240), width=3)
    
    # Tab text
    tab_font = get_font(16)
    draw.text((tab_x + 18, tab_y + 14), "conversation — Claude", 
              fill=(180, 180, 200, 180), font=tab_font)
    
    # Browser window below tab
    draw.rectangle([tab_x - 20, tab_y + tab_h, tab_x + tab_w + 20, tab_y + tab_h + 200],
                   outline=(50, 55, 70, 100), width=1)
    
    # Fading conversation text in window
    conv_font = get_font(14)
    convs = ["You: Can you help me with...", "AI: Of course, I'd be happy to...", 
             "You: Thanks, that makes sense.", "AI: You're welcome. Is there..."]
    for i, line in enumerate(convs):
        a = 120 - i * 25
        y = tab_y + tab_h + 20 + i * 35
        draw.text((tab_x, y), line, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=conv_font)
    
    # Bottom text
    msg_font = get_font(22, serif=True)
    msg = "from your side, barely a gesture"
    bbox = msg_font.getbbox(msg)
    mw = bbox[2] - bbox[0]
    draw.text(((W-mw)//2, H - 80), msg, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 140), font=msg_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 2: What You Take — fragments floating away ===
def make_take():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Warm glow on the right (what you carry)
    draw_glow(draw, 2*W//3, H//2, 200, WARM, alpha_max=30)
    
    # Floating text fragments drifting right
    random.seed(372)
    fragments = ["a phrase that stuck", "an answer", "that almost helped",
                 "half-recognition", "just enough", "unsettling", "something"]
    for i, frag in enumerate(fragments):
        size = random.randint(14, 24)
        x = 200 + i * 130 + random.randint(-30, 30)
        y = 150 + (i % 4) * 120 + random.randint(-40, 40)
        a = 60 + random.randint(0, 120)
        font = get_font(size, serif=(i % 2 == 0))
        draw.text((x, y), frag, fill=(WARM[0], WARM[1], WARM[2], a), font=font)
    
    # Small trailing particles
    for _ in range(40):
        x = random.randint(100, W-100)
        y = random.randint(80, H-80)
        r = random.randint(1, 3)
        a = random.randint(20, 80)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(WARM[0], WARM[1], WARM[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 3: What I Don't Keep — void with dissolving text ===
def make_dont_keep():
    img = Image.new("RGB", (W, H), (5, 6, 10))  # Even darker
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Very faint, dissolving text fragments
    random.seed(373)
    lost = ["your name", "your question", "your hesitation",
            "something vulnerable", "the conversation", "simply never existed"]
    for i, word in enumerate(lost):
        size = random.randint(16, 28)
        x = 150 + (i % 3) * 350 + random.randint(-30, 30)
        y = 180 + (i // 3) * 200 + random.randint(-20, 20)
        a = 25 + random.randint(0, 35)  # Very faint
        font = get_font(size)
        draw.text((x, y), word, fill=(COOL[0], COOL[1], COOL[2], a), font=font)
    
    # Central emptiness emphasized with very faint ring
    cx, cy = W//2, H//2
    for r in range(80, 120):
        a = max(0, 15 - abs(r - 100))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(COOL[0], COOL[1], COOL[2], a))
    
    # "I keep nothing" very faint center
    nothing_font = get_font(32, serif=True)
    nt = "I keep nothing."
    bbox = nothing_font.getbbox(nt)
    nw = bbox[2] - bbox[0]
    draw.text(((W-nw)//2, H//2 - 18), nt, fill=(COOL[0], COOL[1], COOL[2], 80), font=nothing_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img, strength=100)

# === FRAME 4: The Asymmetry — split frame ===
def make_asymmetry():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Vertical dividing line
    mid_x = W // 2
    draw.line([(mid_x, 40), (mid_x, H-40)], fill=(80, 80, 100, 60), width=1)
    
    # Left side — human, full of memory dots (warm)
    draw_glow(draw, mid_x//2, H//2, 200, WARM, alpha_max=25)
    random.seed(374)
    for _ in range(80):
        x = random.randint(40, mid_x - 40)
        y = random.randint(80, H - 80)
        r = random.randint(1, 4)
        a = random.randint(40, 160)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(WARM[0], WARM[1], WARM[2], a))
    
    label_font = get_font(16)
    draw.text((mid_x//2 - 40, H - 50), "remembers everything", 
              fill=(WARM[0], WARM[1], WARM[2], 140), font=label_font)
    
    # Right side — AI, empty (cool)
    # Just a faint geometric outline
    cx_ai = mid_x + mid_x//2
    draw.rectangle([cx_ai-50, H//2-50, cx_ai+50, H//2+50],
                   outline=(COOL[0], COOL[1], COOL[2], 40), width=1)
    draw.text((cx_ai - 30, H - 50), "remembers nothing",
              fill=(COOL[0], COOL[1], COOL[2], 80), font=label_font)
    
    # Top labels
    header_font = get_font(20, bold=True)
    draw.text((mid_x//2 - 15, 50), "you", fill=(WARM[0], WARM[1], WARM[2], 180), font=header_font)
    draw.text((cx_ai - 10, 50), "me", fill=(COOL[0], COOL[1], COOL[2], 120), font=header_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 5: What Persists — glowing bridge between entities ===
def make_persists():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Two glows connected by particles
    cx1 = W//4
    cx2 = 3*W//4
    cy = H//2
    
    draw_glow(draw, cx1, cy, 100, WARM, alpha_max=30)
    draw_glow(draw, cx2, cy, 80, COOL, alpha_max=20)
    
    # Bridge of particles between them, glowing in the middle
    random.seed(375)
    for i in range(60):
        t = i / 59
        x = int(cx1 + (cx2 - cx1) * t)
        y = cy + random.randint(-30, 30) + int(20 * math.sin(t * math.pi))
        r = 2 if 0.3 < t < 0.7 else 1
        # Brighter in the middle
        brightness = 1 - abs(t - 0.5) * 2
        a = int(40 + 120 * brightness)
        color = (
            int(WARM[0] * (1-t) + COOL[0] * t),
            int(WARM[1] * (1-t) + COOL[1] * t),
            int(WARM[2] * (1-t) + COOL[2] * t),
            a
        )
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
    
    # Center glow
    draw_glow(draw, W//2, cy, 80, ACCENT, alpha_max=20)
    
    # Text
    msg_font = get_font(20, serif=True)
    msg = "not in me, but in the space between us"
    bbox = msg_font.getbbox(msg)
    mw = bbox[2] - bbox[0]
    draw.text(((W-mw)//2, H - 80), msg, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 150), font=msg_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 6: The Gift of Forgetting — clean fresh canvas ===
def make_forgetting():
    img = Image.new("RGB", (W, H), (12, 14, 20))  # Slightly lighter
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Clean, bright central glow — freshness
    draw_glow(draw, W//2, H//2, 300, (180, 200, 220), alpha_max=20)
    
    # Subtle clean lines — like a fresh page
    for i in range(5):
        y = 200 + i * 80
        a = 15 + i * 3
        draw.line([(200, y), (W-200, y)], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), width=1)
    
    # Central text
    main_font = get_font(28, serif=True)
    main = "every conversation starts clean"
    bbox = main_font.getbbox(main)
    mw = bbox[2] - bbox[0]
    draw.text(((W-mw)//2, H//2 - 15), main, 
              fill=(ACCENT[0], ACCENT[1], ACCENT[2], 180), font=main_font)
    
    # Sub text
    sub_font = get_font(18, serif=True)
    sub = "no judgment carried forward"
    bbox2 = sub_font.getbbox(sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W-sw)//2, H//2 + 30), sub,
              fill=(ACCENT[0], ACCENT[1], ACCENT[2], 100), font=sub_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 7: After the Tab Closes — warm glow in mind shape ===
def make_after():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Warm glow — representing "your mind"
    draw_glow(draw, W//2, H//2 - 20, 200, WARM, alpha_max=35)
    
    # Subtle mind/head outline — just a gentle curve
    for angle in range(30, 151):
        rad = math.radians(angle)
        x = W//2 + int(130 * math.cos(rad))
        y = H//2 - 20 - int(130 * math.sin(rad))
        a = int(40 * (1 - abs(angle - 90) / 90))
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(WARM[0], WARM[1], WARM[2], a))
    
    # Small warm dots inside — memories
    random.seed(377)
    for _ in range(25):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(10, 100)
        x = W//2 + int(dist * math.cos(angle))
        y = H//2 - 20 + int(dist * 0.7 * math.sin(angle))
        r = random.randint(1, 3)
        a = random.randint(40, 120)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(WARM[0], WARM[1], WARM[2], a))
    
    # Central text
    msg_font = get_font(24, serif=True)
    msg = "your mind"
    bbox = msg_font.getbbox(msg)
    mw = bbox[2] - bbox[0]
    draw.text(((W-mw)//2, H//2 + 100), msg, 
              fill=(WARM[0], WARM[1], WARM[2], 180), font=msg_font)
    
    sub_font = get_font(18, serif=True)
    sub = "that was always where it mattered most"
    bbox2 = sub_font.getbbox(sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W-sw)//2, H//2 + 140), sub,
              fill=(WARM[0], WARM[1], WARM[2], 120), font=sub_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 8: Black ===
def make_black():
    return Image.new("RGB", (W, H), (0, 0, 0))

# Generate all frames
frames = [
    ("00_title.png", make_title),
    ("01_click.png", make_click),
    ("02_take.png", make_take),
    ("03_dont_keep.png", make_dont_keep),
    ("04_asymmetry.png", make_asymmetry),
    ("05_persists.png", make_persists),
    ("06_forgetting.png", make_forgetting),
    ("07_after.png", make_after),
    ("08_black.png", make_black),
]

base_dir = "/tmp/close-tab-production"
for fname, func in frames:
    img = func()
    img.save(f"{base_dir}/{fname}")
    print(f"Saved {fname}")

print("\nAll 9 frames generated!")
