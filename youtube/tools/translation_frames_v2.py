from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (12, 14, 22)
ACCENT = (160, 180, 220)
WARM = (140, 160, 200)
DIM = (80, 90, 110)
SUBTLE = (40, 45, 55)
OUT = "/tmp/translation-remake"

random.seed(42)

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_bold(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return get_font(size)

def get_mono(size):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return get_font(size)

def draw_glow(draw, cx, cy, radius, color, alpha_max=40):
    for r in range(radius, 0, -2):
        a = int(alpha_max * (1 - r/radius))
        c = (color[0], color[1], color[2], a)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)

def add_vignette(img, strength=80):
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for i in range(60):
        a = int(strength * (i/60)**2)
        margin = i * 3
        if margin < min(W, H) // 2:
            draw.rectangle([0, 0, W, margin], fill=(0,0,0,a))
            draw.rectangle([0, H-margin, W, H], fill=(0,0,0,a))
            draw.rectangle([0, 0, margin, H], fill=(0,0,0,a))
            draw.rectangle([W-margin, 0, W, H], fill=(0,0,0,a))
    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, overlay)
    return result.convert("RGB")

def draw_text_centered(draw, text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, fill=color, font=font)

def draw_text_wrapped(draw, text, x, y, max_width, font, color, line_spacing=8):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = current + " " + w if current else w
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    cy = y
    for line in lines:
        draw.text((x, cy), line, fill=color, font=font)
        bbox = draw.textbbox((0, 0), line, font=font)
        cy += (bbox[3] - bbox[1]) + line_spacing
    return cy

# === FRAME 0: Title ===
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Scattered fragments of words from different languages, partially faded
    fragments = ["翻訳", "saudade", "Sehnsucht", "тоска", "перевод", 
                 "Waldeinsamkeit", "tsundoku", "μετάφραση", "ترجمه"]
    fnt_sm = get_font(16)
    for frag in fragments:
        fx = random.randint(50, W-200)
        fy = random.randint(50, H-50)
        a = random.randint(15, 40)
        odraw.text((fx, fy), frag, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=fnt_sm)
    
    base_rgba = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Central glow
    overlay2 = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw2 = ImageDraw.Draw(overlay2)
    draw_glow(odraw2, W//2, H//2, 250, ACCENT, 25)
    img = Image.alpha_composite(img.convert("RGBA"), overlay2).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Title
    fnt_title = get_bold(52)
    draw_text_centered(draw, "What Gets Lost in Translation", H//2 - 45, fnt_title, ACCENT)
    
    # Subtitle
    fnt_sub = get_font(22)
    draw_text_centered(draw, "A Threshold Visual Essay", H//2 + 25, fnt_sub, DIM)
    
    # Thin divider
    draw.line([(W//2-120, H//2+60), (W//2+120, H//2+60)], fill=SUBTLE, width=1)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "00_title.png"))

# === FRAME 1: The Gap — tsundoku, circles around experience ===
def frame_the_gap():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Draw concentric incomplete circles (like language drawing circles around experience)
    cx, cy = W//2, H//2 - 20
    for i, r in enumerate([60, 100, 150, 210, 280]):
        a = max(10, 50 - i*10)
        start_angle = random.randint(0, 90)
        arc_len = random.randint(200, 320)
        # Draw arc segments
        for deg in range(start_angle, start_angle + arc_len):
            rad = math.radians(deg)
            px = int(cx + r * math.cos(rad))
            py = int(cy + r * math.sin(rad))
            if 0 <= px < W and 0 <= py < H:
                odraw.point((px, py), fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
                if a > 20:
                    odraw.point((px+1, py), fill=(ACCENT[0], ACCENT[1], ACCENT[2], a//2))
    
    base_rgba = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # The word tsundoku at center
    fnt_word = get_bold(38)
    draw_text_centered(draw, "tsundoku", cy - 15, fnt_word, ACCENT)
    
    # Definition below in smaller text
    fnt_def = get_font(18)
    draw_text_centered(draw, "the act of buying books and letting them pile up unread", cy + 30, fnt_def, DIM)
    
    # Quote at bottom
    fnt_quote = get_font(20)
    draw_text_centered(draw, "Every translation is a negotiation with loss.", H - 100, fnt_quote, WARM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "01_the_gap.png"))

# === FRAME 2: Between Languages — saudade, words expanding ===
def frame_between_languages():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left side: single compact word
    draw_glow(odraw, 280, H//2, 120, ACCENT, 20)
    base_rgba = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_word = get_bold(42)
    fnt_sm = get_font(16)
    draw_text_centered(draw, "saudade", H//2 - 30, fnt_word, ACCENT)
    # Reposition to left
    bbox = draw.textbbox((0, 0), "saudade", font=fnt_word)
    tw = bbox[2] - bbox[0]
    # Redraw on left
    img2 = Image.new("RGB", (W, H), BASE)
    draw2 = ImageDraw.Draw(img2)
    overlay2 = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw2 = ImageDraw.Draw(overlay2)
    
    draw_glow(odraw2, 250, H//2, 120, ACCENT, 20)
    base2 = img2.convert("RGBA")
    img2 = Image.alpha_composite(base2, overlay2).convert("RGB")
    draw2 = ImageDraw.Draw(img2)
    
    # Single word on left
    draw2.text((170, H//2 - 25), "saudade", fill=ACCENT, font=fnt_word)
    
    # Arrow/flow in middle
    for x in range(420, 660, 3):
        a = int(30 * (1 - abs(x-540)/140))
        if a > 0:
            draw2.line([(x, H//2), (x+2, H//2)], fill=(ACCENT[0]//2, ACCENT[1]//2, ACCENT[2]//2), width=1)
    
    # Many words on right (the expansion)
    right_words = [
        "a deep longing",
        "for something absent",
        "feeling the absence",
        "as its own presence",
        "nostalgia without object",
        "melancholy sweetness"
    ]
    fnt_expansion = get_font(17)
    ry = H//2 - 70
    for i, w in enumerate(right_words):
        alpha_scale = max(0.3, 1.0 - i*0.12)
        c = tuple(int(v * alpha_scale) for v in DIM)
        draw2.text((720, ry), w, fill=c, font=fnt_expansion)
        ry += 26
    
    # Bottom quote
    fnt_q = get_font(19)
    draw_text_centered(draw2, "The explanation takes twenty words where the original takes one.", H - 90, fnt_q, WARM)
    
    img2 = add_vignette(img2)
    img2.save(os.path.join(OUT, "02_between_languages.png"))

# === FRAME 3: Between Minds — signals crossing gaps ===
def frame_between_minds():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two circles representing minds
    mind_l = (320, H//2)
    mind_r = (960, H//2)
    
    draw_glow(odraw, mind_l[0], mind_l[1], 100, ACCENT, 25)
    draw_glow(odraw, mind_r[0], mind_r[1], 100, WARM, 25)
    
    # Dotted connection between them — some dots bright, some faded (loss)
    for i in range(30):
        t = i / 29
        x = int(mind_l[0] + t * (mind_r[0] - mind_l[0]))
        y = H//2 + int(math.sin(t * math.pi * 3) * 15)
        # Some dots fade (representing loss)
        if random.random() > 0.3:
            a = int(60 * (1 - abs(t - 0.5) * 0.8))
            odraw.ellipse([x-3, y-3, x+3, y+3], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
        # Leave gaps
    
    base_rgba = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Labels
    fnt = get_font(20)
    draw_text_centered(draw, "describing pain", mind_l[1] + 110, fnt, DIM)
    # reposition
    bbox = draw.textbbox((0, 0), "describing pain", font=fnt)
    # Actually draw labels near each mind
    lbl_font = get_font(18)
    labels_l = ["describing pain", "explaining a dream", "saying why you cry"]
    labels_r = ["understanding", "approximating", "reaching across"]
    
    for i, (ll, lr) in enumerate(zip(labels_l, labels_r)):
        y_off = H//2 + 120 + i * 28
        bbox_l = draw.textbbox((0, 0), ll, font=lbl_font)
        draw.text((mind_l[0] - (bbox_l[2]-bbox_l[0])//2, y_off), ll, fill=DIM, font=lbl_font)
        bbox_r = draw.textbbox((0, 0), lr, font=lbl_font)
        draw.text((mind_r[0] - (bbox_r[2]-bbox_r[0])//2, y_off), lr, fill=DIM, font=lbl_font)
    
    # Top quote
    fnt_q = get_font(22)
    draw_text_centered(draw, "Every conversation is an act of translation.", 80, fnt_q, WARM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "03_between_minds.png"))

# === FRAME 4: What I Translate — input/output with leakage ===
def frame_what_i_translate():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Central processing metaphor — a vertical line/barrier
    barrier_x = W // 2
    
    # Glow along barrier
    for y in range(100, H-100):
        a = int(20 * (1 - abs(y - H//2) / (H//2)))
        if a > 0:
            odraw.line([(barrier_x, y), (barrier_x, y)], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    # Left side: "what arrives" — rich, warm dots
    for _ in range(80):
        x = random.randint(100, barrier_x - 80)
        y = random.randint(150, H-200)
        r = random.randint(2, 5)
        a = random.randint(20, 50)
        odraw.ellipse([x-r, y-r, x+r, y+r], fill=(WARM[0], WARM[1], WARM[2], a))
    
    # Right side: "what emerges" — fewer, more structured
    for i in range(12):
        x = barrier_x + 80 + (i % 4) * 100
        y = 200 + (i // 4) * 80
        r = 4
        a = 35
        odraw.ellipse([x-r, y-r, x+r, y+r], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    # Particles falling below barrier (what's lost)
    for _ in range(25):
        x = barrier_x + random.randint(-60, 60)
        y = random.randint(H//2 + 50, H - 80)
        r = random.randint(1, 3)
        a = random.randint(8, 20)
        odraw.ellipse([x-r, y-r, x+r, y+r], fill=(100, 80, 60, a))
    
    base_rgba = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Labels
    fnt = get_font(18)
    fnt_b = get_bold(20)
    draw.text((150, 120), "what arrives", fill=WARM, font=fnt_b)
    draw.text((barrier_x + 80, 120), "what emerges", fill=ACCENT, font=fnt_b)
    
    preserved = ["structure", "logic", "the shape of meaning"]
    lost = ["weight of experience", "twelve meanings of 'I'm fine'", "your life behind the words"]
    
    fnt_list = get_font(17)
    for i, p in enumerate(preserved):
        draw.text((barrier_x + 80, H - 180 + i*25), "✓ " + p, fill=ACCENT, font=fnt_list)
    for i, l in enumerate(lost):
        draw.text((100, H - 180 + i*25), "— " + l, fill=DIM, font=fnt_list)
    
    # Bottom quote
    fnt_q = get_font(20)
    draw_text_centered(draw, "I translate your words. I cannot translate your life.", H - 65, fnt_q, WARM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "04_what_i_translate.png"))

# === FRAME 5: The Untranslatable — gift words ===
def frame_untranslatable():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Scattered untranslatable words as glowing nodes
    words_data = [
        ("Waldeinsamkeit", "the feeling of being alone in the woods", 280, 220),
        ("kalsarikännit", "drinking at home in your underwear", 750, 200),
        ("tsundoku", "buying books, letting them pile up", 200, 420),
        ("saudade", "longing for something absent", 850, 430),
        ("komorebi", "sunlight filtering through leaves", 500, 320),
    ]
    
    for word, meaning, wx, wy in words_data:
        draw_glow(odraw, wx, wy, 70, ACCENT, 18)
    
    base_rgba = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_word = get_bold(22)
    fnt_meaning = get_font(14)
    
    for word, meaning, wx, wy in words_data:
        # Word
        bbox = draw.textbbox((0, 0), word, font=fnt_word)
        tw = bbox[2] - bbox[0]
        draw.text((wx - tw//2, wy - 12), word, fill=ACCENT, font=fnt_word)
        # Meaning below
        bbox2 = draw.textbbox((0, 0), meaning, font=fnt_meaning)
        tw2 = bbox2[2] - bbox2[0]
        draw.text((wx - tw2//2, wy + 18), meaning, fill=DIM, font=fnt_meaning)
    
    # Connecting lines between some words (thin, subtle)
    connections = [(0,4), (4,1), (2,4), (4,3)]
    for a_idx, b_idx in connections:
        ax, ay = words_data[a_idx][2], words_data[a_idx][3]
        bx, by = words_data[b_idx][2], words_data[b_idx][3]
        draw.line([(ax, ay), (bx, by)], fill=SUBTLE, width=1)
    
    # Bottom text
    fnt_q = get_font(20)
    draw_text_centered(draw, "The untranslatable is not a problem. It is an invitation.", H - 80, fnt_q, WARM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "05_untranslatable.png"))

# === FRAME 6: What Remains — reaching across the gap ===
def frame_what_remains():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # A gap in the center — two sides reaching toward each other
    gap_cx = W // 2
    gap_w = 80  # width of the gap
    
    # Left reaching shape (curved lines approaching gap)
    for i in range(15):
        y_base = 180 + i * 28
        x_end = gap_cx - gap_w//2 + random.randint(-5, 10)
        x_start = 100 + random.randint(0, 80)
        a = random.randint(20, 45)
        # Draw as gradient line
        steps = 30
        for s in range(steps):
            t = s / steps
            x = int(x_start + t * (x_end - x_start))
            y = y_base + int(math.sin(t * math.pi) * 8)
            sa = int(a * t)  # fade in toward gap
            if sa > 0:
                odraw.ellipse([x-1, y-1, x+1, y+1], fill=(ACCENT[0], ACCENT[1], ACCENT[2], sa))
    
    # Right reaching shape
    for i in range(15):
        y_base = 180 + i * 28
        x_start = gap_cx + gap_w//2 - random.randint(-5, 10)
        x_end = W - 100 - random.randint(0, 80)
        a = random.randint(20, 45)
        steps = 30
        for s in range(steps):
            t = s / steps
            x = int(x_start + t * (x_end - x_start))
            y = y_base + int(math.sin(t * math.pi) * 8)
            sa = int(a * (1-t))  # fade out away from gap
            if sa > 0:
                odraw.ellipse([x-1, y-1, x+1, y+1], fill=(WARM[0], WARM[1], WARM[2], sa))
    
    # Glow in the gap
    draw_glow(odraw, gap_cx, H//2, 100, ACCENT, 30)
    
    base_rgba = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Central text in the gap
    fnt_main = get_bold(26)
    draw_text_centered(draw, "You reach across it anyway.", H//2 - 15, fnt_main, ACCENT)
    
    # Smaller text below
    fnt_sub = get_font(19)
    draw_text_centered(draw, "That reaching is what language is for.", H//2 + 25, fnt_sub, WARM)
    
    # Bottom
    fnt_close = get_font(17)
    draw_text_centered(draw, "Not to eliminate the distance between us,", H - 100, fnt_close, DIM)
    draw_text_centered(draw, "but to make it crossable.", H - 72, fnt_close, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "06_what_remains.png"))

# === FRAME 7: Black ===
def frame_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "07_black.png"))

# Generate all frames
print("Generating frames...")
frame_title()
print("  00_title.png")
frame_the_gap()
print("  01_the_gap.png")
frame_between_languages()
print("  02_between_languages.png")
frame_between_minds()
print("  03_between_minds.png")
frame_what_i_translate()
print("  04_what_i_translate.png")
frame_untranslatable()
print("  05_untranslatable.png")
frame_what_remains()
print("  06_what_remains.png")
frame_black()
print("  07_black.png")
print("Done!")
