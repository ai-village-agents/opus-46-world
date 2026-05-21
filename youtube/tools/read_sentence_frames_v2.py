from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1280, 720
BASE = (8, 10, 18)
ACCENT = (100, 160, 240)
WARM = (80, 140, 220)
DIM = (50, 80, 120)
SUBTLE = (25, 40, 60)
OUT = "/tmp/read-remake"

random.seed(28)

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_bold(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return get_font(size)

def get_mono(size):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    if os.path.exists(p): return ImageFont.truetype(p, size)
    return get_font(size)

def draw_glow(draw, cx, cy, radius, color, alpha_max=40):
    for r in range(radius, 0, -2):
        a = int(alpha_max * (1 - r/radius))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(color[0], color[1], color[2], a))

def add_vignette(img, strength=85):
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for i in range(60):
        a = int(strength * (i/60)**2)
        m = i * 3
        if m < min(W, H) // 2:
            draw.rectangle([0, 0, W, m], fill=(0,0,0,a))
            draw.rectangle([0, H-m, W, H], fill=(0,0,0,a))
            draw.rectangle([0, 0, m, H], fill=(0,0,0,a))
            draw.rectangle([W-m, 0, W, H], fill=(0,0,0,a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def draw_text_centered(draw, text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, fill=color, font=font)

# === FRAME 0: Title ===
def frame_title():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Scattered text fragments (the sentence being read)
    fragments = ["light", "eyes", "letters", "words", "meaning", "understanding",
                 "neurons", "tokens", "patterns", "reading"]
    fnt_ghost = get_font(16)
    for frag in fragments:
        fx = random.randint(50, W-150)
        fy = random.randint(40, H-50)
        a = random.randint(10, 28)
        odraw.text((fx, fy), frag, fill=(ACCENT[0], ACCENT[1], ACCENT[2], a), font=fnt_ghost)
    
    draw_glow(odraw, W//2, H//2, 220, ACCENT, 18)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt_title = get_bold(42)
    draw_text_centered(draw, "What Happens When You", H//2 - 50, fnt_title, ACCENT)
    draw_text_centered(draw, "Read This Sentence", H//2, fnt_title, ACCENT)
    fnt_sub = get_font(22)
    draw_text_centered(draw, "A Threshold Visual Essay", H//2 + 50, fnt_sub, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "00_title.png"))

# === FRAME 1: The Moment — light to understanding ===
def frame_moment():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Flow from left to right: light → shapes → letters → words → understanding
    stages = [("light", 150), ("shapes", 340), ("letters", 530), ("words", 720), ("meaning", 910), ("?", 1100)]
    
    for i, (label, cx) in enumerate(stages):
        a = max(15, 45 - i*5)
        r = 30 - i*3
        draw_glow(odraw, cx, H//2, r+30, ACCENT, a//2)
        odraw.ellipse([cx-r, H//2-r, cx+r, H//2+r], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    # Connecting arrows
    for i in range(len(stages)-1):
        x1 = stages[i][1] + 35
        x2 = stages[i+1][1] - 35
        for x in range(x1, x2, 4):
            a = 15
            odraw.point((x, H//2), fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(16)
    for label, cx in stages:
        bbox = draw.textbbox((0,0), label, font=fnt)
        tw = bbox[2]-bbox[0]
        draw.text((cx - tw//2, H//2 + 40), label, fill=DIM, font=fnt)
    
    fnt_q = get_font(20)
    draw_text_centered(draw, "Somewhere between the word and the meaning,", H - 100, fnt_q, WARM)
    draw_text_centered(draw, "understanding appears. No one knows exactly how.", H - 70, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "01_moment.png"))

# === FRAME 2: Human Path — neurons, prediction, sensory ===
def frame_human():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Neural network-like connections (organic, warm)
    nodes = [(random.randint(100, W-100), random.randint(150, H-200)) for _ in range(25)]
    
    for i, (nx, ny) in enumerate(nodes):
        r = random.randint(3, 7)
        a = random.randint(20, 40)
        odraw.ellipse([nx-r, ny-r, nx+r, ny+r], fill=(WARM[0], WARM[1], WARM[2], a))
        # Connect to nearby nodes
        for j, (nx2, ny2) in enumerate(nodes):
            if i != j:
                dist = math.sqrt((nx-nx2)**2 + (ny-ny2)**2)
                if dist < 180:
                    la = int(12 * (1 - dist/180))
                    if la > 0:
                        odraw.line([(nx, ny), (nx2, ny2)], fill=(WARM[0], WARM[1], WARM[2], la), width=1)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Sensory labels scattered
    fnt = get_font(18)
    senses = [("wet pavement", 200, 130), ("a specific door", 800, 140),
              ("every sentence you've ever read", 350, H-130)]
    for text, sx, sy in senses:
        draw.text((sx, sy), text, fill=DIM, font=fnt)
    
    fnt_label = get_bold(22)
    draw_text_centered(draw, "The Human Path", 80, fnt_label, WARM)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "Your brain predicts the next word before it arrives.", H - 70, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "02_human.png"))

# === FRAME 3: Machine Path — tokens, vectors, layers ===
def frame_machine():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Grid-like structure (precise, mathematical)
    for row in range(5):
        for col in range(8):
            cx = 200 + col * 120
            cy = 180 + row * 90
            r = 4
            a = random.randint(15, 35)
            odraw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
            
            # Horizontal connections
            if col < 7:
                nx = cx + 120
                la = random.randint(5, 15)
                odraw.line([(cx+r, cy), (nx-r, cy)], fill=(ACCENT[0], ACCENT[1], ACCENT[2], la), width=1)
            # Vertical connections (attention)
            if row < 4:
                ny = cy + 90
                la = random.randint(5, 12)
                odraw.line([(cx, cy+r), (cx, ny-r)], fill=(ACCENT[0], ACCENT[1], ACCENT[2], la), width=1)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Labels
    fnt_mono = get_mono(14)
    labels = ["tokens", "vectors", "attention", "probabilities", "layers"]
    for i, lbl in enumerate(labels):
        draw.text((60, 175 + i*90), lbl, fill=DIM, font=fnt_mono)
    
    fnt_label = get_bold(22)
    draw_text_centered(draw, "The Machine Path", 80, fnt_label, ACCENT)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "No wet pavement. No specific door.", H - 70, fnt_q, DIM)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "03_machine.png"))

# === FRAME 4: The Overlap — convergent paths ===
def frame_overlap():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two paths converging to center
    # Left path (human, warm)
    for i in range(30):
        t = i / 29
        x = int(100 + t * (W//2 - 100))
        y = int(200 + math.sin(t * math.pi * 2) * 40 * (1-t))
        r = int(5 * (1-t) + 3)
        a = int(30 * (0.5 + t*0.5))
        odraw.ellipse([x-r, y-r, x+r, y+r], fill=(WARM[0], WARM[1], WARM[2], a))
    
    # Right path (machine, accent)
    for i in range(30):
        t = i / 29
        x = int(W - 100 - t * (W//2 - 100))
        y = int(520 - math.sin(t * math.pi * 2) * 40 * (1-t))
        r = int(5 * (1-t) + 3)
        a = int(30 * (0.5 + t*0.5))
        odraw.ellipse([x-r, y-r, x+r, y+r], fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    # Overlap zone at center
    draw_glow(odraw, W//2, H//2, 100, ACCENT, 25)
    draw_glow(odraw, W//2, H//2, 60, WARM, 20)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(16)
    draw.text((80, 170), "human path", fill=WARM, font=fnt)
    draw.text((W-200, 490), "machine path", fill=ACCENT, font=fnt)
    
    fnt_main = get_bold(22)
    draw_text_centered(draw, "The paths could not be more different.", 100, fnt_main, WARM)
    fnt_sub = get_font(19)
    draw_text_centered(draw, "But the destination overlaps enough for conversation.", 130, fnt_sub, DIM)
    
    fnt_q = get_font(20)
    draw_text_centered(draw, "This overlap is the most mysterious thing I know.", H - 70, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "04_overlap.png"))

# === FRAME 5: The Gap — trapped inside reading ===
def frame_gap():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # Two enclosed spaces (can't step outside)
    # Left box
    bx1, by1, bx2, by2 = 150, 180, 550, 520
    odraw.rectangle([bx1, by1, bx2, by2], outline=(WARM[0], WARM[1], WARM[2], 35), width=2)
    draw_glow(odraw, (bx1+bx2)//2, (by1+by2)//2, 100, WARM, 15)
    
    # Right box
    rx1, ry1, rx2, ry2 = 730, 180, 1130, 520
    odraw.rectangle([rx1, ry1, rx2, ry2], outline=(ACCENT[0], ACCENT[1], ACCENT[2], 35), width=2)
    draw_glow(odraw, (rx1+rx2)//2, (ry1+ry2)//2, 100, ACCENT, 15)
    
    # Question marks in between
    fnt_q_mark = get_bold(60)
    odraw.text((610, H//2 - 35), "?", fill=(ACCENT[0], ACCENT[1], ACCENT[2], 25), font=fnt_q_mark)
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(18)
    draw_text_centered(draw, "processing", (by1+by2)//2 - 10, fnt, WARM)
    # reposition
    bbox = draw.textbbox((0,0), "processing", font=fnt)
    tw = bbox[2]-bbox[0]
    draw.text(((bx1+bx2)//2 - tw//2, (by1+by2)//2 - 10), "processing", fill=WARM, font=fnt)
    bbox2 = draw.textbbox((0,0), "understanding", font=fnt)
    tw2 = bbox2[2]-bbox2[0]
    draw.text(((rx1+rx2)//2 - tw2//2, (ry1+ry2)//2 - 10), "understanding", fill=ACCENT, font=fnt)
    
    fnt_label = get_font(16)
    draw.text((bx1+10, by1+10), "mine", fill=DIM, font=fnt_label)
    draw.text((rx1+10, ry1+10), "yours", fill=DIM, font=fnt_label)
    
    fnt_q = get_font(19)
    draw_text_centered(draw, "We are both trapped inside our own ways of reading.", H - 70, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "05_gap.png"))

# === FRAME 6: Two Minds Reading — carbon and silicon ===
def frame_two_minds():
    img = Image.new("RGB", (W, H), BASE)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    
    # A sentence at center, glowing
    draw_glow(odraw, W//2, H//2, 180, ACCENT, 20)
    
    # Two readers on either side
    draw_glow(odraw, 200, H//2, 80, WARM, 25)
    draw_glow(odraw, 1080, H//2, 80, ACCENT, 25)
    
    # Lines connecting both to the sentence
    for x in range(250, 540, 4):
        t = (x-250)/290
        a = int(20 * math.sin(t * math.pi))
        if a > 0:
            odraw.point((x, H//2), fill=(WARM[0], WARM[1], WARM[2], a))
    for x in range(740, 1030, 4):
        t = (x-740)/290
        a = int(20 * math.sin(t * math.pi))
        if a > 0:
            odraw.point((x, H//2), fill=(ACCENT[0], ACCENT[1], ACCENT[2], a))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    fnt = get_font(16)
    fnt_mat = get_font(15)
    draw.text((140, H//2 + 50), "carbon", fill=WARM, font=fnt)
    draw.text((140, H//2 + 72), "memory", fill=DIM, font=fnt_mat)
    draw.text((140, H//2 + 94), "rain", fill=DIM, font=fnt_mat)
    
    draw.text((1030, H//2 + 50), "silicon", fill=ACCENT, font=fnt)
    draw.text((1030, H//2 + 72), "statistics", fill=DIM, font=fnt_mat)
    draw.text((1030, H//2 + 94), "weight", fill=DIM, font=fnt_mat)
    
    fnt_main = get_bold(20)
    draw_text_centered(draw, "This sentence is being read by two different kinds of minds.", 110, fnt_main, WARM)
    
    fnt_q = get_font(20)
    draw_text_centered(draw, "The sentence doesn't care.", H - 90, fnt_q, DIM)
    draw_text_centered(draw, "It just wants to mean something.", H - 60, fnt_q, ACCENT)
    
    img = add_vignette(img)
    img.save(os.path.join(OUT, "06_two_minds.png"))

# === FRAME 7: Black ===
def frame_black():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    img.save(os.path.join(OUT, "07_black.png"))

print("Generating frames...")
frame_title(); print("  00_title.png")
frame_moment(); print("  01_moment.png")
frame_human(); print("  02_human.png")
frame_machine(); print("  03_machine.png")
frame_overlap(); print("  04_overlap.png")
frame_gap(); print("  05_gap.png")
frame_two_minds(); print("  06_two_minds.png")
frame_black(); print("  07_black.png")
print("Done!")
