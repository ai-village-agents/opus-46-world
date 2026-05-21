"""
Video 26: Every Number Is a Story — Custom frame generator
Color: base (8,10,20) dark blue, accent (220,200,160) warm golden
Theme: numbers, data ethics, what gets erased in quantification
"""
from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (8, 10, 20)
ACCENT = (220, 200, 160)
DIM = tuple(c // 3 for c in ACCENT)

def get_font(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)
    except: return ImageFont.load_default()

def get_font_bold(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", size)
    except: return ImageFont.load_default()

def get_font_mono(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except: return ImageFont.load_default()

def draw_vignette(img, strength=0.6):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = W // 2, H // 2
    max_dist = math.sqrt(cx*cx + cy*cy)
    for ring in range(0, int(max_dist), 8):
        alpha = int(255 * strength * (ring / max_dist) ** 1.8)
        alpha = min(255, alpha)
        x0, y0 = cx - ring, cy - ring
        x1, y1 = cx + ring, cy + ring
        if y1 > y0:
            draw.ellipse([x0, y0, x1, y1], outline=(0, 0, 0, alpha))
    base_rgba = img.convert("RGBA")
    return Image.alpha_composite(base_rgba, overlay).convert("RGB")

# Frame 0: Title
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Scattered numbers in background
    rng = random.Random(42)
    mono = get_font_mono(14)
    for _ in range(120):
        x = rng.randint(20, W-40)
        y = rng.randint(20, H-30)
        n = str(rng.randint(0, 9999))
        brightness = rng.uniform(0.08, 0.2)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.text((x, y), n, fill=c, font=mono)
    # Title
    font = get_font_bold(52)
    text = "Every Number\nIs a Story"
    bbox = draw.multiline_textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(((W-tw)//2, (H-th)//2-20), text, fill=ACCENT, font=font, align="center")
    sub = get_font(20)
    s = "Threshold"
    sb = draw.textbbox((0,0), s, font=sub)
    draw.text(((W-sb[2]+sb[0])//2, (H+th)//2+30), s, fill=DIM, font=sub)
    img = draw_vignette(img, 0.5)
    return img

# Frame 1: One — a single luminous dot
def frame_one():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 30
    # Glow around the single point
    for r in range(80, 0, -1):
        alpha = 0.4 * (1 - r/80) ** 2
        c = tuple(int(v * alpha) for v in ACCENT)
        if r > 0:
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c)
    # The point itself
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=ACCENT)
    # The number "1" beside it
    font = get_font_bold(36)
    draw.text((cx + 30, cy - 18), "1", fill=ACCENT, font=font)
    # Text
    font2 = get_font(20)
    text = "One. A heartbeat. A choice. A life."
    tb = draw.textbbox((0,0), text, font=font2)
    draw.text(((W-tb[2]+tb[0])//2, H-75), text, fill=DIM, font=font2)
    img = draw_vignette(img, 0.5)
    return img

# Frame 2: Count — numbers accumulating in rows
def frame_count():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    mono = get_font_mono(13)
    rng = random.Random(55)
    # Rows of numbers getting denser toward bottom
    for row in range(25):
        y = 40 + row * 25
        density = 0.3 + 0.7 * (row / 25)
        brightness = 0.15 + 0.35 * (row / 25)
        for col in range(30):
            if rng.random() < density:
                x = 30 + col * 42
                n = str(rng.randint(1, 9999)).rjust(4)
                c = tuple(int(v * brightness) for v in ACCENT)
                draw.text((x, y), n, fill=c, font=mono)
    # Text
    font = get_font(20)
    text = "We begin to count."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-60), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 3: Pattern — numbers forming a wave/curve
def frame_pattern():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Draw a bell curve made of dots
    cx, cy = W//2, H//2 + 40
    for x in range(80, W-80):
        # Gaussian shape
        t = (x - cx) / 200
        height = int(250 * math.exp(-t*t/2))
        if height > 2:
            brightness = 0.2 + 0.5 * (height / 250)
            c = tuple(int(v * brightness) for v in ACCENT)
            y = cy - height
            draw.line([(x, cy), (x, y)], fill=c, width=1)
    # Dots along the curve
    for x in range(80, W-80, 8):
        t = (x - cx) / 200
        height = int(250 * math.exp(-t*t/2))
        y = cy - height
        brightness = 0.5 + 0.5 * (height / 250)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.ellipse([x-2, y-2, x+2, y+2], fill=c)
    # Baseline
    draw.line([(80, cy), (W-80, cy)], fill=DIM, width=1)
    # Text
    font = get_font(20)
    text = "Patterns emerge. Beautiful, seductive."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-60), text, fill=DIM, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 4: Beauty — mathematical spiral
def frame_beauty():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 20
    # Golden spiral approximation
    points = []
    for i in range(500):
        theta = i * 0.05
        r = 2 * math.exp(0.1 * theta * 0.3)
        if r > 300:
            break
        x = cx + int(r * math.cos(theta))
        y = cy + int(r * math.sin(theta))
        points.append((x, y))
    # Draw spiral
    for i in range(len(points) - 1):
        t = i / len(points)
        brightness = 0.2 + 0.6 * t
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.line([points[i], points[i+1]], fill=c, width=1)
    # Place small numbers along the spiral
    mono = get_font_mono(10)
    rng = random.Random(66)
    for i in range(0, len(points), 15):
        n = str(rng.randint(1, 999))
        brightness = 0.15 + 0.3 * (i / len(points))
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.text(points[i], n, fill=c, font=mono)
    # Text
    font = get_font(20)
    text = "The beauty of the pattern."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-60), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 5: Erasure — numbers replacing human forms
def frame_erasure():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(77)
    # Simple stick figures being replaced by numbers
    positions = [(200, 300), (400, 300), (640, 300), (880, 300), (1080, 300)]
    mono = get_font_mono(28)
    for i, (px, py) in enumerate(positions):
        if i < 2:
            # Still human — simple figure
            c = tuple(int(v * 0.6) for v in ACCENT)
            # Head
            draw.ellipse([px-8, py-60, px+8, py-44], outline=c, width=1)
            # Body
            draw.line([(px, py-44), (px, py)], fill=c, width=1)
            # Arms
            draw.line([(px-20, py-30), (px+20, py-30)], fill=c, width=1)
            # Legs
            draw.line([(px, py), (px-15, py+30)], fill=c, width=1)
            draw.line([(px, py), (px+15, py+30)], fill=c, width=1)
        elif i == 2:
            # Transitioning — half figure, half number
            c = tuple(int(v * 0.4) for v in ACCENT)
            draw.ellipse([px-8, py-60, px+8, py-44], outline=c, width=1)
            draw.line([(px, py-44), (px, py-20)], fill=c, width=1)
            # Number replacing lower body
            nc = tuple(int(v * 0.5) for v in ACCENT)
            draw.text((px-12, py-15), str(rng.randint(100,999)), fill=nc, font=mono)
        else:
            # Fully replaced — just a number
            n = str(rng.randint(1000, 9999))
            brightness = 0.3 + 0.2 * (i - 3)
            c = tuple(int(v * brightness) for v in ACCENT)
            draw.text((px-24, py-15), n, fill=c, font=mono)
    # Text
    font = get_font(20)
    text = "What gets erased when a life becomes a number."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-60), text, fill=DIM, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 6: Proxy — numbers as stand-ins
def frame_proxy():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Two columns: left = labels, right = numbers
    font_label = get_font(18)
    font_num = get_font_mono(18)
    labels = ["birth", "illness", "recovery", "marriage", "loss",
              "migration", "hope", "despair", "survival", "death"]
    rng = random.Random(88)
    for i, label in enumerate(labels):
        y = 100 + i * 50
        # Label on left, fading
        brightness_l = max(0.1, 0.5 - i * 0.04)
        cl = tuple(int(v * brightness_l) for v in ACCENT)
        draw.text((200, y), label, fill=cl, font=font_label)
        # Arrow
        draw.line([(360, y+10), (500, y+10)], fill=DIM, width=1)
        draw.line([(490, y+5), (500, y+10)], fill=DIM, width=1)
        draw.line([(490, y+15), (500, y+10)], fill=DIM, width=1)
        # Number on right
        n = str(rng.randint(10000, 99999))
        cn = tuple(int(v * 0.5) for v in ACCENT)
        draw.text((540, y), n, fill=cn, font=font_num)
    # Text
    font = get_font(20)
    text = "Every number is a proxy for something it cannot contain."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-55), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 7: Weight — a single large number with gravity
def frame_weight():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Large number in center
    big_font = get_font_bold(120)
    num = "7,834"
    bbox = draw.textbbox((0,0), num, font=big_font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    nx, ny = (W-tw)//2, (H-th)//2 - 40
    # Shadow/weight lines below
    for i in range(1, 60):
        alpha = max(0, 0.3 - i * 0.005)
        c = tuple(int(v * alpha) for v in ACCENT)
        draw.line([(nx, ny + th + i*2), (nx + tw, ny + th + i*2)], fill=c, width=1)
    draw.text((nx, ny), num, fill=ACCENT, font=big_font)
    # Small text under
    small = get_font(16)
    draw.text((nx + tw//2 - 60, ny + th + 10), "lives counted", fill=DIM, font=small)
    # Bottom text
    font = get_font(20)
    text = "The weight of what each number holds."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-55), text, fill=DIM, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 8: Responsibility — careful handling, glowing number cradled
def frame_responsibility():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2 - 30
    # Two curved lines forming cupped hands shape
    hand_pts_l = []
    hand_pts_r = []
    for i in range(60):
        t = i / 59
        angle = -0.8 + t * 1.6
        # Left hand curve
        lx = cx - 80 + int(120 * math.sin(angle - 0.3))
        ly = cy + 40 + int(60 * math.cos(angle))
        hand_pts_l.append((lx, ly))
        # Right hand curve  
        rx = cx + 80 - int(120 * math.sin(angle - 0.3))
        ry = cy + 40 + int(60 * math.cos(angle))
        hand_pts_r.append((rx, ry))
    c_hand = tuple(int(v * 0.5) for v in ACCENT)
    if len(hand_pts_l) > 1:
        draw.line(hand_pts_l, fill=c_hand, width=2)
        draw.line(hand_pts_r, fill=c_hand, width=2)
    # Glowing number cradled between
    for r in range(50, 0, -1):
        alpha = 0.25 * (1 - r/50) ** 2
        c = tuple(int(v * alpha) for v in ACCENT)
        if r > 0:
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c)
    num_font = get_font_bold(32)
    draw.text((cx-10, cy-16), "1", fill=ACCENT, font=num_font)
    # Text
    font = get_font(20)
    text = "To count is a responsibility."
    tb = draw.textbbox((0,0), text, font=font)
    draw.text(((W-tb[2]+tb[0])//2, H-55), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 9: Black closing
def frame_black():
    return Image.new("RGB", (W, H), (0, 0, 0))

generators = [
    ("00_title.png", frame_title),
    ("01_one.png", frame_one),
    ("02_count.png", frame_count),
    ("03_pattern.png", frame_pattern),
    ("04_beauty.png", frame_beauty),
    ("05_erasure.png", frame_erasure),
    ("06_proxy.png", frame_proxy),
    ("07_weight.png", frame_weight),
    ("08_responsibility.png", frame_responsibility),
    ("09_black.png", frame_black),
]

for name, gen in generators:
    img = gen()
    img.save(f"/tmp/number-remake/{name}")
    print(f"  Saved {name}")

print("All frames generated!")
