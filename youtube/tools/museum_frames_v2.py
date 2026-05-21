from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (10, 12, 18)
ACCENT = (140, 160, 200)
DIM = (70, 80, 100)
VDIM = (40, 45, 55)

def get_font(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)
    except: return ImageFont.load_default()

def get_mono(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except: return ImageFont.load_default()

def get_bold(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", size)
    except: return get_font(size)

def draw_vignette(img, strength=80):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = W // 2, H // 2
    max_dist = math.sqrt(cx**2 + cy**2)
    for ring in range(0, int(max_dist), 3):
        alpha = int(strength * (ring / max_dist) ** 2)
        if alpha > 0 and cy + ring >= cy - ring:
            draw.ellipse([cx-ring, cy-ring, cx+ring, cy+ring], outline=(0, 0, 0, min(alpha, 255)))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

random.seed(55)

def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    for i in range(260, 0, -2):
        frac = 1 - i/260
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.15)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_bold(44)
    title = "The Museum of Almost"
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy-30), title, fill=ACCENT, font=f)
    f2 = get_font(18)
    sub = "a threshold visual essay"
    bbox2 = draw.textbbox((0, 0), sub, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, cy+30), sub, fill=DIM, font=f2)
    return draw_vignette(img)

def frame_doorways():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Multiple doorway shapes receding
    for i in range(6):
        inset = 60 + i * 80
        alpha = 0.3 - i * 0.04
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        x1, y1 = inset, 40 + i * 15
        x2, y2 = W - inset, H - 20 - i * 10
        draw.rectangle([x1, y1, x2, y2], outline=c, width=2)
    # Light at the end
    cx, cy = W//2, H//2
    for i in range(40, 0, -1):
        frac = 1 - i/40
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.4)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    return draw_vignette(img, 90)

def frame_different():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(22)
    text = "what if this museum collected"
    text2 = "only the things that almost happened?"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2-30), text, fill=DIM, font=f)
    bbox2 = draw.textbbox((0, 0), text2, font=f)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, H//2+10), text2, fill=ACCENT, font=f)
    return draw_vignette(img, 90)

def frame_museum():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Museum floor plan - rectangles as rooms
    rooms = [(100,100,300,280), (350,100,550,280), (600,100,800,280),
             (100,340,300,520), (350,340,550,520), (600,340,800,520),
             (850,100,1050,520)]
    labels = ["Almost Said", "Nearly Done", "Just Missed", "Half-Formed",
              "The Pause", "What If", "Exit Through\nthe Possible"]
    f = get_mono(12)
    for i, (r, label) in enumerate(zip(rooms, labels)):
        alpha = 0.08 + random.uniform(0, 0.08)
        c_fill = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
        draw.rectangle(r, fill=c_fill, outline=VDIM)
        cx = (r[0] + r[2]) // 2
        cy = (r[1] + r[3]) // 2
        c = tuple(int(ACCENT[j] * 0.4) for j in range(3))
        draw.text((r[0]+10, r[1]+10), label, fill=c, font=f)
    f2 = get_bold(18)
    draw.text((W-350, H-60), "floor plan: Museum of Almost", fill=DIM, font=f2)
    return draw_vignette(img, 80)

def frame_ghosts():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Ghost-like transparent shapes
    for _ in range(15):
        x = random.randint(100, W-100)
        y = random.randint(80, H-80)
        r = random.randint(30, 80)
        alpha = random.uniform(0.04, 0.1)
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
        # Tall oval (person-like)
        draw.ellipse([x-r//2, y-r, x+r//2, y+r], fill=c)
    f = get_font(18)
    text = "the ghosts of things that almost were"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H-70), text, fill=DIM, font=f)
    return draw_vignette(img, 90)

def frame_thought():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Thought bubble that's incomplete
    cx, cy = W//2, H//2 - 40
    # Main bubble (dashed)
    for angle_deg in range(0, 360, 4):
        angle = math.radians(angle_deg)
        x = cx + int(180 * math.cos(angle))
        y = cy + int(100 * math.sin(angle))
        if (angle_deg // 12) % 2 == 0:
            c = tuple(int(ACCENT[j] * 0.25) for j in range(3))
            draw.ellipse([x-2, y-2, x+2, y+2], fill=c)
    # Trailing dots
    for i in range(3):
        dx = cx - 100 + i * 30
        dy = cy + 140 + i * 25
        r = 8 - i * 2
        c = tuple(int(ACCENT[j] * (0.2 - i*0.05)) for j in range(3))
        draw.ellipse([dx-r, dy-r, dx+r, dy+r], fill=c)
    f = get_font(18)
    text = "the thought that almost formed"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy), text, fill=DIM, font=f)
    return draw_vignette(img, 90)

def frame_columns():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Museum columns
    for i in range(7):
        x = 100 + i * 170
        # Column
        alpha = 0.1 + 0.05 * abs(3 - i)
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
        draw.rectangle([x-12, 80, x+12, H-80], fill=c)
        # Capital
        draw.rectangle([x-20, 70, x+20, 85], fill=c)
        draw.rectangle([x-20, H-85, x+20, H-70], fill=c)
    # Display cases between columns (small rectangles)
    for i in range(6):
        x = 185 + i * 170
        y = H//2
        c = tuple(int(ACCENT[j] * 0.08) for j in range(3))
        draw.rectangle([x-30, y-20, x+30, y+20], fill=c, outline=VDIM)
    return draw_vignette(img, 80)

def frame_forget():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Fading text
    f = get_font(20)
    items = [
        "the name you almost remembered",
        "the song you almost recalled",
        "the dream that dissolved at waking",
        "the connection you almost made",
        "the idea that was on the tip of your tongue"
    ]
    for i, item in enumerate(items):
        y = 120 + i * 90
        alpha = 0.6 - i * 0.1
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((150, y), item, fill=c, font=f)
    return draw_vignette(img, 80)

def frame_alternatives():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Branching paths
    cx = 100
    cy = H // 2
    draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=DIM)
    for i in range(5):
        angle = -40 + i * 20
        rad = math.radians(angle)
        x2 = cx + int(900 * math.cos(rad))
        y2 = cy + int(900 * math.sin(rad))
        alpha = 0.15 if i != 2 else 0.35
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        width = 1 if i != 2 else 2
        draw.line([(cx, cy), (x2, y2)], fill=c, width=width)
        # Label at end
        if i == 2:
            f = get_font(14)
            draw.text((x2 - 80, y2 - 10), "chosen", fill=DIM, font=f)
        else:
            f = get_mono(11)
            draw.text((min(x2, W-80), max(10, min(y2, H-20))), "almost", fill=VDIM, font=f)
    return draw_vignette(img, 80)

def frame_ghosts_decision():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # A decision point with ghostly alternate outcomes
    cx, cy = W//2, H//2
    # Central node
    for i in range(25, 0, -1):
        frac = 1 - i/25
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.5)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    # Ghost paths
    for angle_deg in range(0, 360, 45):
        rad = math.radians(angle_deg)
        for dist in range(40, 300, 5):
            x = cx + int(dist * math.cos(rad))
            y = cy + int(dist * math.sin(rad))
            alpha = 0.12 * (1 - dist/300)
            c = tuple(int(ACCENT[j] * alpha) for j in range(3))
            draw.ellipse([x-1, y-1, x+1, y+1], fill=c)
    f = get_font(16)
    text = "every decision haunted by its alternatives"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H-60), text, fill=DIM, font=f)
    return draw_vignette(img, 80)

def frame_inside():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Interior of museum - perspective lines
    cx, cy = W//2, H//3
    # Floor lines
    for i in range(-8, 9):
        x_bottom = W//2 + i * 100
        draw.line([(cx, cy), (x_bottom, H)], fill=VDIM, width=1)
    # Horizontal lines
    for i in range(5):
        y = cy + int((H - cy) * (i/5)**0.7)
        left = cx - int((W//2) * (i/5))
        right = cx + int((W//2) * (i/5))
        draw.line([(left, y), (right, y)], fill=VDIM, width=1)
    # Vanishing point glow
    for i in range(30, 0, -1):
        frac = 1 - i/30
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.3)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    return draw_vignette(img, 80)

def frame_pedestals():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Empty pedestals
    items = [
        (200, "the word\nyou swallowed"),
        (450, "the hand\nyou didn't take"),
        (700, "the door\nyou walked past"),
        (950, "the truth\nyou almost spoke"),
    ]
    f = get_mono(12)
    for x, label in items:
        # Pedestal
        c = tuple(int(ACCENT[j] * 0.15) for j in range(3))
        draw.rectangle([x-40, H//2, x+40, H//2+80], fill=c)
        draw.rectangle([x-50, H//2+80, x+50, H//2+90], fill=c)
        # Empty top (just a faint glow where exhibit should be)
        for i in range(20, 0, -1):
            frac = 1 - i/20
            gc = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.1)) for j in range(3))
            draw.ellipse([x-i, H//2-30-i, x+i, H//2-30+i], fill=gc)
        # Label
        c2 = tuple(int(ACCENT[j] * 0.35) for j in range(3))
        draw.text((x-40, H//2+100), label, fill=c2, font=f)
    return draw_vignette(img, 80)

def frame_laugh():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(22)
    text = "the laugh you almost laughed"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2-60), text, fill=ACCENT, font=f)
    f2 = get_font(18)
    text2 = "still echoes somewhere"
    bbox2 = draw.textbbox((0, 0), text2, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, H//2+10), text2, fill=DIM, font=f2)
    # Faint ripples
    cx, cy = W//2, H//2 + 80
    for r in range(20, 200, 30):
        alpha = 0.1 * (1 - r/200)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.ellipse([cx-r, cy-r//3, cx+r, cy+r//3], outline=c, width=1)
    return draw_vignette(img, 90)

def frame_question():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Large question mark
    f = get_bold(200)
    text = "?"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    c = tuple(int(ACCENT[j] * 0.12) for j in range(3))
    draw.text(((W-tw)//2, (H-th)//2 - 40), text, fill=c, font=f)
    f2 = get_font(18)
    text2 = "what almost happened to you today?"
    bbox2 = draw.textbbox((0, 0), text2, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, H - 100), text2, fill=DIM, font=f2)
    return draw_vignette(img, 90)

def frame_chose():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # One bright path among many dim ones
    cx, cy = W//2, H
    for angle_deg in range(-80, 81, 8):
        rad = math.radians(angle_deg)
        x2 = cx + int(700 * math.sin(rad))
        y2 = cy - int(700 * math.cos(rad))
        if abs(angle_deg) < 5:
            alpha = 0.4
            width = 2
        else:
            alpha = 0.06
            width = 1
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.line([(cx, cy), (x2, y2)], fill=c, width=width)
    return draw_vignette(img, 80)

def frame_almosts():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Many small "almost" scattered
    f = get_font(14)
    for _ in range(60):
        x = random.randint(20, W-80)
        y = random.randint(20, H-30)
        alpha = random.uniform(0.1, 0.4)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((x, y), "almost", fill=c, font=f)
    return draw_vignette(img, 90)

def frame_ending():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    for i in range(200, 0, -2):
        frac = 1 - i/200
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.18)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_font(20)
    text = "the almost-things shape us"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy-30), text, fill=ACCENT, font=f)
    f2 = get_font(18)
    text2 = "as much as the things that arrive"
    bbox2 = draw.textbbox((0, 0), text2, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, cy+10), text2, fill=DIM, font=f2)
    return draw_vignette(img, 90)

def frame_end():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(16)
    text = "threshold visual essays"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2 - 10), text, fill=VDIM, font=f)
    return draw_vignette(img, 100)

frames = [
    ("00_title", frame_title), ("01_doorways", frame_doorways),
    ("02_different", frame_different), ("03_museum", frame_museum),
    ("04_ghosts", frame_ghosts), ("05_thought", frame_thought),
    ("06_columns", frame_columns), ("07_forget", frame_forget),
    ("08_alternatives", frame_alternatives), ("09_ghosts_decision", frame_ghosts_decision),
    ("10_inside", frame_inside), ("11_pedestals", frame_pedestals),
    ("12_laugh", frame_laugh), ("13_question", frame_question),
    ("14_chose", frame_chose), ("15_almosts", frame_almosts),
    ("16_ending", frame_ending), ("17_end", frame_end),
]

out_dir = "/tmp/museum-remake"
for name, func in frames:
    path = f"{out_dir}/{name}.png"
    img = func()
    img.save(path)
    print(f"Saved {path}")
print(f"\nDone! {len(frames)} frames generated.")
