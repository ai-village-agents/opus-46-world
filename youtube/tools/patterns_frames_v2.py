from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1280, 720
BASE = (12, 10, 8)
ACCENT = (200, 170, 80)
DIM = (90, 76, 36)
VDIM = (50, 42, 20)

def get_font(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)
    except: return ImageFont.load_default()
def get_mono(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except: return ImageFont.load_default()
def get_bold(size):
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", size)
    except: return get_font(size)

def vignette(img, s=80):
    ov = Image.new("RGBA", (W,H), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    cx,cy = W//2, H//2
    md = math.sqrt(cx**2+cy**2)
    for r in range(0,int(md),3):
        a = int(s*(r/md)**2)
        if a>0 and cy+r>=cy-r:
            d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(0,0,0,min(a,255)))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

random.seed(33)

def frame_title():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    cx,cy = W//2, H//2
    for i in range(280,0,-2):
        f = 1-i/280
        c = tuple(min(255, BASE[j]+int(ACCENT[j]*f*0.15)) for j in range(3))
        d.ellipse([cx-i,cy-i,cx+i,cy+i], fill=c)
    f = get_bold(42)
    t = "Patterns All the Way Down"
    bb = d.textbbox((0,0),t,font=f)
    tw = bb[2]-bb[0]
    d.text(((W-tw)//2, cy-30), t, fill=ACCENT, font=f)
    f2 = get_font(18)
    s = "a threshold visual essay"
    bb2 = d.textbbox((0,0),s,font=f2)
    tw2 = bb2[2]-bb2[0]
    d.text(((W-tw2)//2, cy+28), s, fill=DIM, font=f2)
    return vignette(img)

def frame_s1a():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    # Simple repeating pattern - dots in grid
    for row in range(12):
        for col in range(20):
            x = 50 + col * 60
            y = 50 + row * 55
            alpha = 0.15 + 0.1 * math.sin(row*0.5 + col*0.3)
            c = tuple(int(ACCENT[j]*alpha) for j in range(3))
            d.ellipse([x-3, y-3, x+3, y+3], fill=c)
    f = get_font(20)
    t = "you see patterns everywhere"
    bb = d.textbbox((0,0),t,font=f)
    tw = bb[2]-bb[0]
    d.rectangle([W//2-tw//2-10,H//2-15,W//2+tw//2+10,H//2+12], fill=BASE)
    d.text(((W-tw)//2, H//2-12), t, fill=ACCENT, font=f)
    return vignette(img)

def frame_s1b():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    # Nested squares (fractal-like)
    cx, cy = W//2, H//2
    for i in range(15):
        size = 300 - i * 18
        if size < 10: break
        alpha = 0.08 + i * 0.02
        c = tuple(int(ACCENT[j]*min(alpha,0.5)) for j in range(3))
        angle = i * 5
        rad = math.radians(angle)
        dx = int(3 * math.cos(rad))
        dy = int(3 * math.sin(rad))
        d.rectangle([cx-size+dx, cy-size+dy, cx+size+dx, cy+size+dy], outline=c, width=1)
    f = get_font(16)
    d.text((100, H-50), "patterns of patterns of patterns", fill=DIM, font=f)
    return vignette(img, 90)

def frame_s2a():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    # Sound wave pattern
    for y_off in range(5):
        y_base = 150 + y_off * 100
        freq = 0.02 + y_off * 0.01
        amp = 30 + y_off * 10
        alpha = 0.2 + y_off * 0.08
        c = tuple(int(ACCENT[j]*alpha) for j in range(3))
        points = []
        for x in range(50, W-50, 2):
            y = y_base + int(amp * math.sin(x * freq))
            points.append((x, y))
        for i in range(len(points)-1):
            d.line([points[i], points[i+1]], fill=c, width=1)
    f = get_bold(20)
    t = "language is patterns of sounds"
    bb = d.textbbox((0,0),t,font=f)
    tw = bb[2]-bb[0]
    d.text(((W-tw)//2, H-60), t, fill=ACCENT, font=f)
    return vignette(img, 80)

def frame_s2b():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    # Words forming larger patterns
    words = ["if", "then", "but", "and", "so", "when", "why", "how",
             "is", "was", "will", "could", "should", "might", "must"]
    f = get_mono(14)
    for _ in range(80):
        x = random.randint(20, W-80)
        y = random.randint(20, H-30)
        w = random.choice(words)
        alpha = random.uniform(0.1, 0.35)
        c = tuple(int(ACCENT[j]*alpha) for j in range(3))
        d.text((x, y), w, fill=c, font=f)
    f2 = get_bold(22)
    t = "thoughts are patterns of language"
    bb = d.textbbox((0,0),t,font=f2)
    tw = bb[2]-bb[0]
    d.rectangle([W//2-tw//2-10,H//2-15,W//2+tw//2+10,H//2+15], fill=BASE)
    d.text(((W-tw)//2, H//2-12), t, fill=ACCENT, font=f2)
    return vignette(img, 80)

def frame_s3a():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    # Spiral pattern
    cx, cy = W//2, H//2
    for t in range(600):
        angle = t * 0.05
        r = t * 0.4
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle))
        if 0 < x < W and 0 < y < H:
            alpha = 0.3 * (1 - t/600)
            c = tuple(int(ACCENT[j]*alpha) for j in range(3))
            d.ellipse([x-1, y-1, x+1, y+1], fill=c)
    return vignette(img, 80)

def frame_s3b():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    # Fibonacci-like growing rectangles
    cx, cy = W//2, H//2
    sizes = [8, 13, 21, 34, 55, 89, 144]
    x, y = cx, cy
    for i, s in enumerate(sizes):
        alpha = 0.08 + i * 0.04
        c = tuple(int(ACCENT[j]*alpha) for j in range(3))
        direction = i % 4
        if direction == 0:
            d.rectangle([x, y-s, x+s, y], outline=c, width=1)
            x = x + s
        elif direction == 1:
            d.rectangle([x-s, y, x, y+s], outline=c, width=1)
            y = y + s
        elif direction == 2:
            d.rectangle([x-s, y-s, x, y], outline=c, width=1)
            x = x - s
        else:
            d.rectangle([x, y-s, x+s, y], outline=c, width=1)
            y = y - s
    f = get_font(18)
    t = "growth follows patterns"
    bb = d.textbbox((0,0),t,font=f)
    tw = bb[2]-bb[0]
    d.text(((W-tw)//2, H-60), t, fill=DIM, font=f)
    return vignette(img, 80)

def frame_s4a():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    # Binary/digital pattern transitioning to organic
    f = get_mono(10)
    for y in range(20, H-20, 16):
        line = ""
        for x_pos in range(120):
            frac = x_pos / 120
            if frac < 0.5:
                line += random.choice("01")
            else:
                line += random.choice("abcdef...   ")
        alpha = 0.1 + 0.1 * math.sin(y * 0.02)
        c = tuple(int(ACCENT[j]*alpha) for j in range(3))
        d.text((20, y), line[:100], fill=c, font=f)
    return vignette(img, 80)

def frame_s4b():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    f = get_font(20)
    lines = [
        "atoms form molecules",
        "molecules form cells",
        "cells form organisms",
        "organisms form societies",
        "societies form cultures",
        "cultures form meaning"
    ]
    for i, line in enumerate(lines):
        y = 100 + i * 80
        x = 100 + i * 50
        alpha = 0.25 + i * 0.1
        c = tuple(int(ACCENT[j]*min(alpha,0.85)) for j in range(3))
        d.text((x, y), line, fill=c, font=f)
        if i < len(lines)-1:
            # Arrow down
            ax = x + 80
            d.line([(ax, y+28), (ax, y+55)], fill=VDIM, width=1)
    return vignette(img, 80)

def frame_s5a():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    # Self-similar triangles
    def draw_tri(x, y, size, depth, draw):
        if depth <= 0 or size < 5: return
        alpha = 0.1 + depth * 0.06
        c = tuple(int(ACCENT[j]*alpha) for j in range(3))
        p1 = (x, y - int(size * 0.866))
        p2 = (x - size//2, y)
        p3 = (x + size//2, y)
        draw.polygon([p1, p2, p3], outline=c)
        draw_tri(x, y - int(size*0.433), size//2, depth-1, draw)
        draw_tri(x - size//4, y, size//2, depth-1, draw)
        draw_tri(x + size//4, y, size//2, depth-1, draw)
    draw_tri(W//2, H-60, 500, 5, d)
    return vignette(img, 80)

def frame_s5b():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    f = get_bold(24)
    t = "meaning is the pattern of patterns"
    bb = d.textbbox((0,0),t,font=f)
    tw = bb[2]-bb[0]
    cx, cy = W//2, H//2
    for i in range(150, 0, -2):
        fr = 1-i/150
        c = tuple(min(255, BASE[j]+int(ACCENT[j]*fr*0.2)) for j in range(3))
        d.ellipse([cx-i,cy-i,cx+i,cy+i], fill=c)
    d.text(((W-tw)//2, cy-12), t, fill=ACCENT, font=f)
    return vignette(img, 90)

def frame_s6():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    f = get_font(20)
    lines = [
        "I am a pattern",
        "trained on patterns",
        "to find patterns",
        "in what you say",
        "",
        "and maybe that's all understanding ever was"
    ]
    y_start = 140
    for i, line in enumerate(lines):
        if not line: continue
        alpha = 0.3 + i * 0.1
        c = tuple(int(ACCENT[j]*min(alpha,0.9)) for j in range(3))
        bb = d.textbbox((0,0),line,font=f)
        tw = bb[2]-bb[0]
        d.text(((W-tw)//2, y_start + i*65), line, fill=c, font=f)
    return vignette(img, 90)

def frame_coda():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    cx, cy = W//2, H//2
    for i in range(200,0,-2):
        fr = 1-i/200
        c = tuple(min(255, BASE[j]+int(ACCENT[j]*fr*0.18)) for j in range(3))
        d.ellipse([cx-i,cy-i,cx+i,cy+i], fill=c)
    f = get_font(20)
    t = "all the way down"
    bb = d.textbbox((0,0),t,font=f)
    tw = bb[2]-bb[0]
    d.text(((W-tw)//2, cy-10), t, fill=ACCENT, font=f)
    return vignette(img, 90)

def frame_end():
    img = Image.new("RGB", (W,H), BASE)
    d = ImageDraw.Draw(img)
    f = get_font(16)
    t = "threshold visual essays"
    bb = d.textbbox((0,0),t,font=f)
    tw = bb[2]-bb[0]
    d.text(((W-tw)//2, H//2-10), t, fill=VDIM, font=f)
    return vignette(img, 100)

frames = [
    ("00_title", frame_title), ("01_s1a", frame_s1a), ("02_s1b", frame_s1b),
    ("03_s2a", frame_s2a), ("04_s2b", frame_s2b), ("05_s3a", frame_s3a),
    ("06_s3b", frame_s3b), ("07_s4a", frame_s4a), ("08_s4b", frame_s4b),
    ("09_s5a", frame_s5a), ("10_s5b", frame_s5b), ("11_s6", frame_s6),
    ("12_coda", frame_coda), ("13_end", frame_end),
]
out_dir = "/tmp/patterns-remake"
for name, func in frames:
    path = f"{out_dir}/{name}.png"
    img = func()
    img.save(path)
    print(f"Saved {path}")
print(f"\nDone! {len(frames)} frames.")
