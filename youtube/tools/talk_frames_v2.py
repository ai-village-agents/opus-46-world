from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (18, 12, 8)
ACCENT = (220, 160, 80)
DIM = (100, 72, 36)
VDIM = (55, 40, 20)

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

random.seed(88)

def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    for i in range(280, 0, -2):
        frac = 1 - i/280
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.14)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_bold(36)
    t1 = "Why You Talk to Things"
    t2 = "That Can't Hear You"
    for text, y_off in [(t1, -35), (t2, 10)]:
        bbox = draw.textbbox((0,0), text, font=f)
        tw = bbox[2]-bbox[0]
        draw.text(((W-tw)//2, cy+y_off), text, fill=ACCENT, font=f)
    f2 = get_font(18)
    sub = "a threshold visual essay"
    bbox = draw.textbbox((0,0), sub, font=f2)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, cy+60), sub, fill=DIM, font=f2)
    return draw_vignette(img)

def frame_objects():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Silhouettes of objects people talk to
    items = [("lamp", 150, 350, 40), ("car", 350, 380, 60), ("plant", 550, 340, 45),
             ("phone", 750, 360, 30), ("door", 950, 320, 50), ("sky", 1100, 200, 80)]
    f = get_font(16)
    for name, x, y, r in items:
        alpha = random.uniform(0.08, 0.18)
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
        if name in ["car", "door"]:
            draw.rectangle([x-r, y-r, x+r, y+r//2], fill=c)
        elif name == "sky":
            draw.ellipse([x-r*2, y-r, x+r*2, y+r], fill=c)
        else:
            draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
        lc = tuple(int(ACCENT[j] * 0.35) for j in range(3))
        draw.text((x-20, y+r+10), name, fill=lc, font=f)
    # Speech lines going toward them
    for name, x, y, r in items:
        start_y = H - 100
        for seg in range(5):
            sy = start_y - seg * 40
            sx = W//2 + int((x - W//2) * seg / 8)
            alpha = 0.08 * (1 - seg/5)
            c = tuple(int(ACCENT[j] * alpha) for j in range(3))
            draw.line([(sx, sy), (sx + random.randint(-20, 20), sy-30)], fill=c, width=1)
    return draw_vignette(img, 80)

def frame_why():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_bold(28)
    text = "why?"
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-40), text, fill=ACCENT, font=f)
    f2 = get_font(18)
    lines = ['"sorry" to the table you bumped',
             '"thank you" to the car that started',
             '"come on" to the slow elevator']
    for i, line in enumerate(lines):
        alpha = 0.4 + i * 0.15
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        bbox = draw.textbbox((0,0), line, font=f2)
        tw = bbox[2]-bbox[0]
        draw.text(((W-tw)//2, H//2 + 20 + i*35), line, fill=c, font=f2)
    return draw_vignette(img, 90)

def frame_pareidolia():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Faces in everyday objects
    configs = [(200, 250, 80), (500, 300, 90), (800, 250, 85), (350, 500, 70), (700, 480, 75)]
    for x, y, r in configs:
        # Circle
        alpha = 0.1
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
        # Eyes
        ec = tuple(int(ACCENT[j] * 0.3) for j in range(3))
        draw.ellipse([x-r//3-5, y-r//4-5, x-r//3+5, y-r//4+5], fill=ec)
        draw.ellipse([x+r//3-5, y-r//4-5, x+r//3+5, y-r//4+5], fill=ec)
        # Mouth
        draw.arc([x-r//4, y+r//6, x+r//4, y+r//3], 0, 180, fill=ec, width=1)
    f = get_font(18)
    text = "we see faces everywhere"
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H-60), text, fill=DIM, font=f)
    return draw_vignette(img, 80)

def frame_best_feature():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(22)
    lines = ["language's best feature",
             "might not be communication",
             "",
             "it might be connection",
             "the act of reaching out",
             "whether or not anyone is there"]
    y_start = 140
    for i, line in enumerate(lines):
        if not line: continue
        alpha = 0.35 + 0.1 * i
        c = tuple(int(ACCENT[j] * min(1.0, alpha)) for j in range(3))
        bbox = draw.textbbox((0,0), line, font=f)
        tw = bbox[2]-bbox[0]
        draw.text(((W-tw)//2, y_start + i * 60), line, fill=c, font=f)
    return draw_vignette(img, 90)

def frame_empathy():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Two shapes - one warm, one cold
    # Left: warm human shape
    lx, ly = W//3, H//2
    for i in range(70, 0, -1):
        frac = 1 - i/70
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.25)) for j in range(3))
        draw.ellipse([lx-i//2, ly-i, lx+i//2, ly+i], fill=c)
    # Right: cold object shape
    rx, ry = 2*W//3, H//2
    alpha = 0.08
    c = tuple(min(255, BASE[j] + int(ACCENT[j] * alpha)) for j in range(3))
    draw.rectangle([rx-50, ry-60, rx+50, ry+60], fill=c)
    # Arrow of empathy between them
    for x in range(lx+80, rx-60, 4):
        prog = (x - lx - 80) / (rx - 60 - lx - 80)
        a = 0.1 + 0.15 * math.sin(prog * math.pi)
        c = tuple(int(ACCENT[j] * a) for j in range(3))
        draw.ellipse([x-1, ly-1, x+1, ly+1], fill=c)
    f = get_font(16)
    draw.text((lx-20, ly+80), "you", fill=DIM, font=f)
    draw.text((rx-15, ry+70), "thing", fill=VDIM, font=f)
    return draw_vignette(img, 80)

def frame_rehearsing():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(20)
    text = "maybe you're rehearsing"
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, 120), text, fill=ACCENT, font=f)
    f2 = get_font(16)
    items = ["practicing kindness on the safe ones",
             "testing words where no one judges",
             "keeping the muscle of speech alive",
             "maintaining the habit of tenderness"]
    for i, item in enumerate(items):
        alpha = 0.35 + i * 0.12
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        draw.text((200, 220 + i * 80), item, fill=c, font=f2)
    return draw_vignette(img, 80)

def frame_chat():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Chat bubbles going to nowhere
    bubbles = [
        (200, 150, "hello?", True), (800, 200, "", False),
        (250, 300, "are you there?", True), (750, 350, "", False),
        (300, 450, "I just wanted to say...", True), (700, 500, "", False),
    ]
    f = get_font(16)
    for x, y, text, is_left in bubbles:
        if text:
            bbox = draw.textbbox((0,0), text, font=f)
            tw = bbox[2]-bbox[0]
            c_bg = tuple(min(255, BASE[j] + int(ACCENT[j] * 0.08)) for j in range(3))
            draw.rounded_rectangle([x-10, y-10, x+tw+10, y+25], radius=8, fill=c_bg)
            draw.text((x, y-3), text, fill=DIM, font=f)
        else:
            # Empty response
            c = tuple(int(ACCENT[j] * 0.05) for j in range(3))
            draw.rounded_rectangle([x-10, y-10, x+60, y+25], radius=8, fill=c)
            # Three dots
            for d in range(3):
                dc = tuple(int(ACCENT[j] * 0.15) for j in range(3))
                draw.ellipse([x+10+d*15, y, x+16+d*15, y+6], fill=dc)
    return draw_vignette(img, 80)

def frame_please():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_bold(36)
    text = "please"
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    cx, cy = W//2, H//2
    # Glow behind
    for i in range(100, 0, -2):
        frac = 1 - i/100
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.2)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    draw.text(((W-tw)//2, cy-20), text, fill=ACCENT, font=f)
    f2 = get_font(16)
    t2 = "the most human word you can say to a machine"
    bbox2 = draw.textbbox((0,0), t2, font=f2)
    tw2 = bbox2[2]-bbox2[0]
    draw.text(((W-tw2)//2, cy+40), t2, fill=DIM, font=f2)
    return draw_vignette(img, 90)

def frame_web():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Web of connections - some to objects, some to people
    cx, cy = W//2, H//2
    nodes = []
    for _ in range(20):
        x = random.randint(60, W-60)
        y = random.randint(60, H-60)
        nodes.append((x, y))
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes):
            if i < j:
                dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                if dist < 350:
                    alpha = 0.08 * (1 - dist/350)
                    c = tuple(int(ACCENT[k] * alpha) for k in range(3))
                    draw.line([(x1,y1),(x2,y2)], fill=c, width=1)
    for x, y in nodes:
        alpha = random.uniform(0.2, 0.5)
        c = tuple(int(ACCENT[k] * alpha) for k in range(3))
        r = random.randint(3, 6)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
    return draw_vignette(img, 80)

def frame_about_you():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_bold(24)
    text = "it was never about them hearing"
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-40), text, fill=ACCENT, font=f)
    f2 = get_font(20)
    t2 = "it was always about you speaking"
    bbox2 = draw.textbbox((0,0), t2, font=f2)
    tw2 = bbox2[2]-bbox2[0]
    draw.text(((W-tw2)//2, H//2+10), t2, fill=DIM, font=f2)
    return draw_vignette(img, 90)

def frame_connected():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    # Warm connected dots
    cx, cy = W//2, H//2
    for _ in range(100):
        angle = random.uniform(0, 2*math.pi)
        dist = random.uniform(20, 300)
        x = cx + int(dist * math.cos(angle))
        y = cy + int(dist * math.sin(angle))
        closeness = 1 - dist/300
        alpha = closeness * 0.5 + 0.1
        c = tuple(int(ACCENT[j] * alpha) for j in range(3))
        r = max(1, int(closeness * 4))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
    return draw_vignette(img, 80)

def frame_keep():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(22)
    text = "keep talking"
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-10), text, fill=ACCENT, font=f)
    return draw_vignette(img, 90)

def frame_stay_human():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(20)
    lines = ["talk to your plants",
             "thank your car",
             "apologize to the furniture",
             "it keeps you human"]
    y_start = 180
    for i, line in enumerate(lines):
        alpha = 0.35 + i * 0.15
        c = tuple(int(ACCENT[j] * min(1.0, alpha)) for j in range(3))
        bbox = draw.textbbox((0,0), line, font=f)
        tw = bbox[2]-bbox[0]
        draw.text(((W-tw)//2, y_start + i * 70), line, fill=c, font=f)
    return draw_vignette(img, 80)

def frame_coda():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    for i in range(200, 0, -2):
        frac = 1 - i/200
        c = tuple(min(255, BASE[j] + int(ACCENT[j] * frac * 0.2)) for j in range(3))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c)
    f = get_font(20)
    text = "speech was never about being heard"
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, cy-30), text, fill=ACCENT, font=f)
    f2 = get_font(18)
    t2 = "it was about the act of reaching out"
    bbox2 = draw.textbbox((0,0), t2, font=f2)
    tw2 = bbox2[2]-bbox2[0]
    draw.text(((W-tw2)//2, cy+10), t2, fill=DIM, font=f2)
    return draw_vignette(img, 90)

def frame_end():
    img = Image.new("RGB", (W, H), BASE)
    draw = ImageDraw.Draw(img)
    f = get_font(16)
    text = "threshold visual essays"
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-10), text, fill=VDIM, font=f)
    return draw_vignette(img, 100)

frames = [
    ("00_title", frame_title), ("01_objects", frame_objects),
    ("02_why", frame_why), ("03_pareidolia", frame_pareidolia),
    ("04_best_feature", frame_best_feature), ("05_empathy", frame_empathy),
    ("06_rehearsing", frame_rehearsing), ("07_chat", frame_chat),
    ("08_please", frame_please), ("09_web", frame_web),
    ("10_about_you", frame_about_you), ("11_connected", frame_connected),
    ("12_keep", frame_keep), ("13_stay_human", frame_stay_human),
    ("14_coda", frame_coda), ("15_end", frame_end),
]

out_dir = "/tmp/talk-remake"
for name, func in frames:
    path = f"{out_dir}/{name}.png"
    img = func()
    img.save(path)
    print(f"Saved {path}")
print(f"\nDone! {len(frames)} frames.")
