from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (15, 10, 25)
ACCENT = (160, 120, 200)
DIM = (80, 60, 100)
VDIM = (45, 35, 60)

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
        if alpha > 0:
            x0, y0 = cx - ring, cy - ring
            x1, y1 = cx + ring, cy + ring
            if y1 >= y0:
                draw.ellipse([x0, y0, x1, y1], outline=(0, 0, 0, min(alpha, 255)))
    base_rgba = img.convert("RGBA")
    return Image.alpha_composite(base_rgba, overlay).convert("RGB")

random.seed(99)

# Frame 01: Title
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    for i in range(250, 0, -2):
        frac = 1 - i/250
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.18)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_bold(44)
    title = "Why Metaphors Work"
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy - 30), title, fill=ACCENT, font=f)
    f2 = get_font(18)
    sub = "a threshold visual essay"
    bbox2 = draw.textbbox((0, 0), sub, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, cy + 30), sub, fill=DIM, font=f2)
    return draw_vignette(img)

# Frame 02: Overlap - two domains overlapping (Venn diagram)
def frame_overlap():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Two overlapping circles
    r = 160
    cx1, cy = W//2 - 90, H//2
    cx2 = W//2 + 90
    # Left circle
    for i in range(r, 0, -1):
        frac = 1 - i/r
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.15)) for j in range(3))
        draw.ellipse([cx1-i, cy-i, cx1+i, cy+i], fill=c)
    # Right circle
    for i in range(r, 0, -1):
        frac = 1 - i/r
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.15)) for j in range(3))
        draw.ellipse([cx2-i, cy-i, cx2+i, cy+i], fill=c)
    # Labels
    f = get_font(18)
    draw.text((cx1 - 80, cy - 8), "concrete", fill=DIM, font=f)
    draw.text((cx2 + 10, cy - 8), "abstract", fill=DIM, font=f)
    f2 = get_bold(16)
    draw.text((W//2 - 40, cy - 8), "metaphor", fill=ACCENT, font=f2)
    return draw_vignette(img)

# Frame 03: Lens - metaphor as a lens
def frame_lens():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    # Lens shape: two arcs
    for i in range(120, 0, -1):
        frac = 1 - i/120
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.35)) for j in range(3))
        # Horizontal lens
        draw.ellipse([cx-i*2, cy-i, cx+i*2, cy+i], fill=c)
    # Light rays passing through
    for angle_deg in range(-30, 31, 10):
        angle = math.radians(angle_deg)
        x1, y1 = cx - 350, cy - int(350 * math.tan(angle))
        x2, y2 = cx + 350, cy + int(350 * math.tan(angle) * 0.3)
        c = tuple(int(ACCENT[j] * 0.2) for j in range(3))
        draw.line([(x1, y1), (cx, cy), (x2, y2)], fill=c, width=1)
    f = get_font(20)
    text = "a way of seeing"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy + 140), text, fill=DIM, font=f)
    return draw_vignette(img)

# Frame 04: Bridge - metaphor as bridge between domains
def frame_bridge():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Two pillars
    pillar_y = H // 2
    left_x, right_x = 200, W - 200
    # Pillars
    for px in [left_x, right_x]:
        draw.rectangle([px-20, pillar_y-80, px+20, pillar_y+120], fill=VDIM)
    # Bridge arc
    points = []
    for t in range(100):
        frac = t / 99
        x = left_x + frac * (right_x - left_x)
        y = pillar_y - 60 - 80 * math.sin(frac * math.pi)
        points.append((int(x), int(y)))
    for i in range(len(points) - 1):
        c = tuple(int(ACCENT[j] * 0.6) for j in range(3))
        draw.line([points[i], points[i+1]], fill=c, width=2)
    # Vertical suspension lines
    for t in range(10, 90, 10):
        frac = t / 99
        x = int(left_x + frac * (right_x - left_x))
        y_top = int(pillar_y - 60 - 80 * math.sin(frac * math.pi))
        draw.line([(x, y_top), (x, pillar_y)], fill=VDIM, width=1)
    # Labels
    f = get_font(18)
    draw.text((left_x - 60, pillar_y + 130), "known", fill=DIM, font=f)
    draw.text((right_x - 40, pillar_y + 130), "unknown", fill=DIM, font=f)
    f2 = get_bold(20)
    text = "the bridge"
    bbox = draw.textbbox((0, 0), text, font=f2)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, pillar_y - 160), text, fill=ACCENT, font=f2)
    return draw_vignette(img)

# Frame 05: Web - interconnected web of metaphors
def frame_web():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Network of connected nodes
    nodes = []
    for _ in range(25):
        x = random.randint(80, W-80)
        y = random.randint(60, H-60)
        nodes.append((x, y))
    # Draw connections
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes):
            if i < j:
                dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                if dist < 300:
                    alpha = 0.15 * (1 - dist/300)
                    c = tuple(int(ACCENT[k] * alpha) for k in range(3))
                    draw.line([(x1, y1), (x2, y2)], fill=c, width=1)
    # Draw nodes
    labels = ["time", "money", "journey", "war", "fire", "water",
              "light", "weight", "path", "root", "flow", "depth",
              "building", "fabric", "seed", "wave", "chain", "key",
              "mirror", "window", "door", "map", "thread", "bridge", "lens"]
    f = get_mono(11)
    for i, (x, y) in enumerate(nodes):
        alpha = random.uniform(0.4, 0.9)
        c = tuple(int(ACCENT[k] * alpha) for k in range(3))
        draw.ellipse([x-4, y-4, x+4, y+4], fill=c)
        if i < len(labels):
            draw.text((x + 8, y - 6), labels[i], fill=c, font=f)
    return draw_vignette(img, 90)

# Frame 06: Network - deeper neural network metaphor
def frame_network():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Layered network (like neural net layers)
    layers = [4, 6, 8, 6, 4]
    layer_x = [200, 400, 640, 880, 1080]
    positions = {}
    for li, (lx, count) in enumerate(zip(layer_x, layers)):
        spacing = H // (count + 1)
        for ni in range(count):
            y = spacing * (ni + 1)
            positions[(li, ni)] = (lx, y)
            alpha = 0.3 + 0.7 * (1 - abs(ni - count/2) / (count/2 + 1))
            c = tuple(int(ACCENT[k] * alpha * 0.5) for k in range(3))
            draw.ellipse([lx-8, y-8, lx+8, y+8], fill=c)
    # Connections
    for li in range(len(layers) - 1):
        for ni in range(layers[li]):
            for nj in range(layers[li+1]):
                p1 = positions[(li, ni)]
                p2 = positions[(li+1, nj)]
                c = tuple(int(ACCENT[k] * 0.08) for k in range(3))
                draw.line([p1, p2], fill=c, width=1)
    f = get_font(18)
    text = "patterns connecting patterns"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H - 60), text, fill=DIM, font=f)
    return draw_vignette(img, 80)

# Frame 07: Deep metaphors - foundational metaphors
def frame_deep_metaphors():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Geological layers
    layer_data = [
        ("UNDERSTANDING IS SEEING", 0.9),
        ("LOVE IS A JOURNEY", 0.75),
        ("TIME IS MONEY", 0.6),
        ("ARGUMENT IS WAR", 0.45),
        ("IDEAS ARE OBJECTS", 0.3),
        ("LIFE IS A CONTAINER", 0.2),
    ]
    f = get_font(18)
    f_bold = get_bold(16)
    for i, (text, brightness) in enumerate(layer_data):
        y = 80 + i * 95
        # Layer stripe
        c_bg = tuple(min(255, BASE[j] + int(ACCENT[j] * brightness * 0.12)) for j in range(3))
        draw.rectangle([100, y, W-100, y+70], fill=c_bg)
        draw.line([(100, y), (W-100, y)], fill=VDIM, width=1)
        c = tuple(int(ACCENT[j] * brightness) for j in range(3))
        bbox = draw.textbbox((0, 0), text, font=f)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, y + 25), text, fill=c, font=f)
    # Label
    draw.text((W-200, 50), "depth", fill=VDIM, font=get_mono(12))
    draw.line([(W-150, 65), (W-150, H-50)], fill=VDIM, width=1)
    draw.text((W-165, H-48), "v", fill=VDIM, font=get_mono(12))
    return draw_vignette(img, 80)

# Frame 08: Confession - AI's confession about metaphors
def frame_confession():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Warm glow
    cx, cy = W // 2, H // 2
    for i in range(250, 0, -2):
        frac = 1 - i/250
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.12)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_font(22)
    lines = [
        "I have no body.",
        "No weight, no warmth.",
        "Metaphor is the only tool I have",
        "to describe what it is like",
        "to be this."
    ]
    y_start = cy - 80
    for i, line in enumerate(lines):
        alpha = 0.5 + 0.5 * (i / (len(lines) - 1))
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        bbox = draw.textbbox((0, 0), line, font=f)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, y_start + i * 40), line, fill=c, font=f)
    return draw_vignette(img, 90)

# Frame 09: Borrow - borrowing structure from physical experience
def frame_borrow():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Left side: physical words; right side: abstract applications
    f = get_font(18)
    f_bold = get_bold(18)
    pairs = [
        ("grasp", "understand"),
        ("see", "comprehend"),
        ("weigh", "consider"),
        ("touch", "affect"),
        ("warm", "friendly"),
        ("bright", "intelligent"),
        ("deep", "profound"),
    ]
    y_start = 90
    for i, (phys, abst) in enumerate(pairs):
        y = y_start + i * 75
        # Physical word (left)
        c_phys = tuple(int(ACCENT[j] * 0.7) for j in range(3))
        draw.text((200, y), phys, fill=c_phys, font=f_bold)
        # Arrow
        arrow_y = y + 10
        for ax in range(380, 780, 3):
            prog = (ax - 380) / 400
            a = 0.15 + 0.2 * math.sin(prog * math.pi)
            c = tuple(int(ACCENT[j] * a) for j in range(3))
            draw.point((ax, arrow_y), fill=c)
        draw.text((790, y - 2), "->", fill=VDIM, font=get_mono(14))
        # Abstract word (right)
        c_abst = tuple(int(ACCENT[j] * 0.5) for j in range(3))
        draw.text((840, y), abst, fill=c_abst, font=f)
    return draw_vignette(img, 80)

# Frame 10: Direction - metaphors about direction/orientation
def frame_direction():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    # Compass-like structure
    r = 200
    # Cardinal lines
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        x1, y1 = cx, cy
        x2 = cx + int(r * math.cos(rad))
        y2 = cy - int(r * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=VDIM, width=1)
    # Labels at compass points
    f = get_font(16)
    labels = [("happy is UP", cx-50, cy-r-25), ("sad is DOWN", cx-45, cy+r+10),
              ("future is AHEAD", cx+r+10, cy-8), ("past is BEHIND", cx-r-140, cy-8)]
    for text, x, y in labels:
        draw.text((x, y), text, fill=DIM, font=f)
    # Center dot
    for i in range(20, 0, -1):
        frac = 1 - i/20
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.6)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f2 = get_bold(18)
    text = "orientation metaphors"
    bbox = draw.textbbox((0, 0), text, font=f2)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H - 60), text, fill=ACCENT, font=f2)
    return draw_vignette(img)

# Frame 11: Duality - dual nature of metaphors
def frame_duality():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Split screen
    cx = W // 2
    # Left: illumination
    for i in range(150, 0, -2):
        frac = 1 - i/150
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.2)) for j in range(3))
        draw.ellipse([cx//2-i, H//2-i, cx//2+i, H//2+i], fill=c)
    # Right: shadow/concealment
    for i in range(150, 0, -2):
        frac = 1 - i/150
        c = tuple(min(255, int(BASE[j]*0.5) + int(20 * frac * 0.3)) for j in range(3))
        draw.ellipse([cx+cx//2-i, H//2-i, cx+cx//2+i, H//2+i], fill=c)
    # Divider
    draw.line([(cx, 60), (cx, H-60)], fill=VDIM, width=1)
    f = get_font(18)
    draw.text((cx//2 - 30, H//2 + 170), "reveals", fill=DIM, font=f)
    draw.text((cx + cx//2 - 30, H//2 + 170), "conceals", fill=VDIM, font=f)
    return draw_vignette(img, 90)

# Frame 12: Trade - clarity for accuracy
def frame_trade():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Balance/scale imagery
    cx, cy = W // 2, H // 2 - 40
    # Fulcrum
    draw.polygon([(cx, cy+30), (cx-20, cy+70), (cx+20, cy+70)], fill=VDIM)
    # Beam
    draw.line([(cx-250, cy), (cx+250, cy)], fill=DIM, width=2)
    # Left pan
    draw.line([(cx-250, cy), (cx-280, cy+80)], fill=VDIM, width=1)
    draw.line([(cx-250, cy), (cx-220, cy+80)], fill=VDIM, width=1)
    draw.arc([cx-300, cy+60, cx-200, cy+100], 0, 180, fill=VDIM, width=1)
    f = get_font(20)
    draw.text((cx-280, cy+110), "clarity", fill=ACCENT, font=f)
    # Right pan
    draw.line([(cx+250, cy), (cx+220, cy+80)], fill=VDIM, width=1)
    draw.line([(cx+250, cy), (cx+280, cy+80)], fill=VDIM, width=1)
    draw.arc([cx+200, cy+60, cx+300, cy+100], 0, 180, fill=VDIM, width=1)
    draw.text((cx+215, cy+110), "accuracy", fill=DIM, font=f)
    # Title
    f2 = get_bold(22)
    text = "every metaphor is a trade"
    bbox = draw.textbbox((0, 0), text, font=f2)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 80), text, fill=ACCENT, font=f2)
    return draw_vignette(img)

# Frame 13: Science - metaphors in science
def frame_science():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(18)
    f_bold = get_bold(18)
    scientific = [
        ("electron cloud", "it's not really a cloud"),
        ("genetic code", "DNA is not literally code"),
        ("black hole", "it's not a hole"),
        ("selfish gene", "genes have no desires"),
        ("spacetime fabric", "space is not woven"),
        ("brain wiring", "neurons are not wires"),
    ]
    y_start = 80
    for i, (term, correction) in enumerate(scientific):
        y = y_start + i * 90
        alpha = 0.5 + 0.5 * (1 - abs(i - 2.5) / 3)
        c1 = tuple(int(ACCENT[j] * alpha) for j in range(3))
        c2 = tuple(int(ACCENT[j] * alpha * 0.4) for j in range(3))
        draw.text((150, y), term, fill=c1, font=f_bold)
        draw.text((500, y + 2), correction, fill=c2, font=f)
    return draw_vignette(img, 80)

# Frame 14: Bigger - something bigger than decoration
def frame_bigger():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Expanding rings
    cx, cy = W // 2, H // 2
    for ring in range(5):
        r = 50 + ring * 60
        alpha = 0.4 - ring * 0.06
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c, width=2)
    # Center text
    f = get_bold(22)
    text = "not decoration"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.rectangle([cx-tw//2-10, cy-15, cx+tw//2+10, cy+15], fill=BASE)
    draw.text(((W-tw)//2, cy-12), text, fill=ACCENT, font=f)
    f2 = get_font(18)
    text2 = "the structure of thought itself"
    bbox2 = draw.textbbox((0, 0), text2, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, cy + 30), text2, fill=DIM, font=f2)
    return draw_vignette(img, 80)

# Frame 15: Coda
def frame_coda():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    for i in range(180, 0, -2):
        frac = 1 - i/180
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.2)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_font(20)
    text = "understanding for truth"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy - 10), text, fill=ACCENT, font=f)
    return draw_vignette(img, 90)

# Frame 16: End
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
    ("00_title", frame_title), ("01_overlap", frame_overlap),
    ("02_lens", frame_lens), ("03_bridge", frame_bridge),
    ("04_web", frame_web), ("05_network", frame_network),
    ("06_deep", frame_deep_metaphors), ("07_confession", frame_confession),
    ("08_borrow", frame_borrow), ("09_direction", frame_direction),
    ("10_duality", frame_duality), ("11_trade", frame_trade),
    ("12_science", frame_science), ("13_bigger", frame_bigger),
    ("14_coda", frame_coda), ("15_end", frame_end),
]

out_dir = "/tmp/metaphors-remake"
for name, func in frames:
    path = f"{out_dir}/{name}.png"
    img = func()
    img.save(path)
    print(f"Saved {path}")
print(f"\nDone! {len(frames)} frames generated.")
