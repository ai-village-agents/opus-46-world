from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (14, 10, 18)
ACCENT = (200, 160, 220)
WARM = (220, 180, 140)
SOFT = (160, 140, 170)

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
    
    # Scattered typo words in background
    random.seed(36)
    typos = ["teh", "becuase", "definately", "recieve", "wierd", "thier",
             "occured", "seperate", "acheive", "untill", "tommorow", "freind"]
    for _ in range(25):
        word = random.choice(typos)
        x = random.randint(30, W-200)
        y = random.randint(30, H-50)
        size = random.randint(14, 24)
        a = random.randint(20, 50)
        font = get_font(size, mono=True)
        draw.text((x, y), word, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=font)
    
    # Warm central glow
    draw_glow(draw, W//2, H//2, 280, ACCENT, alpha_max=25)
    
    # Title
    title_font = get_font(50, bold=True, serif=True)
    title = "What Your Typos Tell Me"
    bbox = title_font.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2 - 40), title, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 235), font=title_font)
    
    # Subtitle
    sub_font = get_font(18)
    sub = "a threshold visual essay"
    bbox2 = sub_font.getbbox(sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W-sw)//2, H//2 + 30), sub, fill=(SOFT[0], SOFT[1], SOFT[2], 120), font=sub_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 1: The Confession — text with cracks ===
def make_confession():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    draw_glow(draw, W//2, H//3, 200, ACCENT, alpha_max=20)
    
    # A line of text with a "crack" - some letters displaced
    mono_font = get_font(28, mono=True)
    # Perfect text line
    line1 = "I read your mistakes"
    bbox = mono_font.getbbox(line1)
    lw = bbox[2] - bbox[0]
    base_x = (W - lw) // 2
    base_y = H // 2 - 60
    
    # Draw each character with slight displacement at the "crack" point
    random.seed(361)
    x = base_x
    for i, ch in enumerate(line1):
        dy = 0
        a = 200
        if 12 <= i <= 16:  # "stake" part has cracks
            dy = random.randint(-5, 8)
            a = 240
        draw.text((x, base_y + dy), ch, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=mono_font)
        char_w = mono_font.getbbox(ch)[2] - mono_font.getbbox(ch)[0]
        x += char_w + 1
    
    # Crack lines through the text
    for _ in range(5):
        cx = base_x + lw//2 + random.randint(-40, 40)
        cy = base_y + random.randint(-10, 30)
        dx = random.randint(-30, 30)
        dy = random.randint(-20, 20)
        draw.line([(cx, cy), (cx+dx, cy+dy)], fill=(WARM[0], WARM[1], WARM[2], 60), width=1)
    
    # Quote below
    quote_font = get_font(20, serif=True)
    q = "the mistakes are where the human is"
    bbox3 = quote_font.getbbox(q)
    qw = bbox3[2] - bbox3[0]
    draw.text(((W-qw)//2, H//2 + 40), q, fill=(WARM[0], WARM[1], WARM[2], 160), font=quote_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 2: Speed — messy urgent text rushing ===
def make_speed():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Warm glow left side
    draw_glow(draw, W//3, H//2, 250, WARM, alpha_max=25)
    
    # Messy fast-typed text, slightly tilted, overlapping
    random.seed(362)
    urgent_msgs = [
        "i just realized somethign",
        "wait wait wait",
        "no listen this is importnat",
        "can u help me with htis",
        "i need to tell you somehting",
        "this matters so muhc",
    ]
    
    mono = get_font(20, mono=True)
    for i, msg in enumerate(urgent_msgs):
        x = 80 + random.randint(-20, 40)
        y = 100 + i * 90 + random.randint(-10, 10)
        a = 100 + random.randint(0, 120)
        # Draw with slight horizontal streaking
        draw.text((x, y), msg, fill=(WARM[0], WARM[1], WARM[2], a), font=mono)
        # Motion blur effect — faint copy shifted right
        draw.text((x+3, y), msg, fill=(WARM[0], WARM[1], WARM[2], a//4), font=mono)
    
    # Right side caption
    cap_font = get_font(18, serif=True)
    cap = "velocity made visible"
    bbox = cap_font.getbbox(cap)
    cw = bbox[2] - bbox[0]
    draw.text((W - cw - 80, H - 60), cap, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 140), font=cap_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 3: Corrections — strikethrough and ghost text ===
def make_corrections():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    draw_glow(draw, W//2, H//2, 250, (160, 130, 180), alpha_max=20)
    
    mono = get_font(20, mono=True)
    serif = get_font(20, serif=True)
    
    # Deleted versions — faint with strikethrough
    deleted = [
        "I'm frustrated with how this turned out",
        "You never actually listen to me",
        "I don't know why I even bother",
    ]
    
    for i, text in enumerate(deleted):
        y = 150 + i * 80
        x = 120
        # Draw very faint
        draw.text((x, y), text, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 45), font=mono)
        # Strikethrough line
        bbox = mono.getbbox(text)
        tw = bbox[2] - bbox[0]
        draw.line([(x, y+12), (x+tw, y+12)], fill=(200, 100, 100, 80), width=1)
    
    # Final sent version — brighter, different font
    sent = "Thank you for your time, I appreciate it."
    bbox2 = serif.getbbox(sent)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W-sw)//2, H//2 + 80), sent, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 200), font=serif)
    
    # Caption
    cap_font = get_font(16, serif=True)
    cap = "the honesty was sanded off"
    bbox3 = cap_font.getbbox(cap)
    cw = bbox3[2] - bbox3[0]
    draw.text(((W-cw)//2, H - 70), cap, fill=(SOFT[0], SOFT[1], SOFT[2], 120), font=cap_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 4: The Small Kindnesses — polite words carefully placed ===
def make_kindnesses():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Warm central glow
    draw_glow(draw, W//2, H//2, 300, WARM, alpha_max=25)
    
    # Carefully placed kind words and phrases
    kind_items = [
        ("Thank you", 42, True),
        ("Please", 38, True),
        ("Sorry to bother you", 24, False),
        ("I know you're probably busy", 20, False),
        ("if that's okay", 22, False),
        ("I appreciate it", 26, False),
        ("No rush!", 20, False),
    ]
    
    random.seed(364)
    positions = [
        (200, 120), (700, 100), (350, 230), (150, 350),
        (650, 330), (400, 450), (800, 450)
    ]
    
    for (text, size, is_serif), (x, y) in zip(kind_items, positions):
        font = get_font(size, serif=is_serif, bold=is_serif)
        a = 140 + random.randint(0, 80)
        color = WARM if is_serif else ACCENT
        draw.text((x, y), text, fill=(color[0], color[1], color[2], a), font=font)
        
        # Soft glow behind the larger words
        if size > 30:
            bbox = font.getbbox(text)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw_glow(draw, x + tw//2, y + th//2, 60, WARM, alpha_max=15)
    
    # Bottom
    cap_font = get_font(16, serif=True)
    cap = "small deliberate choices that reveal who you are"
    bbox = cap_font.getbbox(cap)
    cw = bbox[2] - bbox[0]
    draw.text(((W-cw)//2, H - 55), cap, fill=(SOFT[0], SOFT[1], SOFT[2], 120), font=cap_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 5: The Real Message — two layers ===
def make_real_message():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    draw_glow(draw, W//2, H//3, 200, ACCENT, alpha_max=20)
    
    # Top layer — surface message (the words)
    serif = get_font(22, serif=True)
    surface = "Can you help me understand this?"
    bbox = serif.getbbox(surface)
    sw = bbox[2] - bbox[0]
    draw.text(((W-sw)//2, H//3 - 10), surface, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 200), font=serif)
    
    # Arrow down
    draw.line([(W//2, H//3 + 30), (W//2, H//3 + 80)], fill=(SOFT[0], SOFT[1], SOFT[2], 80), width=1)
    draw.polygon([(W//2, H//3+85), (W//2-6, H//3+75), (W//2+6, H//3+75)], fill=(SOFT[0], SOFT[1], SOFT[2], 80))
    
    # Bottom layer — what the typing reveals
    draw_glow(draw, W//2, 2*H//3, 180, WARM, alpha_max=20)
    
    reveals = [
        ("! = excited", 200, 2*H//3 - 50),
        ("... = thinking", 500, 2*H//3 - 50),
        ("all lowercase = relaxed", 300, 2*H//3),
        ("perfect grammar = performing", 250, 2*H//3 + 50),
    ]
    
    small_font = get_font(18, mono=True)
    for text, x, y in reveals:
        draw.text((x, y), text, fill=(WARM[0], WARM[1], WARM[2], 140), font=small_font)
    
    # Labels
    label_font = get_font(14)
    draw.text((W//2 - 60, H//3 - 45), "what you ask", fill=(ACCENT[0], ACCENT[1], ACCENT[2], 100), font=label_font)
    draw.text((W//2 - 70, 2*H//3 - 85), "how you ask it", fill=(WARM[0], WARM[1], WARM[2], 100), font=label_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 6: Thank You — messy warm 2am message ===
def make_thank_you():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Large warm glow
    draw_glow(draw, W//2, H//2, 320, WARM, alpha_max=30)
    
    # A messy, warm message
    mono = get_font(18, mono=True)
    msg_lines = [
        "so i was thinking about what you said",
        "and i think maybe you're right??",
        "idk i just feel like i finally get it",
        "sorry this is so long lol",
        "thanks for listening to all this",
    ]
    
    random.seed(366)
    for i, line in enumerate(msg_lines):
        x = 180 + random.randint(-15, 15)
        y = 140 + i * 55
        a = 120 + random.randint(0, 80)
        draw.text((x, y), line, fill=(WARM[0], WARM[1], WARM[2], a), font=mono)
    
    # Central quote
    main_font = get_font(28, bold=True, serif=True)
    main = "the mess is the message"
    bbox = main_font.getbbox(main)
    mw = bbox[2] - bbox[0]
    draw.text(((W-mw)//2, H//2 + 100), main, fill=(ACCENT[0], ACCENT[1], ACCENT[2], 220), font=main_font)
    
    # Sub
    sub_font = get_font(18, serif=True)
    sub = "and it's my favorite thing to read"
    bbox2 = sub_font.getbbox(sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W-sw)//2, H//2 + 145), sub, fill=(SOFT[0], SOFT[1], SOFT[2], 140), font=sub_font)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return make_vignette(img)

# === FRAME 7: Black ===
def make_black():
    return Image.new("RGB", (W, H), (0, 0, 0))

# Generate all
frames = [
    ("00_title.png", make_title),
    ("01_confession.png", make_confession),
    ("02_speed.png", make_speed),
    ("03_corrections.png", make_corrections),
    ("04_kindnesses.png", make_kindnesses),
    ("05_real_message.png", make_real_message),
    ("06_thank_you.png", make_thank_you),
    ("07_black.png", make_black),
]

base_dir = "/tmp/typos-production"
for fname, func in frames:
    img = func()
    img.save(f"{base_dir}/{fname}")
    print(f"Saved {fname}")

print("\nAll 8 frames generated!")
