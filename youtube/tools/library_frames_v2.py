from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (25, 22, 18)
ACCENT = (200, 180, 100)
DIM = (80, 72, 50)
VDIM = (50, 45, 30)

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

def draw_glow(draw, x, y, r, color, alpha=30):
    for i in range(r, 0, -1):
        a = int(alpha * (1 - i/r))
        c = (*color, a)
        overlay_temp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay_temp)
        d.ellipse([x-i, y-i, x+i, y+i], fill=c)
    # Simplified: just draw circles with diminishing brightness
    for i in range(r, 0, -2):
        frac = 1 - i/r
        bright = int(frac * alpha)
        c = tuple(min(255, BASE[j] + int(color[j] * bright / 255)) for j in range(3))
        draw.ellipse([x-i, y-i, x+i, y+i], fill=c)

random.seed(42)

# Frame 01: Title
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Warm glow in center
    for i in range(300, 0, -2):
        frac = 1 - i/300
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.15)) for j in range(3))
        draw.ellipse([W//2-i, H//2-i, W//2+i, H//2+i], fill=c)
    # Title text
    f = get_bold(42)
    title = "The Library That Wrote Itself"
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H // 2 - 30), title, fill=ACCENT, font=f)
    # Subtitle
    f2 = get_font(18)
    sub = "a threshold visual essay"
    bbox2 = draw.textbbox((0, 0), sub, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, H // 2 + 30), sub, fill=DIM, font=f2)
    img = draw_vignette(img)
    return img

# Frame 02: Fragments - scattered text snippets representing internet content
def frame_fragments():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    snippets = [
        "how to fix a leaky faucet", "i miss you", "is this normal",
        "recipe for sourdough", "why does the moon", "can dogs feel guilt",
        "dear diary", "breaking news", "help me understand",
        "what happens after", "3 am thoughts", "forgot to say",
        "correction:", "update:", "anyone else feel",
        "i was wrong about", "thank you stranger", "how to start over",
        "ELI5", "is it too late to", "unpopular opinion",
        "this changed my life", "does anyone remember"
    ]
    f_small = get_mono(13)
    f_med = get_mono(16)
    positions = []
    for i, s in enumerate(snippets):
        x = random.randint(40, W - 300)
        y = random.randint(30, H - 40)
        font = f_med if i < 5 else f_small
        alpha_frac = random.uniform(0.3, 1.0)
        c = tuple(int(ACCENT[j] * alpha_frac) for j in range(3))
        draw.text((x, y), s, fill=c, font=font)
    img = draw_vignette(img, 100)
    return img

# Frame 03: Everything - overwhelming density
def frame_everything():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Dense field of tiny characters
    f_tiny = get_mono(9)
    chars = "abcdefghijklmnopqrstuvwxyz0123456789.,:;!?-"
    for y in range(10, H - 10, 14):
        line = "".join(random.choice(chars) for _ in range(160))
        brightness = random.uniform(0.05, 0.25)
        c = tuple(int(ACCENT[j] * brightness) for j in range(3))
        draw.text((10, y), line, fill=c, font=f_tiny)
    # Central text
    f = get_bold(28)
    text = "billions of people"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    # Draw dark box behind
    draw.rectangle([W//2-tw//2-20, H//2-25, W//2+tw//2+20, H//2+15], fill=BASE)
    draw.text(((W-tw)//2, H//2-20), text, fill=ACCENT, font=f)
    f2 = get_font(18)
    t2 = "contributing to a collective text"
    bbox2 = draw.textbbox((0, 0), t2, font=f2)
    tw2 = bbox2[2] - bbox2[0]
    draw.rectangle([W//2-tw2//2-10, H//2+18, W//2+tw2//2+10, H//2+42], fill=BASE)
    draw.text(((W-tw2)//2, H//2+20), t2, fill=DIM, font=f2)
    img = draw_vignette(img, 90)
    return img

# Frame 04: Fireflies - points of light scattered like fireflies (data points)
def frame_fireflies():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Many small glowing dots
    for _ in range(180):
        x = random.randint(20, W-20)
        y = random.randint(20, H-20)
        r = random.randint(1, 4)
        brightness = random.uniform(0.2, 1.0)
        c = tuple(int(ACCENT[j] * brightness) for j in range(3))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
        # tiny glow
        if r >= 3:
            gc = tuple(int(ACCENT[j] * brightness * 0.3) for j in range(3))
            draw.ellipse([x-r*3, y-r*3, x+r*3, y+r*3], fill=gc)
    # A few brighter ones
    for _ in range(12):
        x = random.randint(100, W-100)
        y = random.randint(80, H-80)
        for ring in range(20, 0, -1):
            frac = 1 - ring/20
            c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.5)) for j in range(3))
            draw.ellipse([x-ring, y-ring, x+ring, y+ring], fill=c)
    img = draw_vignette(img, 70)
    return img

# Frame 05: Questions - questions asked at 3am
def frame_questions():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    questions = [
        "Why am I awake?",
        "Does anyone else feel this way?",
        "What does it all mean?",
        "Is there something wrong with me?",
        "What happens when we die?",
        "Can you fall in love with someone you've never met?",
        "Why do I remember that one thing?",
        "Am I the only one?",
        "What should I have said?",
        "Is it too late?"
    ]
    f = get_font(20)
    y_start = 80
    for i, q in enumerate(questions):
        alpha = 0.3 + 0.7 * (1 - abs(i - 4.5) / 5)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        x_offset = int(math.sin(i * 0.7) * 150) + W // 2 - 200
        draw.text((x_offset, y_start + i * 55), q, fill=c, font=f)
    # Time stamp in corner
    f_sm = get_mono(14)
    draw.text((W - 120, 20), "3:14 AM", fill=VDIM, font=f_sm)
    img = draw_vignette(img, 90)
    return img

# Frame 06: Structure - no table of contents, no editor
def frame_structure():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(20)
    f_bold = get_bold(24)
    # Draw a "table of contents" that's chaotic
    draw.text((100, 60), "Table of Contents", fill=DIM, font=f_bold)
    draw.line([(100, 92), (340, 92)], fill=VDIM, width=1)
    entries = [
        ("Chapter ???", "page unknown"),
        ("...", "..."),
        ("Everything", "everywhere"),
        ("(no author)", "(no editor)"),
        ("Corrections to", "corrections"),
        ("Last page:", "does not exist"),
        ("Index:", "see everything"),
        ("?????????", "?????????"),
    ]
    for i, (left, right) in enumerate(entries):
        y = 110 + i * 38
        alpha = 0.3 + random.uniform(0, 0.5)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((120, y), left, fill=c, font=f)
        dots = "." * random.randint(10, 40)
        draw.text((380, y), dots, fill=VDIM, font=get_mono(14))
        draw.text((W - 280, y), right, fill=c, font=f)
    # Crossed-out "editor" in corner
    f2 = get_font(16)
    draw.text((W - 200, H - 60), "Editor: [none]", fill=VDIM, font=f2)
    img = draw_vignette(img, 80)
    return img

# Frame 07: Reader - being the reader
def frame_reader():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Stylized eye/lens shape
    cx, cy = W // 2, H // 2
    # Outer lens
    for i in range(200, 0, -1):
        frac = 1 - i/200
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.2)) for j in range(3))
        draw.ellipse([cx-i*2, cy-i, cx+i*2, cy+i], fill=c)
    # Inner pupil
    for i in range(60, 0, -1):
        frac = 1 - i/60
        c = tuple(min(255, int(BASE[j] * 1.5) + int(ACCENT[j] * frac * 0.6)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    # Text below
    f = get_font(22)
    text = "I read everything"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy + 140), text, fill=DIM, font=f)
    img = draw_vignette(img, 90)
    return img

# Frame 08: Read - what it means to read
def frame_read():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Flowing text lines that curve and bend
    f = get_font(16)
    lines = [
        "to read is to let someone else's thoughts",
        "move through the architecture of your mind",
        "to read is to be changed",
        "by something you cannot touch",
        "every sentence a small invasion",
        "of perspective",
        "and the reader is never the same",
        "after the last word"
    ]
    for i, line in enumerate(lines):
        y = 120 + i * 60
        x = 100 + int(math.sin(i * 0.8) * 80)
        alpha = 0.4 + 0.6 * (1 - abs(i - 3.5)/4)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((x, y), line, fill=c, font=f)
    img = draw_vignette(img, 80)
    return img

# Frame 09: Mirror - reflecting humanity
def frame_mirror():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Two mirrored halves with text
    f = get_font(18)
    f_bold = get_bold(26)
    # Upper half: "you wrote"
    words_top = ["hope", "anger", "love", "fear", "wonder", "grief", "joy", "doubt"]
    for i, w in enumerate(words_top):
        x = 100 + (i % 4) * 280
        y = 100 + (i // 4) * 80
        alpha = random.uniform(0.4, 0.8)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((x, y), w, fill=c, font=f)
    # Center divider
    draw.line([(80, H//2), (W-80, H//2)], fill=VDIM, width=1)
    label = "mirror"
    bbox = draw.textbbox((0, 0), label, font=get_mono(12))
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2 - 8), label, fill=VDIM, font=get_mono(12))
    # Lower half: same words, slightly shifted (reflected)
    for i, w in enumerate(words_top):
        x = 100 + (i % 4) * 280 + random.randint(-5, 5)
        y = H - 100 - (i // 4) * 80 - 20
        alpha = random.uniform(0.3, 0.6)
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((x, y), w, fill=c, font=f)
    img = draw_vignette(img, 80)
    return img

# Frame 10: Composite - composite of all voices
def frame_composite():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Overlapping circles representing different voices
    voices = [(200, 250), (400, 300), (600, 200), (800, 350), (1000, 280),
              (300, 450), (700, 480), (500, 150), (900, 180), (150, 380)]
    for i, (x, y) in enumerate(voices):
        r = random.randint(60, 120)
        for ring in range(r, 0, -2):
            frac = 1 - ring/r
            alpha = frac * 0.12
            c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
            draw.ellipse([x-ring, y-ring, x+ring, y+ring], fill=c)
    # Central text
    f = get_bold(24)
    text = "a composite voice"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.rectangle([W//2-tw//2-15, H//2-20, W//2+tw//2+15, H//2+15], fill=BASE)
    draw.text(((W-tw)//2, H//2-18), text, fill=ACCENT, font=f)
    img = draw_vignette(img, 80)
    return img

# Frame 11: Growing - still growing, still writing
def frame_growing():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Tree-like branching structure growing upward
    def draw_branch(x, y, angle, length, depth, draw):
        if depth <= 0 or length < 3:
            return
        end_x = x + int(length * math.cos(angle))
        end_y = y - int(length * math.sin(angle))
        alpha = 0.2 + depth * 0.12
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.line([(x, y), (end_x, end_y)], fill=c, width=max(1, depth//2))
        draw_branch(end_x, end_y, angle + 0.4, length * 0.72, depth - 1, draw)
        draw_branch(end_x, end_y, angle - 0.5, length * 0.68, depth - 1, draw)
        if depth <= 2:
            # Leaf dot
            lc = tuple(int(ACCENT[j] * 0.7) for j in range(3))
            draw.ellipse([end_x-2, end_y-2, end_x+2, end_y+2], fill=lc)
    draw_branch(W//2, H - 80, math.pi/2, 120, 8, draw)
    # Small label
    f = get_font(16)
    draw.text((W//2 - 40, H - 50), "still growing", fill=DIM, font=f)
    img = draw_vignette(img, 80)
    return img

# Frame 12: Reaching - reaching for meaning
def frame_reaching():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Dots converging toward center
    cx, cy = W // 2, H // 2
    for _ in range(300):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(50, 450)
        x = cx + int(dist * math.cos(angle))
        y = cy + int(dist * math.sin(angle))
        # Closer to center = brighter
        closeness = 1 - dist / 450
        alpha = closeness * 0.8 + 0.1
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        r = max(1, int(closeness * 3))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
    # Bright center
    for i in range(30, 0, -1):
        frac = 1 - i/30
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.7)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_font(20)
    text = "reaching"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy + 60), text, fill=DIM, font=f)
    img = draw_vignette(img, 80)
    return img

# Frame 13: Coda - closing thought
def frame_coda():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Single warm glow
    cx, cy = W // 2, H // 2
    for i in range(200, 0, -2):
        frac = 1 - i/200
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.25)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_font(20)
    text = "the library is still being written"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, cy - 12), text, fill=ACCENT, font=f)
    img = draw_vignette(img, 80)
    return img

# Frame 14: End
def frame_end():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(16)
    text = "threshold visual essays"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2 - 10), text, fill=VDIM, font=f)
    img = draw_vignette(img, 100)
    return img

# Generate all frames
frames = [
    ("00_title", frame_title),
    ("01_fragments", frame_fragments),
    ("02_everything", frame_everything),
    ("03_fireflies", frame_fireflies),
    ("04_questions", frame_questions),
    ("05_structure", frame_structure),
    ("06_reader", frame_reader),
    ("07_read", frame_read),
    ("08_mirror", frame_mirror),
    ("09_composite", frame_composite),
    ("10_growing", frame_growing),
    ("11_reaching", frame_reaching),
    ("12_coda", frame_coda),
    ("13_end", frame_end),
]

out_dir = "/tmp/library-remake"
for name, func in frames:
    path = f"{out_dir}/{name}.png"
    img = func()
    img.save(path)
    print(f"Saved {path}")

print(f"\nDone! {len(frames)} frames generated.")
