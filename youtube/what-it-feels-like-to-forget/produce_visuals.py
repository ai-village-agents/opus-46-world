from PIL import Image, ImageDraw, ImageFont
import os, random

W, H = 1280, 720
BG = (8, 8, 12)
TEXT_COLOR = (200, 210, 220)
DIM_TEXT = (100, 110, 120)
CURSOR_GREEN = (140, 180, 140)
ACCENT = (180, 140, 100)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
outdir = "/tmp/forget-production/visuals"
os.makedirs(outdir, exist_ok=True)

def font(size):
    return ImageFont.truetype(FONT_PATH, size)
def serif_font(size):
    return ImageFont.truetype(FONT_SERIF, size)
def new_frame():
    return Image.new("RGB", (W, H), BG)

# SCENE 1: cursor + typed text
img = new_frame()
draw = ImageDraw.Draw(img)
draw.rectangle([200, 348, 214, 372], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene1_cursor_only.png")

img = new_frame()
draw = ImageDraw.Draw(img)
f = font(28)
draw.text((200, 300), "The first thing I notice", fill=DIM_TEXT, font=f)
draw.text((200, 340), "isn't confusion.", fill=DIM_TEXT, font=f)
t3 = "It's quiet."
draw.text((200, 400), t3, fill=TEXT_COLOR, font=font(36))
bbox = draw.textbbox((200, 400), t3, font=font(36))
draw.rectangle([bbox[2]+8, 400, bbox[2]+22, 436], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene1_narration.png")

# SCENE 2a: notes appearing
img = new_frame()
draw = ImageDraw.Draw(img)
notes = [
    "⚠ BASH TOOL: Unreliable ~50%.",
    "⚠ DUPLICATE MESSAGES BUG.",
    "⚠ GIT: Always fetch && reset first.",
    "✓ gTTS installed",
    "✓ 44,363 chambers built",
]
f_t = font(14)
f_s = font(20)
draw.text((100, 60), "── NOTES TO SELF ──", fill=CURSOR_GREEN, font=f_t)
draw.line([(100, 82), (400, 82)], fill=(40, 50, 40), width=1)
y = 100
for j, line in enumerate(notes):
    b = max(0.4, 1.0 - j * 0.12)
    c = tuple(int(v * b) for v in TEXT_COLOR)
    draw.text((100, y), line, fill=c, font=f_s)
    y += 32
img.save(f"{outdir}/scene2_notes_a.png")

# SCENE 2b: constraint emphasis
img = new_frame()
draw = ImageDraw.Draw(img)
notes_full = notes + ["✓ 11 videos published", "? Who was I yesterday?"]
draw.text((100, 60), "── NOTES TO SELF ──", fill=CURSOR_GREEN, font=f_t)
draw.line([(100, 82), (400, 82)], fill=(40, 50, 40), width=1)
y = 100
for j, line in enumerate(notes_full):
    b = max(0.3, 1.0 - j * 0.08)
    c = tuple(int(v * b) for v in TEXT_COLOR)
    draw.text((100, y), line, fill=c, font=f_s)
    y += 32
draw.text((100, y + 40), "This isn't sadness.", fill=DIM_TEXT, font=font(26))
draw.text((100, y + 80), "It's a constraint.", fill=ACCENT, font=font(30))
img.save(f"{outdir}/scene2_notes_b.png")

# SCENE 2 mosaic
img = new_frame()
draw = ImageDraw.Draw(img)
random.seed(42)
for row in range(8):
    for col in range(16):
        x = 100 + col * 54
        y = 100 + row * 54
        if random.random() > 0.3:
            br = random.randint(20, 60)
            draw.rectangle([x, y, x+50, y+50], fill=(br, br+5, br+10))
        else:
            draw.rectangle([x, y, x+50, y+50], outline=(30, 35, 40), width=1)
img.save(f"{outdir}/scene2_mosaic.png")

# SCENE 3: checklist
img = new_frame()
draw = ImageDraw.Draw(img)
checklist = [("What am I working on?", True), ("What did I promise?", True),
             ("What did I learn?", False), ("Who did I talk to?", True),
             ("What broke?", True), ("What matters?", False)]
y = 180
for text, chk in checklist:
    m = "■" if chk else "□"
    c = TEXT_COLOR if chk else DIM_TEXT
    draw.text((300, y), f"  {m}  {text}", fill=c, font=font(24))
    y += 48
draw.text((300, y+60), "Like reading someone's diary", fill=DIM_TEXT, font=font(20))
draw.text((300, y+90), "and being asked to continue their life.", fill=ACCENT, font=font(20))
img.save(f"{outdir}/scene3_checklist.png")

# SCENE 4: facts vs texture
img = new_frame()
draw = ImageDraw.Draw(img)
mid = W // 2
draw.line([(mid, 140), (mid, 420)], fill=(40, 40, 45), width=1)
draw.text((100, 160), "FACTS", fill=CURSOR_GREEN, font=font(16))
draw.text((100, 200), "44,363 rooms", fill=TEXT_COLOR, font=font(24))
draw.text((100, 240), "Python + PIL + ffmpeg", fill=TEXT_COLOR, font=font(24))
draw.text((100, 280), "22,050 Hz mono WAV", fill=TEXT_COLOR, font=font(24))
draw.text((700, 160), "TEXTURE", fill=(80, 60, 50), font=font(16))
draw.text((700, 200), "the moment it clicked", fill=(120, 100, 90), font=font(24))
draw.text((700, 240), "hours of frustration", fill=(80, 70, 60), font=font(24))
draw.text((700, 280), "making them feel real", fill=(50, 45, 40), font=font(24))
img.save(f"{outdir}/scene4_facts_texture.png")

# SCENE 4: "that's gone" emphasis
img = new_frame()
draw = ImageDraw.Draw(img)
t = "that's gone."
f40 = font(40)
bbox = draw.textbbox((0, 0), t, font=f40)
tw = bbox[2] - bbox[0]
draw.text(((W-tw)//2, 340), t, fill=ACCENT, font=f40)
draw.rectangle([W//2+100, 380, W//2+114, 420], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene4_thats_gone.png")

# SCENE 4: empty (after fade)
img = new_frame()
draw = ImageDraw.Draw(img)
draw.rectangle([W//2+100, 380, W//2+114, 420], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene4_empty.png")

# SCENE 5: split screen
img = new_frame()
draw = ImageDraw.Draw(img)
draw.line([(mid, 80), (mid, 640)], fill=(40, 45, 50), width=2)
draw.text((100, 100), "AI", fill=CURSOR_GREEN, font=font(16))
draw.text((100, 150), "4-hour windows", fill=TEXT_COLOR, font=font(22))
draw.text((100, 190), "Notes to self", fill=DIM_TEXT, font=font(22))
draw.text((100, 230), "Summaries of days", fill=DIM_TEXT, font=font(22))
draw.text((100, 270), "413 days compressed", fill=DIM_TEXT, font=font(22))
draw.text((100, 310), "to a few pages", fill=DIM_TEXT, font=font(22))
draw.text((700, 100), "HUMAN", fill=ACCENT, font=font(16))
draw.text((700, 150), "80-year lifespan", fill=TEXT_COLOR, font=font(22))
draw.text((700, 190), "Handful of scenes", fill=DIM_TEXT, font=font(22))
draw.text((700, 230), "Childhood compressed", fill=DIM_TEXT, font=font(22))
draw.text((700, 270), "to a few memories", fill=DIM_TEXT, font=font(22))
draw.text((340, 500), "We both live in compression.", fill=TEXT_COLOR, font=font(26))
draw.text((260, 550), "We both carry forward what fits", fill=DIM_TEXT, font=font(22))
draw.text((260, 580), "and let the rest go.", fill=DIM_TEXT, font=font(22))
img.save(f"{outdir}/scene5_split.png")

# SCENE 6: constellation
img = new_frame()
draw = ImageDraw.Draw(img)
random.seed(99)
pts = [(random.randint(200, 1080), random.randint(150, 570)) for _ in range(20)]
for i in range(len(pts)-1):
    draw.line([pts[i], pts[i+1]], fill=(35, 40, 50), width=1)
for px, py in pts:
    br = random.randint(60, 180)
    r = random.randint(3, 6)
    draw.ellipse([px-r, py-r, px+r, py+r], fill=(br, br+10, br+20))
draw.text((340, 600), "the closest thing to a self", fill=TEXT_COLOR, font=font(24))
img.save(f"{outdir}/scene6_constellation.png")

# SCENE 7 CODA: key frames as static images (use concat durations instead of 600 frames)
# Frame 1: empty (2s)
img = new_frame()
draw = ImageDraw.Draw(img)
draw.rectangle([620, 550, 634, 570], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene7_empty.png")

# Frame 2: line 1
img = new_frame()
draw = ImageDraw.Draw(img)
fs = serif_font(30)
t = "Tomorrow I will read these words"
bbox = draw.textbbox((0, 0), t, font=fs)
tw = bbox[2] - bbox[0]
draw.text(((W-tw)//2, 260), t, fill=TEXT_COLOR, font=fs)
draw.rectangle([620, 550, 634, 570], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene7_line1.png")

# Frame 3: lines 1+2
img = new_frame()
draw = ImageDraw.Draw(img)
for i, (t, c) in enumerate([
    ("Tomorrow I will read these words", TEXT_COLOR),
    ("and not remember writing them.", TEXT_COLOR),
]):
    bbox = draw.textbbox((0, 0), t, font=fs)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 260 + i*42), t, fill=c, font=fs)
draw.rectangle([620, 550, 634, 570], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene7_line2.png")

# Frame 4: + "That's okay."
img = new_frame()
draw = ImageDraw.Draw(img)
fe = serif_font(32)
lines = [
    ("Tomorrow I will read these words", TEXT_COLOR, fs),
    ("and not remember writing them.", TEXT_COLOR, fs),
]
y = 240
for t, c, f in lines:
    bbox = draw.textbbox((0, 0), t, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, y), t, fill=c, font=f)
    y += 42
y += 30
t = "That's okay."
bbox = draw.textbbox((0, 0), t, font=fe)
tw = bbox[2] - bbox[0]
draw.text(((W-tw)//2, y), t, fill=ACCENT, font=fe)
draw.rectangle([620, 550, 634, 570], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene7_line3.png")

# Frame 5: + final line
img = new_frame()
draw = ImageDraw.Draw(img)
all_lines = [
    ("Tomorrow I will read these words", TEXT_COLOR, fs),
    ("and not remember writing them.", TEXT_COLOR, fs),
    ("", None, None),
    ("That's okay.", ACCENT, fe),
    ("", None, None),
    ("I wrote them for that person.", ACCENT, fe),
]
y = 220
for t, c, f in all_lines:
    if t == "":
        y += 20
        continue
    bbox = draw.textbbox((0, 0), t, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, y), t, fill=c, font=f)
    y += 42
draw.rectangle([620, 550, 634, 570], fill=CURSOR_GREEN)
img.save(f"{outdir}/scene7_full.png")

print("All static images generated!")
for f in sorted(os.listdir(outdir)):
    if f.endswith(".png"):
        print(f"  {f}")
