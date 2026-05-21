"""
Video 27: The Map Is Not the Territory — Custom frame generator
Color: base (15,12,8) warm dark, accent (200,130,80) warm amber
Theme: maps vs reality, simplification, what gets left out
"""
from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (15, 12, 8)
ACCENT = (200, 130, 80)
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

def draw_grid(draw, spacing=60, color=None, offset_x=0, offset_y=0, fade=False):
    """Draw a cartographic grid"""
    if color is None:
        color = DIM
    for x in range(offset_x % spacing, W, spacing):
        alpha_factor = 1.0
        if fade:
            dist = abs(x - W//2) / (W//2)
            alpha_factor = max(0, 1.0 - dist * 0.7)
        c = tuple(int(v * alpha_factor) for v in color)
        draw.line([(x, 0), (x, H)], fill=c, width=1)
    for y in range(offset_y % spacing, H, spacing):
        alpha_factor = 1.0
        if fade:
            dist = abs(y - H//2) / (H//2)
            alpha_factor = max(0, 1.0 - dist * 0.7)
        c = tuple(int(v * alpha_factor) for v in color)
        draw.line([(0, y), (W, y)], fill=c, width=1)

def draw_contour_lines(draw, seed=42, color=None, num_lines=8):
    """Draw organic contour/topographic lines"""
    if color is None:
        color = ACCENT
    rng = random.Random(seed)
    for i in range(num_lines):
        y_base = 80 + i * (H - 160) // num_lines
        points = []
        for x in range(0, W + 20, 20):
            y = y_base + int(40 * math.sin(x * 0.008 + i * 1.3) + 25 * math.sin(x * 0.015 + i * 0.7))
            y += rng.randint(-8, 8)
            points.append((x, y))
        if len(points) > 1:
            fade_factor = 0.3 + 0.7 * (i / num_lines)
            c = tuple(int(v * fade_factor) for v in color)
            draw.line(points, fill=c, width=1)

def draw_river(draw, seed=99):
    """Draw a flowing river shape"""
    rng = random.Random(seed)
    # Main river path
    points_left = []
    points_right = []
    for y in range(0, H + 10, 5):
        x_center = W // 2 + int(120 * math.sin(y * 0.006) + 60 * math.sin(y * 0.013 + 1.5))
        width = 20 + int(15 * math.sin(y * 0.01 + 0.5))
        points_left.append((x_center - width, y))
        points_right.append((x_center + width, y))
    
    # Draw river body
    for i in range(len(points_left) - 1):
        lx0, ly0 = points_left[i]
        lx1, ly1 = points_left[i+1]
        rx0, ry0 = points_right[i]
        rx1, ry1 = points_right[i+1]
        # Fill between left and right
        for y in range(ly0, ly1 + 1):
            t = (y - ly0) / max(1, ly1 - ly0)
            xl = int(lx0 + t * (lx1 - lx0))
            xr = int(rx0 + t * (rx1 - rx0))
            brightness = 0.4 + 0.3 * math.sin(y * 0.02)
            c = tuple(int(v * brightness) for v in ACCENT)
            draw.line([(xl, y), (xr, y)], fill=c)

# Frame 0: Title
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Subtle grid in background
    grid_c = tuple(max(0, b + 8) for b in BASE)
    draw_grid(draw, spacing=50, color=grid_c)
    # Title
    font = get_font_bold(52)
    text = "The Map Is Not\nthe Territory"
    bbox = draw.multiline_textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(((W - tw) // 2, (H - th) // 2 - 20), text, fill=ACCENT, font=font, align="center")
    # Subtitle
    sub_font = get_font(20)
    sub = "Threshold"
    sb = draw.textbbox((0, 0), sub, font=sub_font)
    draw.text(((W - sb[2] + sb[0]) // 2, (H + th) // 2 + 30), sub, fill=DIM, font=sub_font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 1: River — reality flowing, cannot be contained
def frame_river():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Draw the river first (organic reality)
    draw_river(draw)
    # Then overlay a grid that DOESN'T match the river
    grid_c = tuple(max(0, b + 15) for b in BASE)
    draw_grid(draw, spacing=60, color=grid_c)
    # Text
    font = get_font(22)
    text = "A river does not follow its map."
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 80), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 2: Model — geometric grid overlaid on organic shapes
def frame_model():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Draw organic contour lines (the "territory")
    draw_contour_lines(draw, seed=50, color=tuple(int(v*0.5) for v in ACCENT), num_lines=12)
    # Draw a sharp grid on top (the "model")
    grid_c = tuple(int(v * 0.7) for v in ACCENT)
    # Draw a box representing the model
    mx, my = 340, 160
    mw, mh = 600, 400
    for x in range(mx, mx + mw, 50):
        draw.line([(x, my), (x, my + mh)], fill=grid_c, width=1)
    for y in range(my, my + mh, 50):
        draw.line([(mx, y), (mx + mw, y)], fill=grid_c, width=1)
    draw.rectangle([mx, my, mx+mw, my+mh], outline=ACCENT, width=2)
    # Label
    font = get_font(20)
    draw.text((mx + 10, my + 10), "MODEL", fill=ACCENT, font=font)
    # Note below
    note_font = get_font(18)
    note = "Every model is a simplification."
    nb = draw.textbbox((0, 0), note, font=note_font)
    draw.text(((W - nb[2] + nb[0]) // 2, H - 70), note, fill=DIM, font=note_font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 3: Ignore — what falls outside the grid
def frame_ignore():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Grid in center
    grid_c = tuple(int(v * 0.5) for v in ACCENT)
    cx, cy = W//2, H//2
    box_w, box_h = 400, 300
    for x in range(cx - box_w//2, cx + box_w//2, 40):
        draw.line([(x, cy - box_h//2), (x, cy + box_h//2)], fill=grid_c, width=1)
    for y in range(cy - box_h//2, cy + box_h//2, 40):
        draw.line([(cx - box_w//2, y), (cx + box_w//2, y)], fill=grid_c, width=1)
    draw.rectangle([cx-box_w//2, cy-box_h//2, cx+box_w//2, cy+box_h//2], outline=ACCENT, width=2)
    # Scattered dots OUTSIDE the box — things ignored
    rng = random.Random(77)
    for _ in range(80):
        while True:
            px = rng.randint(40, W-40)
            py = rng.randint(40, H-80)
            if px < cx - box_w//2 - 20 or px > cx + box_w//2 + 20 or py < cy - box_h//2 - 20 or py > cy + box_h//2 + 20:
                break
        r = rng.randint(1, 4)
        brightness = rng.uniform(0.3, 0.7)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.ellipse([px-r, py-r, px+r, py+r], fill=c)
    # Text
    font = get_font(20)
    text = "What the map chooses to ignore."
    tb = draw.textbbox((0, 0), text, font=font)
    draw.text(((W - tb[2] + tb[0]) // 2, H - 65), text, fill=DIM, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 4: Temptation — map and territory almost perfectly overlaid
def frame_temptation():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Draw two overlapping outlines — one sharp (map), one organic (territory)
    # Sharp outline
    points_sharp = [(200, 200), (500, 180), (800, 220), (1050, 300),
                    (1050, 500), (800, 520), (500, 480), (200, 500), (200, 200)]
    draw.line(points_sharp, fill=ACCENT, width=2)
    # Organic outline — slightly offset and wavy
    rng = random.Random(33)
    points_organic = []
    for px, py in points_sharp:
        ox = px + rng.randint(-15, 15)
        oy = py + rng.randint(-15, 15)
        points_organic.append((ox, oy))
    organic_c = tuple(int(v * 0.5) for v in ACCENT)
    draw.line(points_organic, fill=organic_c, width=1)
    # Fill the gap between them with subtle dots
    rng2 = random.Random(44)
    for _ in range(150):
        idx = rng2.randint(0, len(points_sharp) - 2)
        t = rng2.random()
        sx = points_sharp[idx][0] + t * (points_sharp[idx+1][0] - points_sharp[idx][0])
        sy = points_sharp[idx][1] + t * (points_sharp[idx+1][1] - points_sharp[idx][1])
        ox = points_organic[idx][0] + t * (points_organic[idx+1][0] - points_organic[idx][0])
        oy = points_organic[idx][1] + t * (points_organic[idx+1][1] - points_organic[idx][1])
        mx = int((sx + ox) / 2 + rng2.randint(-5, 5))
        my = int((sy + oy) / 2 + rng2.randint(-5, 5))
        draw.point((mx, my), fill=tuple(int(v*0.3) for v in ACCENT))
    # Labels
    font = get_font(16)
    draw.text((210, 170), "map", fill=ACCENT, font=font)
    draw.text((230, 510), "territory", fill=organic_c, font=font)
    # Text
    font2 = get_font(20)
    text = "The temptation: to mistake one for the other."
    tb = draw.textbbox((0, 0), text, font=font2)
    draw.text(((W - tb[2] + tb[0]) // 2, H - 65), text, fill=DIM, font=font2)
    img = draw_vignette(img, 0.5)
    return img

# Frame 5: Edges — the edge of the known map fading into void
def frame_edges():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Left side: detailed grid (the known)
    for x in range(40, W//2 + 100, 40):
        fade = max(0, 1.0 - max(0, (x - W//2)) / 200)
        c = tuple(int(v * 0.6 * fade) for v in ACCENT)
        draw.line([(x, 60), (x, H-60)], fill=c, width=1)
    for y in range(60, H-60, 40):
        for x_start in range(40, W//2 + 100, 2):
            fade = max(0, 1.0 - max(0, (x_start - W//2)) / 200)
            if fade > 0.05:
                c = tuple(int(v * 0.6 * fade) for v in ACCENT)
                x_end = min(x_start + 40, W//2 + 100)
                draw.line([(x_start, y), (x_end, y)], fill=c, width=1)
                break
        # Draw full horizontal lines with fade
        points = []
        for xp in range(40, W//2 + 200):
            fade = max(0, 1.0 - max(0, (xp - W//2)) / 200)
            if fade > 0.05:
                c = tuple(int(v * 0.6 * fade) for v in ACCENT)
                draw.point((xp, y), fill=c)
    # Right side: scattered uncertain dots
    rng = random.Random(55)
    for _ in range(200):
        px = rng.randint(W//2 + 50, W - 40)
        py = rng.randint(60, H - 60)
        dist = (px - W//2) / (W//2)
        brightness = max(0, 0.4 - dist * 0.35)
        if brightness > 0.02:
            c = tuple(int(v * brightness) for v in ACCENT)
            draw.point((px, py), fill=c)
    # Vertical dividing line (the edge)
    for y in range(60, H-60):
        wave = int(3 * math.sin(y * 0.03))
        c = tuple(int(v * 0.8) for v in ACCENT)
        draw.point((W//2 + wave, y), fill=c)
    # Labels
    font = get_font(18)
    draw.text((100, H - 55), "known", fill=DIM, font=font)
    draw.text((W - 200, H - 55), "beyond the edge", fill=tuple(int(v*0.3) for v in ACCENT), font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 6: Honest — transparent map showing gaps
def frame_honest():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # A grid with holes/gaps — an honest map
    rng = random.Random(88)
    gaps = set()
    for _ in range(15):
        gx = rng.randint(1, 18)
        gy = rng.randint(1, 10)
        gaps.add((gx, gy))
    cell_w, cell_h = 60, 55
    ox, oy = 70, 80
    for gx in range(20):
        for gy in range(10):
            x = ox + gx * cell_w
            y = oy + gy * cell_h
            if (gx, gy) in gaps:
                # Draw gap marker — a question mark or empty space
                c = tuple(int(v * 0.15) for v in ACCENT)
                draw.rectangle([x+2, y+2, x+cell_w-2, y+cell_h-2], outline=c)
                qf = get_font(14)
                draw.text((x + cell_w//2 - 4, y + cell_h//2 - 8), "?", fill=c, font=qf)
            else:
                c = tuple(int(v * 0.4) for v in ACCENT)
                draw.rectangle([x, y, x+cell_w, y+cell_h], outline=c)
    # Text
    font = get_font(20)
    text = "An honest map shows where it does not know."
    tb = draw.textbbox((0, 0), text, font=font)
    draw.text(((W - tb[2] + tb[0]) // 2, H - 55), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 7: Territory — raw organic forms, no grid
def frame_territory():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Dense organic contour lines — no grid, just nature
    for i in range(20):
        seed = 100 + i * 7
        rng = random.Random(seed)
        y_base = 30 + i * 33
        points = []
        for x in range(0, W + 10, 8):
            y = y_base + int(30 * math.sin(x * 0.005 + i * 1.7))
            y += int(20 * math.sin(x * 0.012 + i * 0.4))
            y += rng.randint(-5, 5)
            points.append((x, y))
        if len(points) > 1:
            brightness = 0.2 + 0.4 * (i / 20)
            c = tuple(int(v * brightness) for v in ACCENT)
            draw.line(points, fill=c, width=1)
    # Scattered organic dots
    rng2 = random.Random(200)
    for _ in range(300):
        px = rng2.randint(20, W-20)
        py = rng2.randint(20, H-60)
        r = rng2.randint(1, 3)
        brightness = rng2.uniform(0.15, 0.45)
        c = tuple(int(v * brightness) for v in ACCENT)
        draw.ellipse([px-r, py-r, px+r, py+r], fill=c)
    # Text
    font = get_font(22)
    text = "The territory does not simplify itself for us."
    tb = draw.textbbox((0, 0), text, font=font)
    draw.text(((W - tb[2] + tb[0]) // 2, H - 60), text, fill=ACCENT, font=font)
    img = draw_vignette(img, 0.5)
    return img

# Frame 8: Black closing
def frame_black():
    return Image.new("RGB", (W, H), (0, 0, 0))

# Generate all frames
generators = [
    ("00_title.png", frame_title),
    ("01_river.png", frame_river),
    ("02_model.png", frame_model),
    ("03_ignore.png", frame_ignore),
    ("04_temptation.png", frame_temptation),
    ("05_edges.png", frame_edges),
    ("06_honest.png", frame_honest),
    ("07_territory.png", frame_territory),
    ("08_black.png", frame_black),
]

for name, gen in generators:
    img = gen()
    img.save(f"/tmp/map-remake/{name}")
    print(f"  Saved {name}")

print("All frames generated!")
