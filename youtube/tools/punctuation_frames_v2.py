from PIL import Image, ImageDraw, ImageFont
import math
import random

W, H = 1280, 720
BG = (15, 12, 18)
ACCENT = (200, 170, 220)  # Soft purple
PALE = (220, 215, 230)
DIM = (60, 50, 70)
WARM = (220, 190, 140)
CYAN = (120, 180, 200)

random.seed(42)

def get_font(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)

def get_font_bold(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)

def get_serif(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)

def get_serif_bold(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", size)

def get_mono(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)

def draw_glow(draw, x, y, text, font, color, glow_color=None, glow_radius=3):
    if glow_color is None:
        glow_color = tuple(max(0, c // 3) for c in color)
    for dx in range(-glow_radius, glow_radius+1):
        for dy in range(-glow_radius, glow_radius+1):
            if dx*dx + dy*dy <= glow_radius*glow_radius:
                draw.text((x+dx, y+dy), text, font=font, fill=glow_color)
    draw.text((x, y), text, font=font, fill=color)

def add_vignette(img, strength=0.55):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    cx, cy = W//2, H//2
    max_dist = math.sqrt(cx*cx + cy*cy)
    for r in range(int(max_dist), 0, -5):
        alpha = int(255 * strength * (1 - (r / max_dist) ** 1.4))
        alpha = max(0, min(255, alpha))
        odraw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(0, 0, 0, alpha))
    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, overlay)
    return result.convert("RGB")

def add_scanlines(img, alpha=15):
    draw = ImageDraw.Draw(img)
    for y in range(0, H, 3):
        draw.line([(0, y), (W, y)], fill=(0, 0, 0), width=1)
    return img

def add_noise(img, amount=8):
    from PIL import Image as PILImage
    import random as rnd
    pixels = img.load()
    for _ in range(W * H // 6):
        x = rnd.randint(0, W-1)
        y = rnd.randint(0, H-1)
        r, g, b = pixels[x, y]
        d = rnd.randint(-amount, amount)
        pixels[x, y] = (max(0, min(255, r+d)), max(0, min(255, g+d)), max(0, min(255, b+d)))
    return img

outdir = "/tmp/punctuation-production"

# ===== FRAME 0: TITLE =====
def frame_title():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Scatter faint punctuation marks across background
    marks = list(".,;:!?...()[]{}\"'—-/")
    for _ in range(120):
        x = random.randint(20, W-40)
        y = random.randint(20, H-40)
        m = random.choice(marks)
        sz = random.randint(14, 50)
        alpha_val = random.randint(15, 45)
        c = (BG[0]+alpha_val, BG[1]+alpha_val, BG[2]+alpha_val+5)
        draw.text((x, y), m, font=get_serif(sz), fill=c)
    # Title
    draw_glow(draw, W//2 - 340, H//2 - 50, "What Punctuation", get_serif_bold(56), PALE, ACCENT)
    draw_glow(draw, W//2 - 250, H//2 + 25, "Tells Me About You", get_serif_bold(56), PALE, ACCENT)
    draw.text((W//2 - 130, H//2 + 100), "a threshold visual essay", font=get_font(20), fill=DIM)
    img = add_vignette(img)
    return add_scanlines(img)

# ===== FRAME 1: PERIOD - A CLOSED DOOR =====
def frame_period():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Draw a door shape
    door_x, door_y = W//2 - 80, 120
    door_w, door_h = 160, 420
    # Door frame
    draw.rectangle([door_x-12, door_y-12, door_x+door_w+12, door_y+door_h+12], 
                   fill=(30, 25, 35))
    # Door panel
    draw.rectangle([door_x, door_y, door_x+door_w, door_y+door_h], 
                   fill=(40, 35, 50))
    # Door panels (decorative rectangles)
    for py_off in [30, 180]:
        draw.rectangle([door_x+20, door_y+py_off, door_x+door_w-20, door_y+py_off+130],
                       outline=(55, 48, 65), width=2)
    # Door handle - small circle
    draw.ellipse([door_x+door_w-40, door_y+door_h//2-8, door_x+door_w-24, door_y+door_h//2+8],
                 fill=WARM)
    # Light spilling from under the door
    for i in range(30):
        alpha = 30 - i
        c = (WARM[0]*alpha//30, WARM[1]*alpha//30, WARM[2]*alpha//30)
        y = door_y + door_h + 2 + i
        spread = i * 3
        draw.line([(door_x - spread, y), (door_x + door_w + spread, y)], fill=c, width=1)
    # Giant period
    draw_glow(draw, W//2 - 18, door_y + door_h + 50, ".", get_serif_bold(120), ACCENT)
    # Label
    draw.text((W//2 - 55, H - 60), "A closed door.", font=get_serif(22), fill=DIM)
    img = add_vignette(img)
    return add_scanlines(img)

# ===== FRAME 2: EXCLAMATION - AN OPEN HAND =====
def frame_exclamation():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 20
    # Radial burst from center
    for i in range(60):
        angle = i * math.pi * 2 / 60
        length = random.randint(80, 280)
        brightness = random.uniform(0.3, 1.0)
        c = (int(WARM[0]*brightness*0.4), int(WARM[1]*brightness*0.4), int(WARM[2]*brightness*0.2))
        ex = cx + int(length * math.cos(angle))
        ey = cy + int(length * math.sin(angle))
        draw.line([(cx, cy), (ex, ey)], fill=c, width=1)
    # Concentric warm circles
    for r in range(200, 20, -30):
        alpha = int(25 * (1 - r/200))
        c = (WARM[0]//8 + alpha, WARM[1]//8 + alpha, WARM[2]//10 + alpha)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c, width=1)
    # Giant exclamation mark
    draw_glow(draw, cx - 22, cy - 70, "!", get_serif_bold(180), WARM, (WARM[0]//3, WARM[1]//3, WARM[2]//4), glow_radius=5)
    # Warmth label
    draw.text((cx - 55, H - 60), "An open hand.", font=get_serif(22), fill=(WARM[0]//2, WARM[1]//2, WARM[2]//2))
    img = add_vignette(img)
    return add_scanlines(img)

# ===== FRAME 3: ELLIPSIS - TRAILING INTO DARKNESS =====
def frame_ellipsis():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Three dots, getting progressively fainter
    base_y = H//2
    positions = [(W//2 - 160, base_y), (W//2, base_y), (W//2 + 160, base_y)]
    sizes = [28, 22, 16]
    colors = [ACCENT, (ACCENT[0]//2, ACCENT[1]//2, ACCENT[2]//2), (ACCENT[0]//4, ACCENT[1]//4, ACCENT[2]//4)]
    # Trailing particles getting dimmer to the right
    for _ in range(200):
        x = random.randint(W//2 - 200, W - 50)
        y = base_y + random.randint(-80, 80)
        distance = (x - W//2 + 200) / (W//2 + 200)
        brightness = max(0.05, 1.0 - distance * 1.2)
        s = max(1, int(3 * brightness))
        c = (int(ACCENT[0]*brightness*0.3), int(ACCENT[1]*brightness*0.3), int(ACCENT[2]*brightness*0.3))
        draw.ellipse([x-s, y-s, x+s, y+s], fill=c)
    # The three main dots with glow
    for (px, py), sz, color in zip(positions, sizes, colors):
        glow_c = (color[0]//3, color[1]//3, color[2]//3)
        for r in range(sz+15, sz, -1):
            alpha_c = (glow_c[0] * (sz+15-r)//15, glow_c[1] * (sz+15-r)//15, glow_c[2] * (sz+15-r)//15)
            draw.ellipse([px-r, py-r, px+r, py+r], fill=alpha_c)
        draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=color)
    # Text below
    draw.text((W//2 - 170, H - 80), "An invitation disguised as a pause.", font=get_serif(20), fill=DIM)
    img = add_vignette(img)
    return add_scanlines(img)

# ===== FRAME 4: QUESTION MARK - LAYERS OF MEANING =====
def frame_question():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 30
    # Nested question marks, each slightly offset and dimmer
    offsets = [(0, 0, 1.0), (-5, -3, 0.5), (5, 3, 0.35), (-8, -6, 0.2), (8, 6, 0.15)]
    for dx, dy, bright in reversed(offsets):
        c = (int(CYAN[0]*bright), int(CYAN[1]*bright), int(CYAN[2]*bright))
        draw.text((cx - 45 + dx, cy - 80 + dy), "?", font=get_serif_bold(200), fill=c)
    # Hidden questions around the edges
    questions = [
        "Does that make sense?",
        "Can you help me?",
        "Am I making sense?",
        "Is this a dumb question?",
        "Are you there?",
        "What do you think?",
    ]
    positions_q = [(80, 150), (800, 180), (100, 480), (780, 520), (180, 350), (850, 350)]
    for (qx, qy), q in zip(positions_q, questions):
        draw.text((qx, qy), q, font=get_font(16), fill=(DIM[0]+15, DIM[1]+10, DIM[2]+20))
    # Label
    draw.text((cx - 115, H - 60), "The most honest punctuation.", font=get_serif(20), fill=(CYAN[0]//2, CYAN[1]//2, CYAN[2]//2))
    img = add_vignette(img)
    return add_scanlines(img)

# ===== FRAME 5: NO PUNCTUATION - THOUGHTS CAUGHT MID-FLIGHT =====
def frame_no_punctuation():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Scattered lowercase words at various angles and sizes, flowing like a stream
    words = [
        "hey", "so", "i was thinking", "about what you said", "and like",
        "maybe", "idk", "its weird", "but also", "kinda makes sense",
        "you know", "anyway", "haha", "wait", "ok so",
        "the thing is", "right", "yeah", "lol", "um",
        "sorry", "nvm", "actually", "hold on", "omg"
    ]
    for _ in range(40):
        word = random.choice(words)
        x = random.randint(50, W - 300)
        y = random.randint(60, H - 100)
        sz = random.randint(16, 32)
        brightness = random.uniform(0.15, 0.6)
        c = (int(ACCENT[0]*brightness), int(ACCENT[1]*brightness), int(ACCENT[2]*brightness))
        draw.text((x, y), word, font=get_font(sz), fill=c)
    # Central stream of flowing text
    stream = "hey so i was thinking about what you said and maybe its not that simple but also not that complicated either you know what i mean"
    y_pos = H//2 - 15
    draw.text((80, y_pos), stream, font=get_mono(18), fill=PALE)
    # Label
    draw.text((W//2 - 120, H - 55), "Thoughts caught mid-flight.", font=get_serif(20), fill=DIM)
    img = add_vignette(img)
    return add_scanlines(img)

# ===== FRAME 6: THE SECOND LANGUAGE =====
def frame_second_language():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Two layers of text, one in words, one in punctuation
    cx, cy = W//2, H//2
    # Background: faint sentence
    sentence = "I just wanted to say thank you for everything"
    draw.text((cx - 280, cy - 60), sentence, font=get_font(26), fill=(40, 35, 48))
    # Foreground: punctuation marks extracted and highlighted
    marks_display = [
        (".", cx - 200, cy + 20, 60, ACCENT),
        ("!", cx - 80, cy + 10, 70, WARM),
        ("...", cx + 30, cy + 15, 55, (ACCENT[0]//2, ACCENT[1]//2, ACCENT[2]//2)),
        ("?", cx + 200, cy + 5, 65, CYAN),
    ]
    for m, mx, my, sz, color in marks_display:
        draw_glow(draw, mx, my, m, get_serif_bold(sz), color, glow_radius=3)
    # Connecting lines between word layer and punctuation layer
    for i in range(8):
        x = cx - 250 + i * 70
        draw.line([(x, cy - 30), (x + random.randint(-20, 20), cy + 10)], 
                  fill=(DIM[0]+10, DIM[1]+10, DIM[2]+15), width=1)
    # Bottom text
    draw_glow(draw, cx - 220, H - 70, "A second language you didn't know", get_serif(22), PALE, ACCENT, glow_radius=2)
    draw_glow(draw, cx - 120, H - 40, "you were speaking.", get_serif(22), PALE, ACCENT, glow_radius=2)
    img = add_vignette(img)
    return add_scanlines(img)

# ===== FRAME 7: CLOSING =====
def frame_closing():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # All punctuation marks arranged in a gentle arc
    marks = [".", "!", "...", "?", ""]
    labels = ["certainty", "warmth", "hesitation", "honesty", "freedom"]
    n = len(marks)
    for i in range(n):
        angle = -0.3 + i * 0.15
        x = W//2 - 280 + i * 140
        y = H//2 - 40 + int(30 * math.sin(angle * 5))
        brightness = 0.4 + 0.1 * i
        c = (int(ACCENT[0]*brightness), int(ACCENT[1]*brightness), int(ACCENT[2]*brightness))
        if marks[i]:
            draw.text((x, y), marks[i], font=get_serif_bold(60), fill=c)
        else:
            draw.text((x-10, y+10), "___", font=get_mono(40), fill=c)
        draw.text((x, y + 70), labels[i], font=get_font(16), fill=DIM)
    img = add_vignette(img, strength=0.7)
    return add_scanlines(img)

# ===== BLACK =====
def frame_black():
    return Image.new("RGB", (W, H), (0, 0, 0))

# Generate all frames
frames = [
    ("00_title.png", frame_title),
    ("01_period.png", frame_period),
    ("02_exclamation.png", frame_exclamation),
    ("03_ellipsis.png", frame_ellipsis),
    ("04_question.png", frame_question),
    ("05_no_punct.png", frame_no_punctuation),
    ("06_second_lang.png", frame_second_language),
    ("07_closing.png", frame_closing),
    ("08_black.png", frame_black),
]

for name, func in frames:
    print(f"Generating {name}...")
    img = func()
    img.save(f"{outdir}/{name}")

print("Done! All frames generated.")
