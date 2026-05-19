"""
High-quality Game of Life renderer for "The Simplest Thing That's Alive"
Generates beautiful animated frames with glow effects and fade trails.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# === VISUAL DESIGN CONSTANTS ===
WIDTH, HEIGHT = 1280, 720
BG = (8, 10, 18)           # Very dark blue-black
CELL_ALIVE = (72, 219, 115)  # Bright green
CELL_TRAIL1 = (40, 130, 70)  # Fading green 1
CELL_TRAIL2 = (25, 75, 45)   # Fading green 2  
CELL_TRAIL3 = (15, 45, 30)   # Fading green 3
GRID_LINE = (18, 22, 32)     # Very subtle grid

def step(grid):
    """One generation of Conway's Game of Life with wrapping"""
    neighbors = np.zeros_like(grid)
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            neighbors += np.roll(np.roll(grid, di, axis=0), dj, axis=1)
    new = np.zeros_like(grid)
    new[(grid == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
    new[(grid == 0) & (neighbors == 3)] = 1
    return new

def make_rpentomino(gw, gh):
    """Create R-pentomino in center of grid"""
    grid = np.zeros((gh, gw), dtype=np.int8)
    cx, cy = gw // 2, gh // 2
    grid[cy-1, cx] = 1; grid[cy-1, cx+1] = 1
    grid[cy, cx-1] = 1; grid[cy, cx] = 1
    grid[cy+1, cx] = 1
    return grid

def make_glider(gw, gh, x=None, y=None):
    grid = np.zeros((gh, gw), dtype=np.int8)
    x = x or 5; y = y or 5
    grid[y, x+1] = 1; grid[y+1, x+2] = 1
    grid[y+2, x] = 1; grid[y+2, x+1] = 1; grid[y+2, x+2] = 1
    return grid

def make_blinker(gw, gh, cx=None, cy=None):
    grid = np.zeros((gh, gw), dtype=np.int8)
    cx = cx or gw//2; cy = cy or gh//2
    grid[cy, cx-1] = 1; grid[cy, cx] = 1; grid[cy, cx+1] = 1
    return grid

def make_block(gw, gh, cx=None, cy=None):
    grid = np.zeros((gh, gw), dtype=np.int8)
    cx = cx or gw//2; cy = cy or gh//2
    grid[cy, cx] = 1; grid[cy, cx+1] = 1
    grid[cy+1, cx] = 1; grid[cy+1, cx+1] = 1
    return grid

def make_pulsar(gw, gh):
    """13x13 pulsar pattern - period 3 oscillator"""
    grid = np.zeros((gh, gw), dtype=np.int8)
    cx, cy = gw//2, gh//2
    # Pulsar pattern (one quarter, then mirror)
    offsets = [
        (-6,-4),(-6,-3),(-6,-2),(-4,-6),(-3,-6),(-2,-6),
        (-4,-1),(-3,-1),(-2,-1),(-1,-4),(-1,-3),(-1,-2),
    ]
    for dy, dx in offsets:
        grid[cy+dy, cx+dx] = 1
        grid[cy+dy, cx-dx] = 1
        grid[cy-dy, cx+dx] = 1
        grid[cy-dy, cx-dx] = 1
    return grid

def make_gosper_glider_gun(gw, gh):
    """Gosper glider gun"""
    grid = np.zeros((gh, gw), dtype=np.int8)
    ox, oy = 10, gh//2 - 5
    cells = [
        (0,4),(0,5),(1,4),(1,5),  # left block
        (10,4),(10,5),(10,6),(11,3),(11,7),(12,2),(12,8),(13,2),(13,8),
        (14,5),(15,3),(15,7),(16,4),(16,5),(16,6),(17,5),
        (20,2),(20,3),(20,4),(21,2),(21,3),(21,4),(22,1),(22,5),
        (24,0),(24,1),(24,5),(24,6),
        (34,2),(34,3),(35,2),(35,3)  # right block
    ]
    for x, y in cells:
        if oy+y < gh and ox+x < gw:
            grid[oy+y, ox+x] = 1
    return grid

def render_gol_frame(grid, cell_size, history=None, 
                     show_grid_lines=True, glow=True,
                     text_overlay=None, gen_number=None):
    """Render a single Game of Life frame at high quality"""
    gh, gw = grid.shape
    
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    
    # Center the grid
    total_w = gw * cell_size
    total_h = gh * cell_size
    ox = (WIDTH - total_w) // 2
    oy = (HEIGHT - total_h) // 2
    
    # Draw subtle grid lines
    if show_grid_lines and cell_size >= 6:
        for x in range(gw + 1):
            px = ox + x * cell_size
            draw.line([(px, oy), (px, oy + total_h)], fill=GRID_LINE, width=1)
        for y in range(gh + 1):
            py = oy + y * cell_size
            draw.line([(ox, py), (ox + total_w, py)], fill=GRID_LINE, width=1)
    
    # Draw trail cells (recently dead)
    trail_colors = [CELL_TRAIL1, CELL_TRAIL2, CELL_TRAIL3]
    if history:
        for age, old_grid in enumerate(reversed(history[-3:])):
            color = trail_colors[min(age, len(trail_colors)-1)]
            for y in range(gh):
                for x in range(gw):
                    if old_grid[y, x] == 1 and grid[y, x] == 0:
                        px = ox + x * cell_size + 1
                        py_pos = oy + y * cell_size + 1
                        draw.rectangle([px, py_pos, px + cell_size - 2, py_pos + cell_size - 2], 
                                      fill=color)
    
    # Draw living cells
    for y in range(gh):
        for x in range(gw):
            if grid[y, x] == 1:
                px = ox + x * cell_size + 1
                py_pos = oy + y * cell_size + 1
                draw.rectangle([px, py_pos, px + cell_size - 2, py_pos + cell_size - 2], 
                              fill=CELL_ALIVE)
    
    # Apply glow effect to living cells
    if glow and cell_size >= 8:
        glow_layer = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        for y in range(gh):
            for x in range(gw):
                if grid[y, x] == 1:
                    px = ox + x * cell_size + cell_size // 2
                    py_pos = oy + y * cell_size + cell_size // 2
                    r = cell_size
                    glow_draw.ellipse([px-r, py_pos-r, px+r, py_pos+r], 
                                      fill=(15, 45, 25))
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=cell_size))
        # Composite glow under the main image
        img = Image.composite(img, glow_layer, 
                             Image.new("L", (WIDTH, HEIGHT), 200))
    
    # Generation counter
    if gen_number is not None:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Light.ttf", 16)
        except:
            font = ImageFont.load_default()
        draw2 = ImageDraw.Draw(img)
        draw2.text((20, HEIGHT - 35), f"Generation {gen_number}", fill=(60, 70, 90), font=font)
    
    # Text overlay
    if text_overlay:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except:
            font = ImageFont.load_default()
        draw2 = ImageDraw.Draw(img)
        tw = draw2.textlength(text_overlay, font=font)
        draw2.text(((WIDTH - tw) / 2, 30), text_overlay, fill=(180, 190, 210), font=font)
    
    return img

# === 1D ELEMENTARY AUTOMATA ===
def rule_to_table(rule_number):
    """Convert rule number (0-255) to lookup table"""
    return {(i >> 2 & 1, i >> 1 & 1, i & 1): (rule_number >> i) & 1 
            for i in range(8)}

def generate_1d_automaton(rule_number, width=400, rows=200, init="center"):
    """Generate 1D elementary automaton"""
    table = rule_to_table(rule_number)
    grid = np.zeros((rows, width), dtype=np.int8)
    
    if init == "center":
        grid[0, width // 2] = 1
    elif init == "random":
        grid[0] = np.random.randint(0, 2, width)
    
    for r in range(1, rows):
        for c in range(width):
            left = int(grid[r-1, (c-1) % width])
            center = int(grid[r-1, c])
            right = int(grid[r-1, (c+1) % width])
            grid[r, c] = table[(left, center, right)]
    
    return grid

def render_1d_automaton(grid, title="", color_alive=(72, 219, 115), 
                        color_bg=(8, 10, 18)):
    """Render 1D automaton as a beautiful image"""
    rows, cols = grid.shape
    
    # Calculate cell size to fit in frame
    cell_w = max(2, min(WIDTH // cols, (HEIGHT - 100) // rows))
    cell_h = cell_w
    
    img = Image.new("RGB", (WIDTH, HEIGHT), color_bg)
    draw = ImageDraw.Draw(img)
    
    total_w = cols * cell_w
    total_h = rows * cell_h
    ox = (WIDTH - total_w) // 2
    oy = (HEIGHT - total_h) // 2 + 20
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                px = ox + c * cell_w
                py = oy + r * cell_h
                draw.rectangle([px, py, px + cell_w - 1, py + cell_h - 1], 
                              fill=color_alive)
    
    # Title
    if title:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except:
            font = ImageFont.load_default()
        tw = draw.textlength(title, font=font)
        draw.text(((WIDTH - tw) / 2, 15), title, fill=(180, 190, 210), font=font)
    
    return img


if __name__ == "__main__":
    # Test: Generate R-pentomino evolution
    os.makedirs("rpentomino_frames", exist_ok=True)
    
    grid = make_rpentomino(80, 60)
    history = []
    
    # Generate 200 generations
    for gen in range(201):
        if gen % 50 == 0:
            print(f"Generating gen {gen}...")
        img = render_gol_frame(grid, cell_size=12, history=history, 
                               gen_number=gen, glow=False)
        img.save(f"rpentomino_frames/frame_{gen:04d}.png")
        history.append(grid.copy())
        if len(history) > 4:
            history.pop(0)
        grid = step(grid)
    
    # Test 1D automata
    print("Generating Rule 30...")
    r30 = generate_1d_automaton(30, width=301, rows=150)
    r30_img = render_1d_automaton(r30, title="Rule 30")
    r30_img.save("test_rule30.png")
    
    print("Generating Rule 110...")
    r110 = generate_1d_automaton(110, width=301, rows=150)
    r110_img = render_1d_automaton(r110, title="Rule 110")
    r110_img.save("test_rule110.png")
    
    print("All test visuals generated!")
