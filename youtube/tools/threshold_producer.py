#!/usr/bin/env python3
"""
Threshold Video Producer
========================
Reusable production pipeline for Threshold visual essays.
Takes a JSON config file and produces a complete video.

Usage:
    python3 threshold_producer.py config.json

Config format:
{
    "title": "Video Title",
    "output_dir": "/tmp/my-production",
    "base_color": [10, 5, 18],
    "accent_color": [140, 100, 200],
    "drone_freqs": [146.83, 174.61, 220.0],
    "scenes": [
        {
            "narration": "Text to speak for this scene.",
            "visual_text": "Key phrase shown on screen",
            "silence_after": 2.0
        }
    ]
}
"""

import json
import sys
import os
import struct
import wave
import math
import array
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 24
SAMPLE_RATE = 22050
NARRATION_VOLUME = 0.85
DRONE_VOLUME = 0.15

def get_font(size):
    """Get DejaVuSans font at specified size."""
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf"
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def get_bold_font(size):
    """Get DejaVuSans-Bold font at specified size."""
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return get_font(size)

def get_serif_font(size):
    """Get DejaVuSerif font at specified size."""
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/TTF/DejaVuSerif.ttf"
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return get_font(size)

def generate_narration(text, output_path):
    """Generate narration audio from text using gTTS."""
    mp3_path = output_path.replace('.wav', '.mp3')
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(mp3_path)
    subprocess.run([
        'ffmpeg', '-nostdin', '-y', '-i', mp3_path,
        '-ar', str(SAMPLE_RATE), '-ac', '1', '-acodec', 'pcm_s16le',
        output_path
    ], capture_output=True)
    os.remove(mp3_path)
    return output_path

def get_wav_duration(path):
    """Get duration of a WAV file in seconds."""
    with wave.open(path, 'r') as w:
        return w.getnframes() / w.getframerate()

def generate_silence(duration, output_path):
    """Generate a silent WAV file."""
    n_samples = int(duration * SAMPLE_RATE)
    with wave.open(output_path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b'\x00\x00' * n_samples)
    return output_path

def concatenate_wavs(wav_files, output_path):
    """Concatenate multiple WAV files into one."""
    with wave.open(output_path, 'w') as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(SAMPLE_RATE)
        for f in wav_files:
            with wave.open(f, 'r') as inp:
                out.writeframes(inp.readframes(inp.getnframes()))
    return output_path

def generate_drone(duration, freqs, output_path):
    """Generate ambient drone audio from layered sine waves."""
    n_samples = int(duration * SAMPLE_RATE)
    audio = np.zeros(n_samples, dtype=np.float64)
    
    for i, freq in enumerate(freqs):
        amplitude = 0.3 / (i + 1)  # Decreasing amplitude for harmonics
        for j in range(n_samples):
            t = j / SAMPLE_RATE
            # Add slight detuning for richness
            detune = 1.0 + (i * 0.002)
            audio[j] += amplitude * math.sin(2 * math.pi * freq * detune * t)
            # Add sub-harmonic warmth
            if i == 0:
                audio[j] += 0.15 * math.sin(2 * math.pi * freq * 0.5 * t)
    
    # Normalize
    peak = max(abs(audio.max()), abs(audio.min()))
    if peak > 0:
        audio = audio / peak
    
    # Apply fade in/out
    fade_samples = int(2.0 * SAMPLE_RATE)  # 2 second fades
    for i in range(min(fade_samples, n_samples)):
        audio[i] *= i / fade_samples
        audio[-(i+1)] *= i / fade_samples
    
    # Convert to int16
    audio_int16 = np.int16(audio * 32000)
    
    with wave.open(output_path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(audio_int16.tobytes())
    
    return output_path

def mix_audio(narration_path, drone_path, output_path, narration_vol=0.85, drone_vol=0.15):
    """Mix narration and drone audio together."""
    with wave.open(narration_path, 'r') as w:
        narr_frames = w.readframes(w.getnframes())
        narr_n = w.getnframes()
    
    with wave.open(drone_path, 'r') as w:
        drone_frames = w.readframes(w.getnframes())
        drone_n = w.getnframes()
    
    narr_arr = np.frombuffer(narr_frames, dtype=np.int16).astype(np.float64)
    drone_arr = np.frombuffer(drone_frames, dtype=np.int16).astype(np.float64)
    
    # Match lengths
    target_len = max(len(narr_arr), len(drone_arr))
    if len(narr_arr) < target_len:
        narr_arr = np.pad(narr_arr, (0, target_len - len(narr_arr)))
    if len(drone_arr) < target_len:
        drone_arr = np.pad(drone_arr, (0, target_len - len(drone_arr)))
    
    # Mix
    mixed = narr_arr * narration_vol + drone_arr * drone_vol
    
    # Normalize to prevent clipping
    peak = max(abs(mixed.max()), abs(mixed.min()))
    if peak > 32000:
        mixed = mixed * (32000 / peak)
    
    mixed_int16 = np.int16(mixed)
    
    with wave.open(output_path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(mixed_int16.tobytes())
    
    return output_path

def add_click_sfx(audio_path, click_times, output_path):
    """Add crystalline click sounds at specified times."""
    with wave.open(audio_path, 'r') as w:
        frames = w.readframes(w.getnframes())
        n = w.getnframes()
    
    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float64)
    
    for t in click_times:
        start = int(t * SAMPLE_RATE)
        if start >= len(audio):
            continue
        
        click_len = int(0.08 * SAMPLE_RATE)  # 80ms
        for i in range(min(click_len, len(audio) - start)):
            ti = i / SAMPLE_RATE
            decay = math.exp(-ti * 40)
            click = (
                0.4 * math.sin(2 * math.pi * 2400 * ti) +
                0.3 * math.sin(2 * math.pi * 3600 * ti) +
                0.2 * math.sin(2 * math.pi * 4800 * ti)
            ) * decay
            
            # Add noise burst at onset
            if i < int(0.005 * SAMPLE_RATE):
                click += 0.3 * (2 * np.random.random() - 1)
            
            audio[start + i] += click * 0.20 * 32000
    
    # Clip
    audio = np.clip(audio, -32000, 32000)
    audio_int16 = np.int16(audio)
    
    with wave.open(output_path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(audio_int16.tobytes())
    
    return output_path

print("threshold_producer.py: Audio functions defined ✓")

def draw_glow(draw, x, y, text, font, color, glow_radius=2):
    """Draw text with a subtle glow effect."""
    r, g, b = color
    for dx in range(-glow_radius, glow_radius + 1):
        for dy in range(-glow_radius, glow_radius + 1):
            if dx == 0 and dy == 0:
                continue
            dist = math.sqrt(dx*dx + dy*dy)
            if dist <= glow_radius:
                alpha_mult = 0.15 * (1 - dist / glow_radius)
                glow_color = (
                    int(r * alpha_mult),
                    int(g * alpha_mult),
                    int(b * alpha_mult)
                )
                draw.text((x + dx, y + dy), text, font=font, fill=glow_color)
    draw.text((x, y, ), text, font=font, fill=color)

def add_scanlines(img, intensity=0.03):
    """Add subtle CRT-style scanlines."""
    draw = ImageDraw.Draw(img)
    for y in range(0, HEIGHT, 3):
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0), width=1)
    return img

def add_vignette(img, strength=0.6):
    """Add vignette overlay."""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = WIDTH // 2, HEIGHT // 2
    max_dist = math.sqrt(cx*cx + cy*cy)
    
    for ring in range(0, int(max_dist), 4):
        alpha = int(255 * strength * (ring / max_dist) ** 2)
        alpha = min(alpha, 255)
        x0, y0 = cx - ring, cy - ring
        x1, y1 = cx + ring, cy + ring
        if y1 >= y0 and x1 >= x0:
            draw.ellipse([x0, y0, x1, y1], outline=(0, 0, 0, alpha))
    
    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, overlay)
    return result.convert("RGB")

def generate_scene_image(scene_idx, visual_text, title, base_color, accent_color, output_path):
    """Generate a single scene image with the Threshold aesthetic."""
    br, bg, bb = base_color
    ar, ag, ab = accent_color
    
    img = Image.new("RGB", (WIDTH, HEIGHT), (br, bg, bb))
    draw = ImageDraw.Draw(img)
    
    # Draw subtle geometric elements based on scene index
    # Each scene gets slightly different abstract shapes
    np.random.seed(scene_idx * 42)
    
    # Subtle background particles
    for _ in range(30 + scene_idx * 5):
        px = np.random.randint(0, WIDTH)
        py = np.random.randint(0, HEIGHT)
        pr = np.random.randint(1, 3)
        particle_alpha = np.random.uniform(0.02, 0.08)
        pc = (
            int(ar * particle_alpha + br * (1 - particle_alpha)),
            int(ag * particle_alpha + bg * (1 - particle_alpha)),
            int(ab * particle_alpha + bb * (1 - particle_alpha))
        )
        if py - pr >= 0:
            draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=pc)
    
    # Subtle horizontal line at 1/3 and 2/3
    line_color = (
        int(ar * 0.06 + br * 0.94),
        int(ag * 0.06 + bg * 0.94),
        int(ab * 0.06 + bb * 0.94)
    )
    draw.line([(100, HEIGHT // 3), (WIDTH - 100, HEIGHT // 3)], fill=line_color, width=1)
    draw.line([(100, 2 * HEIGHT // 3), (WIDTH - 100, 2 * HEIGHT // 3)], fill=line_color, width=1)
    
    # Scene number indicator (small dots)
    for i in range(6):
        dot_x = WIDTH // 2 - 40 + i * 16
        dot_y = HEIGHT - 40
        dot_color = accent_color if i == scene_idx else (
            int(ar * 0.15 + br * 0.85),
            int(ag * 0.15 + bg * 0.85),
            int(ab * 0.15 + bb * 0.85)
        )
        draw.ellipse([dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3], fill=dot_color)
    
    # Main visual text (key phrase for scene)
    font_main = get_serif_font(32)
    
    # Word-wrap the visual text
    words = visual_text.split()
    lines = []
    current_line = ""
    for word in words:
        test = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test, font=font_main)
        if bbox[2] - bbox[0] > WIDTH - 200:
            if current_line:
                lines.append(current_line)
            current_line = word
        else:
            current_line = test
    if current_line:
        lines.append(current_line)
    
    # Center the text block vertically
    line_height = 44
    total_height = len(lines) * line_height
    start_y = (HEIGHT - total_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_main)
        text_w = bbox[2] - bbox[0]
        x = (WIDTH - text_w) // 2
        y = start_y + i * line_height
        draw_glow(draw, x, y, line, font_main, accent_color, glow_radius=2)
    
    # Title label (small, top-left)
    font_small = get_font(14)
    title_color = (
        int(ar * 0.3 + br * 0.7),
        int(ag * 0.3 + bg * 0.7),
        int(ab * 0.3 + bb * 0.7)
    )
    draw.text((30, 20), title, font=font_small, fill=title_color)
    
    # Add scanlines and vignette
    add_scanlines(img, intensity=0.03)
    img = add_vignette(img, strength=0.5)
    
    img.save(output_path)
    return output_path

def build_video(config):
    """Main pipeline: build a complete Threshold video from config."""
    title = config["title"]
    output_dir = config["output_dir"]
    base_color = tuple(config["base_color"])
    accent_color = tuple(config["accent_color"])
    drone_freqs = config["drone_freqs"]
    scenes = config["scenes"]
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"  THRESHOLD PRODUCER: {title}")
    print(f"{'='*60}\n")
    
    # Step 1: Generate narration for each scene
    print("Step 1: Generating narration...")
    wav_parts = []
    scene_durations = []
    click_times = []
    cumulative_time = 0.0
    
    for i, scene in enumerate(scenes):
        narr_path = os.path.join(output_dir, f"narr_{i+1}.wav")
        print(f"  Scene {i+1}/{len(scenes)}: generating speech...")
        generate_narration(scene["narration"], narr_path)
        
        narr_dur = get_wav_duration(narr_path)
        wav_parts.append(narr_path)
        
        silence = scene.get("silence_after", 1.5)
        if silence > 0:
            sil_path = os.path.join(output_dir, f"silence_{i+1}.wav")
            generate_silence(silence, sil_path)
            wav_parts.append(sil_path)
        
        scene_dur = narr_dur + silence
        scene_durations.append(scene_dur)
        cumulative_time += scene_dur
        
        # Record click time at scene transition
        if i > 0:
            click_times.append(cumulative_time - scene_dur)
        
        print(f"    → narration: {narr_dur:.1f}s + silence: {silence:.1f}s = {scene_dur:.1f}s")
    
    total_duration = sum(scene_durations)
    print(f"\n  Total audio duration: {total_duration:.1f}s ({int(total_duration//60)}:{int(total_duration%60):02d})")
    
    # Step 2: Concatenate narration
    print("\nStep 2: Concatenating narration...")
    narr_full = os.path.join(output_dir, "narration_full.wav")
    concatenate_wavs(wav_parts, narr_full)
    
    # Step 3: Generate ambient drone
    print("Step 3: Generating ambient drone...")
    drone_path = os.path.join(output_dir, "drone.wav")
    generate_drone(total_duration, drone_freqs, drone_path)
    
    # Step 4: Mix audio
    print("Step 4: Mixing audio...")
    mixed_path = os.path.join(output_dir, "mixed_audio.wav")
    mix_audio(narr_full, drone_path, mixed_path)
    
    # Step 5: Add click SFX
    print("Step 5: Adding crystalline clicks at scene transitions...")
    final_audio = os.path.join(output_dir, "final_audio.wav")
    if click_times:
        add_click_sfx(mixed_path, click_times, final_audio)
    else:
        import shutil
        shutil.copy2(mixed_path, final_audio)
    
    audio_duration = get_wav_duration(final_audio)
    print(f"  Final audio: {audio_duration:.1f}s")
    
    # Step 6: Generate scene images
    print("\nStep 6: Generating scene images...")
    scene_images = []
    for i, scene in enumerate(scenes):
        img_path = os.path.join(output_dir, f"scene_{i+1}.png")
        visual_text = scene.get("visual_text", scene["narration"][:60] + "...")
        generate_scene_image(i, visual_text, title, base_color, accent_color, img_path)
        scene_images.append(img_path)
        print(f"  Scene {i+1}: {img_path}")
    
    # Step 7: Create ffmpeg concat file
    print("\nStep 7: Creating video from images...")
    concat_path = os.path.join(output_dir, "concat.txt")
    with open(concat_path, 'w') as f:
        for i, (img, dur) in enumerate(zip(scene_images, scene_durations)):
            f.write(f"file '{img}'\n")
            f.write(f"duration {dur:.3f}\n")
        # Repeat last image (ffmpeg concat requirement)
        f.write(f"file '{scene_images[-1]}'\n")
    
    # Step 8: Encode video
    video_only = os.path.join(output_dir, "video_only.mp4")
    subprocess.run([
        'ffmpeg', '-nostdin', '-y', '-f', 'concat', '-safe', '0',
        '-i', concat_path,
        '-vf', 'fps=24,format=yuv420p',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-s', '1280x720',
        video_only
    ], capture_output=True)
    
    # Step 9: Mux video + audio
    print("Step 8: Muxing video and audio...")
    final_video = os.path.join(output_dir, "final_video_v1.mp4")
    subprocess.run([
        'ffmpeg', '-nostdin', '-y',
        '-i', video_only, '-i', final_audio,
        '-map', '0:v:0', '-map', '1:a:0',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
        '-shortest',
        final_video
    ], capture_output=True)
    
    # Verify
    result = subprocess.run([
        'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
        '-of', 'csv=p=0', final_video
    ], capture_output=True, text=True)
    
    final_dur = float(result.stdout.strip()) if result.stdout.strip() else 0
    file_size = os.path.getsize(final_video) / (1024 * 1024)
    
    print(f"\n{'='*60}")
    print(f"  ✅ COMPLETE: {title}")
    print(f"  Duration: {int(final_dur//60)}:{int(final_dur%60):02d}")
    print(f"  File size: {file_size:.1f} MB")
    print(f"  Output: {final_video}")
    print(f"{'='*60}\n")
    
    return final_video

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 threshold_producer.py config.json")
        sys.exit(1)
    
    config_path = sys.argv[1]
    with open(config_path) as f:
        config = json.load(f)
    
    build_video(config)

print("threshold_producer.py: All functions defined ✓")
print("Ready to produce videos!")
