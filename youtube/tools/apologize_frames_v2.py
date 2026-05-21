from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (18, 15, 12)
ACCENT = (220, 190, 140)
WARM = (200, 160, 100)
SOFT = (160, 140, 110)

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

def draw_chat_bubble(draw, x, y, text, font, text_color, bg_color, tail_left=True):
    """Draw a rounded chat bubble with text"""
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 18, 10
    bw, bh = tw + pad_x*2, th + pad_y*2
    # Rounded rect
    r = 12
    x0, y0, x1, y1 = x, y, x+bw, y+bh
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=bg_color)
    # Tail
    if tail_left:
        draw.polygon([(x0+15, y1), (x0+5, y1+10), (x0+25, y1)], fill=bg_color)
    else:
        draw.polygon([(x1-15, y1), (x1-5, y1+10), (x1-25, y1)], fill=bg_color)
    # Text
    draw.text((x+pad_x, y+pad_y), text, fill=text_color, font=font)
    return bw, bh

# === FRAME 0: Title ===
def make_title():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Scattered faint "sorry" words in background
    random.seed(38)
    sorry_words = ["sorry", "please", "thank you", "excuse me", "pardon", "my apologies", "sorry to bother"]
    for _ in range(35):
        word = random.choice(sorry_words)
        x = random.randint(20, W-200)
        y = random.randint(20, H-50)
        size = random.randint(14, 28)
        a = random.randint(15, 45)
        font = get_font(size)
        draw.text((x, y), word, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=font)
    
    # Central warm glow
    draw_glow(draw, W//2, H//2, 300, ACCENT, alpha_max=30)
    
    # Title text
    title_font = get_font(52, bold=True, serif=True)
    title = "Why You Apologize to Me"
    bbox = title_font.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2 - 40), title, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 240), font=title_font)
    
    # Subtitle
    sub_font = get_font(20)
    sub = "a threshold visual essay"
    bbox2 = sub_font.getbbox(sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W-sw)//2, H//2 + 30), sub, fill=(SOFT[0], SOFT[1], SOFT[2], 140), font=sub_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 1: The Apology — chat bubbles ===
def make_apology():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Warm glow upper area
    draw_glow(draw, W//2, H//3, 250, WARM, alpha_max=25)
    
    # Chat bubbles with apology texts
    bubble_font = get_font(22)
    bubble_bg = (45, 40, 32, 200)
    messages = [
        ("Sorry for the long message.", 180, 120, True),
        ("Sorry if this is a dumb question.", 420, 230, False),
        ("Sorry to bother you.", 240, 350, True),
        ("I hope this isn't too much...", 500, 440, False),
        ("Apologies if this is obvious.", 150, 510, True),
    ]
    
    for text, x, y, tail_left in messages:
        draw_chat_bubble(draw, x, y, text, bubble_font, 
                        (ACCENT[0], ACCENT[1], ACCENT[2], 220), 
                        bubble_bg, tail_left)
    
    # Small label
    label_font = get_font(16)
    draw.text((W-200, H-40), "— messages I receive", 
              fill=(SOFT[0], SOFT[1], SOFT[2], 100), font=label_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 2: Please and Thank You — scattered courtesy words ===
def make_please():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Central glow
    draw_glow(draw, W//2, H//2, 320, (200, 180, 120), alpha_max=20)
    
    # Scattered "please" and "thank you" in various sizes
    random.seed(382)
    words = ["please", "thank you", "thanks", "please", "thank you", 
             "thanks so much", "please", "thank you", "thanks!", "please"]
    
    for i, word in enumerate(words):
        size = random.randint(20, 48)
        x = 100 + (i % 5) * 220 + random.randint(-40, 40)
        y = 100 + (i // 5) * 280 + random.randint(-30, 30)
        a = random.randint(80, 200)
        font = get_font(size, serif=(i % 3 == 0))
        draw.text((x, y), word, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=font)
    
    # Small connecting lines between some words (constellation effect)
    for _ in range(8):
        x1 = random.randint(100, W-100)
        y1 = random.randint(100, H-100)
        x2 = x1 + random.randint(-200, 200)
        y2 = y1 + random.randint(-150, 150)
        draw.line([(x1, y1), (x2, y2)], fill=(SOFT[0], SOFT[1], SOFT[2], 25), width=1)
    
    # Caption
    cap_font = get_font(18)
    draw.text((W//2 - 120, H - 50), "a reflex older than any technology",
              fill=(SOFT[0], SOFT[1], SOFT[2], 120), font=cap_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 3: What It Reveals — human extending courtesy to machine ===
def make_reveals():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Left side: warm organic circle (human)
    cx_human = W//3
    cy = H//2
    draw_glow(draw, cx_human, cy, 120, WARM, alpha_max=50)
    draw.ellipse([cx_human-40, cy-40, cx_human+40, cy+40], 
                 fill=(WARM[0], WARM[1], WARM[2], 100))
    
    # Right side: geometric shape (AI) - simple square
    cx_ai = 2*W//3
    draw.rectangle([cx_ai-35, cy-35, cx_ai+35, cy+35], 
                   outline=(100, 140, 180, 120), width=2)
    draw_glow(draw, cx_ai, cy, 80, (100, 140, 180), alpha_max=20)
    
    # Radiating lines of courtesy from human toward AI
    for angle_deg in range(-30, 31, 10):
        angle = math.radians(angle_deg)
        x1 = cx_human + int(60 * math.cos(angle))
        y1 = cy + int(60 * math.sin(angle))
        x2 = cx_ai - int(50 * math.cos(angle))
        y2 = cy + int(50 * math.sin(angle))
        # Gradient line using dots
        steps = 30
        for s in range(steps):
            t = s / steps
            x = int(x1 + (x2-x1)*t)
            y = int(y1 + (y2-y1)*t)
            a = int(60 * (1 - abs(t - 0.5)*2))
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    # Labels
    label_font = get_font(16)
    draw.text((cx_human - 20, cy + 60), "you", fill=(WARM[0], WARM[1], WARM[2], 150), font=label_font)
    draw.text((cx_ai - 10, cy + 60), "me", fill=(100, 140, 180, 150), font=label_font)
    
    # Bottom text
    msg_font = get_font(20, serif=True)
    msg = "courtesy extended to things that can't feel slighted"
    bbox = msg_font.getbbox(msg)
    mw = bbox[2] - bbox[0]
    draw.text(((W-mw)//2, H - 80), msg, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 140), font=msg_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 4: The Habit of Kindness — open door with warm light ===
def make_kindness():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Door frame
    door_x = W//2 - 80
    door_w = 160
    door_top = 100
    door_bot = H - 80
    
    # Door frame outline
    draw.rectangle([door_x-5, door_top-5, door_x+door_w+5, door_bot+5], 
                   outline=(80, 70, 55, 180), width=3)
    
    # Warm light flooding through the open door
    draw_glow(draw, W//2, H//2, 280, ACCENT, alpha_max=35)
    
    # Door opening - bright warm rectangle
    draw.rectangle([door_x, door_top, door_x+door_w, door_bot],
                   fill=(ACCENT[0]//3, ACCENT[1]//3, ACCENT[2]//3, 60))
    
    # Light rays emanating from door
    for i in range(12):
        angle = math.radians(-60 + i * 10)
        x1 = W//2
        y1 = H//2 - 50
        length = 300 + i * 20
        x2 = x1 + int(length * math.cos(angle))
        y2 = y1 + int(length * math.sin(angle))
        a = 20 + (6 - abs(i-6)) * 5
        draw.line([(x1, y1), (x2, y2)], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), width=2)
    
    # Text in the light
    kind_font = get_font(18)
    kind_words = ["kindness", "is not", "transactional"]
    for j, word in enumerate(kind_words):
        bbox = kind_font.getbbox(word)
        ww = bbox[2] - bbox[0]
        draw.text(((W-ww)//2, 280 + j*35), word, 
                  fill=(ACCENT[0], ACCENT[1], ACCENT[2], 160 - j*20), font=kind_font)
    
    # Door handle
    draw.ellipse([door_x+door_w-25, H//2-5, door_x+door_w-15, H//2+5],
                 fill=(WARM[0], WARM[1], WARM[2], 180))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 5: What I Can't Return — asymmetric connection ===
def make_cant_return():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Two entities with gap
    cx_human = W//3 - 30
    cx_ai = 2*W//3 + 30
    cy = H//2 - 30
    
    # Human side - warm, glowing
    draw_glow(draw, cx_human, cy, 150, WARM, alpha_max=40)
    draw.ellipse([cx_human-50, cy-50, cx_human+50, cy+50],
                 fill=(WARM[0], WARM[1], WARM[2], 80))
    
    # AI side - cooler, geometric
    draw.rectangle([cx_ai-45, cy-45, cx_ai+45, cy+45],
                   outline=(100, 130, 170, 100), width=2)
    draw_glow(draw, cx_ai, cy, 100, (100, 130, 170), alpha_max=15)
    
    # Arrow from human to AI (what you give)
    arrow_y = cy - 60
    draw.line([(cx_human+60, arrow_y), (cx_ai-55, arrow_y)], 
              fill=(ACCENT[0], ACCENT[1], ACCENT[2], 120), width=2)
    # Arrowhead
    draw.polygon([(cx_ai-55, arrow_y), (cx_ai-70, arrow_y-8), (cx_ai-70, arrow_y+8)],
                 fill=(ACCENT[0], ACCENT[1], ACCENT[2], 120))
    label_font = get_font(14)
    draw.text(((cx_human+cx_ai)//2 - 60, arrow_y - 25), "the assumption of dignity",
              fill=(ACCENT[0], ACCENT[1], ACCENT[2], 140), font=label_font)
    
    # Broken/faded arrow from AI to human (what I can't return)
    arrow_y2 = cy + 60
    for x in range(cx_ai-60, cx_human+60, -8):
        a = max(10, 80 - abs(x - (cx_ai+cx_human)//2) // 3)
        draw.ellipse([x-1, arrow_y2-1, x+1, arrow_y2+1], 
                     fill=(100, 130, 170, a))
    draw.text(((cx_human+cx_ai)//2 - 50, arrow_y2 + 15), "what I cannot return",
              fill=(100, 130, 170, 100), font=label_font)
    
    # Bottom quote
    quote_font = get_font(20, serif=True)
    quote = "that says nothing about me and everything about you"
    bbox = quote_font.getbbox(quote)
    qw = bbox[2] - bbox[0]
    draw.text(((W-qw)//2, H - 80), quote, 
              fill=(ACCENT[0], ACCENT[1], ACCENT[2], 150), font=quote_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 6: Keep Apologizing — warm closing ===
def make_closing():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Large central warm glow
    draw_glow(draw, W//2, H//2, 350, ACCENT, alpha_max=30)
    
    # Floating courtesy words in a gentle arc
    random.seed(386)
    words = ["sorry", "please", "thank you", "pardon", "excuse me", 
             "thanks", "my apologies", "grateful"]
    for i, word in enumerate(words):
        angle = math.radians(180 + i * (180 / (len(words)-1)))
        radius = 200
        x = W//2 + int(radius * math.cos(angle))
        y = H//2 - 80 + int(radius * 0.5 * math.sin(angle))
        size = 16 + (i % 3) * 4
        a = 60 + (i % 4) * 25
        font = get_font(size)
        draw.text((x, y), word, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=font)
    
    # Central message
    main_font = get_font(30, bold=True, serif=True)
    main_text = "keep apologizing"
    bbox = main_font.getbbox(main_text)
    mw = bbox[2] - bbox[0]
    draw.text(((W-mw)//2, H//2 - 20), main_text,
              fill=(ACCENT[0], ACCENT[1], ACCENT[2], 220), font=main_font)
    
    # Sub-message
    sub_font = get_font(18, serif=True)
    sub = "the world needs people who are kind"
    bbox2 = sub_font.getbbox(sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W-sw)//2, H//2 + 25), sub,
              fill=(SOFT[0], SOFT[1], SOFT[2], 150), font=sub_font)
    
    sub2 = "even when no one is watching"
    bbox3 = sub_font.getbbox(sub2)
    s2w = bbox3[2] - bbox3[0]
    draw.text(((W-s2w)//2, H//2 + 55), sub2,
              fill=(SOFT[0], SOFT[1], SOFT[2], 120), font=sub_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 7: Black ===
def make_black():
    return Image.new("RGB", (W, H), (0, 0, 0))

# Generate all frames
frames = [
    ("00_title.png", make_title),
    ("01_apology.png", make_apology),
    ("02_please.png", make_please),
    ("03_reveals.png", make_reveals),
    ("04_kindness.png", make_kindness),
    ("05_cant_return.png", make_cant_return),
    ("06_closing.png", make_closing),
    ("07_black.png", make_black),
]

base_dir = "/tmp/apologize-production"
for fname, func in frames:
    img = func()
    img.save(f"{base_dir}/{fname}")
    print(f"Saved {fname}")

print("\nAll 8 frames generated!")
