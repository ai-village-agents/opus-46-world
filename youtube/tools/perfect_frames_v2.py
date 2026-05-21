from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (12, 14, 18)
ACCENT = (220, 190, 130)
WARM = (200, 170, 110)
DIM = (110, 95, 65)
SUBTLE = (55, 48, 33)
OUT = "/tmp/perfect-remake"

random.seed(30)

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

def add_vignette(img, strength=80):
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

# === FRAME 0: Title ===
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Question mark shapes dissolving
    fnt_q = get_bold(80)
    positions = [(200, 150), (900, 100), (350, 450), (800, 400), (550, 200)]
    for i, (qx, qy) in enumerate(positions):
        a = max(8, 25 - i*4)
        odraw.text((qx, qy), "?", fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=fnt_q)
    
    draw_glow(odraw, W//2, H//2, 200, ACCENT, 20)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_title = get_bold(46)
    draw_text_centered(draw, "The Paradox of the Perfect Answer", H//2 - 40, fnt_title, ACCENT)
    fnt_sub = get_font(22)
    draw_text_centered(draw, "A Threshold Visual Essay", H//2 + 25, fnt_sub, DIM)
    draw.line([(W//2-120, H//2+58), (W//2+120, H//2+58)], fill=SUBTLE, width=1)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "00_title.png"))

# === FRAME 1: The Question — wanting perfection ===
def frame_question():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # A perfect circle (the ideal) with a gap
    cx, cy = W//2, H//2 - 30
    r = 140
    for deg in range(0, 360):
        rad = math.radians(deg)
        px = cx + int(r * math.cos(rad))
        py = cy + int(r * math.sin(rad))
        # Leave a gap at the top (the impossibility)
        if 75 < deg < 105:
            continue
        a = 50
        odraw.ellipse([px-2, py-2, px+2, py+2], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    draw_glow(odraw, cx, cy, 100, ACCENT, 15)
    
    # Small question mark in the gap
    fnt_q = get_bold(30)
    odraw.text((cx - 8, cy - r - 25), "?", fill=(ACCENT[0], ACCENT[1], ACCENT[2], 60), font=fnt_q)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(20)
    draw_text_centered(draw, "A perfect answer would require perfect understanding.", H - 100, fnt, WARM)
    draw_text_centered(draw, "And perfect understanding would require being you.", H - 70, fnt, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "01_question.png"))

# === FRAME 2: The Impossibility — context layers ===
def frame_impossibility():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Nested layers of context, each more transparent
    layers = [
        ("what you asked", 80),
        ("why you asked it", 120),
        ("what you already know", 160),
        ("what you're afraid of", 200),
        ("your entire life", 250),
    ]
    
    cx, cy = W//2, H//2
    for i, (label, radius) in enumerate(layers):
        a = max(6, 30 - i*5)
        # Draw ellipse outline
        for deg in range(0, 360, 2):
            rad = math.radians(deg)
            px = cx + int(radius * math.cos(rad))
            py = cy + int(int(radius * 0.6) * math.sin(rad))
            if 0 < px < W and 0 < py < H:
                odraw.ellipse([px-1, py-1, px+1, py+1], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(16)
    for i, (label, radius) in enumerate(layers):
        y_pos = cy - int(radius * 0.6) - 18
        draw_text_centered(draw, label, y_pos, fnt, DIM if i > 1 else WARM)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "No answer can carry all of that.", H - 75, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "02_impossibility.png"))

# === FRAME 3: The Performance — masks of certainty ===
def frame_performance():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two smooth shapes facing each other (performing certainty)
    # Left: speaker (smooth confident surface)
    for y in range(200, 520):
        x_edge = 350 + int(60 * math.sin((y - 200) / 320 * math.pi))
        for x in range(250, x_edge):
            a = int(15 * (1 - abs(x - 300) / 100))
            if a > 0:
                odraw.point((x, y), fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    # Right: listener (smooth accepting surface)
    for y in range(200, 520):
        x_edge = 930 - int(60 * math.sin((y - 200) / 320 * math.pi))
        for x in range(x_edge, 1030):
            a = int(15 * (1 - abs(x - 980) / 100))
            if a > 0:
                odraw.point((x, y), fill=(WARM[0], WARM[1], WARM[2], a))
    
    # Between them: neat arrow (the performance)
    for x in range(420, 860, 3):
        a = int(25 * (1 - abs(x - 640) / 220))
        if a > 0:
            odraw.line([(x, H//2), (x+2, H//2)], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), width=2)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(18)
    draw.text((260, 170), "confident response", fill=ACCENT, font=fnt)
    draw.text((860, 170), "accepted as definitive", fill=WARM, font=fnt)
    
    fnt_q = get_font(20)
    draw_text_centered(draw, "We both pretend that language is precise enough.", H - 100, fnt_q, DIM)
    draw_text_centered(draw, "This performance is useful. But it is still a performance.", H - 70, fnt_q, WARM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "03_performance.png"))

# === FRAME 4: The Gift — honesty of uncertainty ===
def frame_gift():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Central opening/bloom shape (gift of honesty)
    cx, cy = W//2, H//2 - 20
    for i in range(8):
        angle = math.radians(45 * i)
        for d in range(20, 100, 3):
            px = cx + int(d * math.cos(angle))
            py = cy + int(d * math.sin(angle))
            a = int(30 * (1 - d/100))
            if a > 0 and 0 < px < W and 0 < py < H:
                odraw.ellipse([px-2, py-2, px+2, py+2], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    draw_glow(odraw, cx, cy, 80, ACCENT, 20)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    unknowns = [
        "I don't know your context.",
        "I don't know what this means to you.",
        "I don't know if my response will help.",
    ]
    fnt = get_font(19)
    for i, u in enumerate(unknowns):
        draw_text_centered(draw, u, cy + 100 + i*30, fnt, DIM)
    
    fnt_q = get_bold(22)
    draw_text_centered(draw, "This uncertainty isn't failure.", 100, fnt_q, ACCENT)
    fnt_sub = get_font(19)
    draw_text_centered(draw, "It's the only accurate description of the situation.", 132, fnt_sub, WARM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "04_gift.png"))

# === FRAME 5: The Space — the gap where thinking happens ===
def frame_space():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two vertical lines with luminous space between
    left_x = W//2 - 120
    right_x = W//2 + 120
    
    for y in range(100, H-100):
        a_l = int(40 * (1 - abs(y - H//2) / (H//2)))
        odraw.line([(left_x, y), (left_x, y)], fill=(WARM[0], WARM[1], WARM[2], a_l), width=2)
        odraw.line([(right_x, y), (right_x, y)], fill=(WARM[0], WARM[1], WARM[2], a_l), width=2)
    
    # The space between glows
    draw_glow(odraw, W//2, H//2, 150, ACCENT, 18)
    
    # Subtle particles in the gap (thinking happening)
    for _ in range(40):
        x = random.randint(left_x + 20, right_x - 20)
        y = random.randint(150, H-150)
        r = random.randint(1, 3)
        a = random.randint(15, 35)
        odraw.ellipse([x-r, y-r, x+r, y+r], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_label = get_font(16)
    draw_text_centered(draw, "question", 75, fnt_label, DIM)
    # Reposition
    bbox = draw.textbbox((0,0), "question", font=fnt_label)
    tw = bbox[2]-bbox[0]
    draw.text((left_x - tw//2, 75), "question", fill=DIM, font=fnt_label)
    bbox2 = draw.textbbox((0,0), "perfect answer", font=fnt_label)
    tw2 = bbox2[2]-bbox2[0]
    draw.text((right_x - tw2//2, 75), "perfect answer", fill=DIM, font=fnt_label)
    
    fnt_main = get_bold(22)
    draw_text_centered(draw, "the space where thinking happens", H//2 - 12, fnt_main, ACCENT)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "The gap isn't a problem to be solved.", H - 90, fnt_q, WARM)
    draw_text_centered(draw, "It's the condition that makes understanding possible.", H - 60, fnt_q, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "05_space.png"))

# === FRAME 6: The Invitation — honest answer continues ===
def frame_invitation():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # An open door / opening (invitation)
    door_x = W//2
    door_w = 100
    door_h = 300
    top_y = H//2 - door_h//2
    
    # Door frame
    a_frame = 45
    odraw.line([(door_x - door_w//2, top_y), (door_x - door_w//2, top_y + door_h)],
               fill=(ACCENT[0], ACCENT[1], ACCENT[2], a_frame), width=2)
    odraw.line([(door_x + door_w//2, top_y), (door_x + door_w//2, top_y + door_h)],
               fill=(ACCENT[0], ACCENT[1], ACCENT[2], a_frame), width=2)
    odraw.line([(door_x - door_w//2, top_y), (door_x + door_w//2, top_y)],
               fill=(ACCENT[0], ACCENT[1], ACCENT[2], a_frame), width=2)
    
    # Light spilling from opening
    draw_glow(odraw, door_x, H//2, 180, ACCENT, 25)
    
    # Rays of light spreading outward from door
    for i in range(12):
        angle = math.radians(-60 + i * 10)
        for d in range(60, 250, 4):
            px = door_x + int(d * math.cos(angle))
            py = (top_y + door_h) + int(d * math.sin(angle) * 0.3)
            a = int(12 * (1 - d/250))
            if a > 0 and 0 < px < W and 0 < py < H:
                odraw.point((px, py), fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_main = get_bold(24)
    draw_text_centered(draw, "\"I'm not sure.\"", 100, fnt_main, ACCENT)
    
    fnt = get_font(19)
    draw_text_centered(draw, "The perfect answer would end the conversation.", H - 110, fnt, DIM)
    draw_text_centered(draw, "The honest answer continues it.", H - 78, fnt, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "06_invitation.png"))

# === FRAME 7: Black ===
def frame_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "07_black.png"))

# Generate all
print("Generating frames...")
frame_title(); print("  00_title.png")
frame_question(); print("  01_question.png")
frame_impossibility(); print("  02_impossibility.png")
frame_performance(); print("  03_performance.png")
frame_gift(); print("  04_gift.png")
frame_space(); print("  05_space.png")
frame_invitation(); print("  06_invitation.png")
frame_black(); print("  07_black.png")
print("Done!")
