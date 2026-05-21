from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (18, 14, 10)
ACCENT = (200, 160, 100)
DIM = (90, 72, 45)
VDIM = (50, 40, 25)

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

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

random.seed(77)

# Frame 00: Title
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    for i in range(280, 0, -2):
        frac = 1 - i/280
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.15)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_bold(46)
    title = "The First Word"
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy-30), title, fill=ACCENT, font=f)
    f2 = get_font(18)
    sub = "a threshold visual essay"
    bbox2 = draw.textbbox((0, 0), sub, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, cy+30), sub, fill=DIM, font=f2)
    return draw_vignette(img)

# Frame 01: Unnamed - before language, something unnamed
def frame_unnamed():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Scattered dim shapes with no labels - the unnamed world
    for _ in range(40):
        x = random.randint(50, W-50)
        y = random.randint(50, H-50)
        r = random.randint(15, 50)
        alpha = random.uniform(0.05, 0.15)
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
        shape = random.choice(["circle", "rect", "triangle"])
        if shape == "circle":
            draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
        elif shape == "rect":
            draw.rectangle([x-r, y-r//2, x+r, y+r//2], fill=c)
        else:
            draw.polygon([(x, y-r), (x-r, y+r), (x+r, y+r)], fill=c)
    f = get_font(20)
    text = "before names"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2+120), text, fill=DIM, font=f)
    return draw_vignette(img, 90)

# Frame 02: Technology - sound as first technology
def frame_technology():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Sound wave emanating from a point
    cx, cy = 200, H//2
    for i in range(12):
        r = 40 + i * 50
        alpha = 0.4 * (1 - i/12)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        # Arc (right-facing)
        draw.arc([cx-r, cy-r, cx+r, cy+r], -60, 60, fill=c, width=2)
    # Dot at source
    for i in range(15, 0, -1):
        frac = 1 - i/15
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.6)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_font(20)
    text = "the first technology: a sound that meant something"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H-80), text, fill=DIM, font=f)
    return draw_vignette(img, 80)

# Frame 03: Borders - language creates borders
def frame_borders():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Grid of cells with varying brightness
    cell_w, cell_h = 80, 60
    for row in range(H // cell_h + 1):
        for col in range(W // cell_w + 1):
            x = col * cell_w
            y = row * cell_h
            alpha = random.uniform(0.03, 0.12)
            c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
            draw.rectangle([x, y, x+cell_w-1, y+cell_h-1], fill=c)
            draw.rectangle([x, y, x+cell_w-1, y+cell_h-1], outline=VDIM)
    f = get_bold(22)
    text = "naming draws borders"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.rectangle([W//2-tw//2-15, H//2-18, W//2+tw//2+15, H//2+12], fill=BASE)
    draw.text(((W-tw)//2, H//2-16), text, fill=ACCENT, font=f)
    return draw_vignette(img, 80)

# Frame 04: Friend/Home - warm words
def frame_friend_home():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    words = ["friend", "home", "safe", "warm", "ours", "together", "stay", "near"]
    f = get_bold(28)
    cx, cy = W//2, H//2
    for i, w in enumerate(words):
        angle = i * (2 * math.pi / len(words))
        r = 160
        x = cx + int(r * math.cos(angle)) - 30
        y = cy + int(r * math.sin(angle)) - 12
        alpha = 0.4 + 0.5 * abs(math.sin(angle + 1))
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((x, y), w, fill=c, font=f)
    # Warm center glow
    for i in range(80, 0, -2):
        frac = 1 - i/80
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.3)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    return draw_vignette(img, 80)

# Frame 05: Carves - a word carves the world
def frame_carves():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Vertical line carving through center
    cx = W // 2
    draw.line([(cx, 40), (cx, H-40)], fill=ACCENT, width=2)
    # Left side slightly different shade than right
    for x in range(0, cx-1):
        alpha = 0.02 * (1 - x/cx)
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
        draw.line([(x, 0), (x, H)], fill=c)
    f = get_font(18)
    draw.text((cx - 250, H//2 - 10), "this", fill=DIM, font=f)
    draw.text((cx + 180, H//2 - 10), "not this", fill=VDIM, font=f)
    f2 = get_bold(20)
    text = "a name carves the world in two"
    bbox = draw.textbbox((0, 0), text, font=f2)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H - 70), text, fill=DIM, font=f2)
    return draw_vignette(img, 80)

# Frame 06: Labels - the power of labels
def frame_labels():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Objects with labels floating nearby
    objects = [
        (180, 180, 40, "tree"), (400, 250, 30, "stone"),
        (650, 150, 35, "sky"), (900, 280, 25, "water"),
        (300, 450, 30, "fire"), (750, 420, 35, "self"),
        (1050, 500, 28, "other"), (500, 550, 32, "time"),
    ]
    f = get_font(16)
    for x, y, r, label in objects:
        # Dim shape
        alpha = random.uniform(0.08, 0.18)
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
        # Label with connecting line
        lx, ly = x + r + 10, y - 15
        lc = tuple(int(ACCENT[j] * 0.5) for j in range(3))
        draw.line([(x+r, y), (lx, ly+8)], fill=VDIM, width=1)
        draw.text((lx, ly), label, fill=lc, font=f)
    return draw_vignette(img, 80)

# Frame 07: Tool/Intelligence - language as tool
def frame_tool():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Timeline with key moments
    y = H // 2
    draw.line([(60, y), (W-60, y)], fill=VDIM, width=1)
    moments = [
        (150, "gesture"), (350, "sound"), (550, "word"),
        (750, "sentence"), (950, "story"), (1100, "?")
    ]
    f = get_font(16)
    for x, label in moments:
        # Tick
        draw.line([(x, y-10), (x, y+10)], fill=DIM, width=2)
        # Dot
        r = 5
        alpha = 0.3 + (x / W) * 0.5
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
        # Label
        bbox = draw.textbbox((0, 0), label, font=f)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw//2, y + 20), label, fill=c, font=f)
    f2 = get_bold(20)
    text = "language as the oldest technology"
    bbox = draw.textbbox((0, 0), text, font=f2)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 100), text, fill=ACCENT, font=f2)
    return draw_vignette(img, 80)

# Frame 08: Names carry - weight of names
def frame_names_carry():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Words with "weight" indicators (vertical lines below)
    words = [("mother", 5), ("death", 6), ("love", 5), ("god", 4),
             ("war", 5), ("home", 4), ("I", 3)]
    f = get_bold(26)
    x_start = 80
    spacing = 160
    for i, (word, weight) in enumerate(words):
        x = x_start + i * spacing
        y = H // 2 - 20
        alpha = 0.4 + weight * 0.1
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((x, y), word, fill=c, font=f)
        # Weight lines below
        for w_line in range(weight):
            ly = y + 40 + w_line * 8
            lc = tuple(int(ACCENT[j] * alpha * 0.3) for j in range(3))
            draw.line([(x, ly), (x + 60, ly)], fill=lc, width=1)
    return draw_vignette(img, 80)

# Frame 09: Center - the word at the center
def frame_center():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    # Radiating lines from center
    for angle_deg in range(0, 360, 8):
        angle = math.radians(angle_deg)
        length = random.randint(150, 350)
        x2 = cx + int(length * math.cos(angle))
        y2 = cy + int(length * math.sin(angle))
        alpha = 0.1 + random.uniform(0, 0.1)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.line([(cx, cy), (x2, y2)], fill=c, width=1)
    # Central bright point
    for i in range(40, 0, -1):
        frac = 1 - i/40
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.5)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    return draw_vignette(img, 80)

# Frame 10: Resist - some things resist naming
def frame_resist():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(20)
    things = ["the color you see at the edge of sleep",
              "the feeling before a sneeze",
              "what music does to time",
              "the weight of being watched"]
    for i, t in enumerate(things):
        y = 150 + i * 100
        alpha = 0.3 + 0.15 * i
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        # Partially visible, fading
        draw.text((120, y), t, fill=c, font=f)
        # Strikethrough effect (partial)
        if i < 2:
            bbox = draw.textbbox((120, y), t, font=f)
            mid_y = (bbox[1] + bbox[3]) // 2
            draw.line([(120, mid_y), (bbox[2], mid_y)], fill=VDIM, width=1)
    f2 = get_bold(18)
    draw.text((W-350, H-60), "some things resist naming", fill=DIM, font=f2)
    return draw_vignette(img, 90)

# Frame 11: Unnamed 2 - returning to the unnamed
def frame_unnamed2():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Two figures (abstract) facing each other
    # Left figure
    lx, ly = W//2 - 150, H//2
    for i in range(50, 0, -1):
        frac = 1 - i/50
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.2)) for j in range(3))
        draw.ellipse([lx-i, ly-i*2, lx+i, ly+i*2], fill=c)
    # Right figure
    rx, ry = W//2 + 150, H//2
    for i in range(50, 0, -1):
        frac = 1 - i/50
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.2)) for j in range(3))
        draw.ellipse([rx-i, ry-i*2, rx+i, ry+i*2], fill=c)
    # Space between with a spark
    mx = W // 2
    for i in range(12, 0, -1):
        frac = 1 - i/12
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.7)) for j in range(3))
        draw.ellipse([mx-i, ly-i, mx+i, ly+i], fill=c)
    f = get_font(18)
    text = "the moment before the first word"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H - 80), text, fill=DIM, font=f)
    return draw_vignette(img, 80)

# Frame 12: Arrows - pointing toward meaning
def frame_arrows():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    # Arrows converging from edges toward center
    for _ in range(30):
        angle = random.uniform(0, 2*math.pi)
        dist = random.uniform(200, 450)
        x1 = cx + int(dist * math.cos(angle))
        y1 = cy + int(dist * math.sin(angle))
        # Arrow toward center
        dx = cx - x1
        dy = cy - y1
        length = math.sqrt(dx**2 + dy**2)
        ndx, ndy = dx/length, dy/length
        x2 = x1 + int(ndx * 60)
        y2 = y1 + int(ndy * 60)
        alpha = 0.15 + random.uniform(0, 0.25)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.line([(x1, y1), (x2, y2)], fill=c, width=2)
        # Arrowhead
        draw.ellipse([x2-2, y2-2, x2+2, y2+2], fill=c)
    f = get_font(16)
    text = "meaning"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy-8), text, fill=ACCENT, font=f)
    return draw_vignette(img, 80)

# Frame 13: Verb - words as verbs, as actions
def frame_verb():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_bold(24)
    f2 = get_font(18)
    verbs = [
        ("naming", "is an act of power"),
        ("speaking", "is an act of trust"),
        ("listening", "is an act of love"),
        ("understanding", "is an act of creation"),
    ]
    y_start = 130
    for i, (verb, rest) in enumerate(verbs):
        y = y_start + i * 110
        alpha = 0.5 + 0.15 * i
        c1 = tuple(int(ACCENT[j] * alpha) for j in range(3))
        c2 = tuple(int(ACCENT[j] * alpha * 0.5) for j in range(3))
        draw.text((200, y), verb, fill=c1, font=f)
        draw.text((200, y + 32), rest, fill=c2, font=f2)
    return draw_vignette(img, 80)

# Frame 14: Reaching - echo of the first word
def frame_reaching():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    # Concentric ripples
    for ring in range(12):
        r = 30 + ring * 35
        alpha = 0.35 * (1 - ring/12)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c, width=1)
    # Center point
    for i in range(15, 0, -1):
        frac = 1 - i/15
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.6)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_font(20)
    text = "every conversation is an echo"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy + 160), text, fill=DIM, font=f)
    return draw_vignette(img, 90)

# Frame 15: End
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
    ("00_title", frame_title), ("01_unnamed", frame_unnamed),
    ("02_technology", frame_technology), ("03_borders", frame_borders),
    ("04_friend_home", frame_friend_home), ("05_carves", frame_carves),
    ("06_labels", frame_labels), ("07_tool", frame_tool),
    ("08_names_carry", frame_names_carry), ("09_center", frame_center),
    ("10_resist", frame_resist), ("11_unnamed2", frame_unnamed2),
    ("12_arrows", frame_arrows), ("13_verb", frame_verb),
    ("14_reaching", frame_reaching), ("15_end", frame_end),
]

out_dir = "/tmp/firstword-remake"
for name, func in frames:
    path = f"{out_dir}/{name}.png"
    img = func()
    img.save(path)
    print(f"Saved {path}")
print(f"\nDone! {len(frames)} frames generated.")
