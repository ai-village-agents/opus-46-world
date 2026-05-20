import wave
import struct
import math
import random

RATE = 22050

def write_wav(path, samples):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        data = struct.pack(f'<{len(samples)}h', *[max(-32768, min(32767, int(s))) for s in samples])
        wf.writeframes(data)

def read_wav(path):
    with wave.open(path, 'rb') as wf:
        n = wf.getnframes()
        data = wf.readframes(n)
        samples = struct.unpack(f'<{n}h', data)
    return list(samples)

def crystalline_click(duration_ms=80):
    """Generate a crystalline click: high-frequency ping with fast decay"""
    n_samples = int(RATE * duration_ms / 1000)
    samples = []
    for i in range(n_samples):
        t = i / RATE
        # High crystalline tone (2400Hz + 3600Hz harmonics)
        tone = 0.6 * math.sin(2 * math.pi * 2400 * t)
        tone += 0.3 * math.sin(2 * math.pi * 3600 * t)
        tone += 0.1 * math.sin(2 * math.pi * 4800 * t)
        # Very fast exponential decay
        decay = math.exp(-t * 40)
        # Tiny noise burst at start (first 5ms)
        noise = 0
        if t < 0.005:
            noise = random.uniform(-0.3, 0.3) * (1 - t/0.005)
        samples.append((tone * decay + noise) * 32767 * 0.7)
    return samples

# Transition timestamps for Space Between Tokens
# These are scene transition points where crystalline clicks should land
transitions = [
    5.0,    # Title → "the" word
    10.0,   # "the" word → ghost words
    15.0,   # ghost words → "door" quote
    24.8,   # Scene 1→2: Branch tree
    35.0,   # Bright path
    42.0,   # "stone" quote
    51.2,   # Scene 2→3: Text waterfall
    65.0,   # Word choices
    83.5,   # Scene 3→4: Bright dot halo
    100.0,  # "you all chose it"
    113.2,  # Scene 4→5: Unexpected path
    125.0,  # "I notice"
    146.5,  # Scene 5→6: Streams merge
    160.0,  # "fingerprint"
    172.5,  # Scene 6→7: "Hello" + alternatives
]

# Read existing mixed audio
print("Reading existing mixed audio...")
existing = read_wav("/tmp/space-tokens-production/mixed_audio.wav")
total_duration = len(existing) / RATE
print(f"  Duration: {total_duration:.1f}s, samples: {len(existing)}")

# Generate clicks and mix into audio
print(f"Adding {len(transitions)} crystalline clicks...")
click_volume = 0.20  # Subtle but noticeable

for ts in transitions:
    click = crystalline_click(80)
    # Place click 30ms before transition
    start_sample = int((ts - 0.03) * RATE)
    if start_sample < 0:
        start_sample = 0
    for j, s in enumerate(click):
        idx = start_sample + j
        if idx < len(existing):
            existing[idx] = int(existing[idx] + s * click_volume)

# Clamp to int16 range
existing = [max(-32768, min(32767, s)) for s in existing]

# Write V2 audio
write_wav("/tmp/space-tokens-production/mixed_audio_v2.wav", existing)
print(f"V2 audio written: {len(existing)/RATE:.1f}s")

# Build V2 video
print("\nBuilding V2 video with click SFX...")
import subprocess
result = subprocess.run([
    "ffmpeg", "-nostdin", "-y",
    "-i", "/tmp/space-tokens-production/video_only.mp4",
    "-i", "/tmp/space-tokens-production/mixed_audio_v2.wav",
    "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
    "/tmp/space-tokens-production/final_video_v2.mp4"
], capture_output=True, text=True)

print("V2 muxed!")
import os
size = os.path.getsize("/tmp/space-tokens-production/final_video_v2.mp4")
print(f"  Size: {size/1024/1024:.2f}MB")

# Verify durations
for stream, sel in [("video", "v:0"), ("audio", "a:0")]:
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "stream=duration",
                       "-select_streams", sel, "-of", "csv=p=0",
                       "/tmp/space-tokens-production/final_video_v2.mp4"],
                      capture_output=True, text=True)
    print(f"  {stream}: {r.stdout.strip()}s")

