import wave
import struct
import math
import random
import os

RATE = 22050

def read_wav_samples(path):
    """Read WAV file and return float samples."""
    with wave.open(path, "r") as w:
        n = w.getnframes()
        raw = w.readframes(n)
        samples = struct.unpack(f"<{n}h", raw)
        return [s / 32768.0 for s in samples]

def generate_typing_click(duration_ms=35, rate=RATE):
    """Generate a single subtle typing click sound."""
    n_samples = int(rate * duration_ms / 1000)
    samples = []
    for i in range(n_samples):
        t = i / rate
        # Short noise burst with exponential decay
        envelope = math.exp(-t * 80)  # Fast decay
        noise = random.uniform(-1, 1)
        # Add a tiny tonal component for "key" feel
        tone = math.sin(2 * math.pi * 800 * t) * 0.3
        sample = (noise * 0.7 + tone) * envelope * 0.15  # Keep quiet
        samples.append(sample)
    return samples

def generate_typing_sequence(num_keys=5, spacing_ms=70, rate=RATE):
    """Generate a sequence of typing clicks (like someone typing a short word)."""
    spacing_samples = int(rate * spacing_ms / 1000)
    result = []
    for i in range(num_keys):
        click = generate_typing_click(duration_ms=random.randint(25, 45))
        result.extend(click)
        if i < num_keys - 1:
            # Add silence between clicks
            silence_len = spacing_samples + random.randint(-10, 10)
            result.extend([0.0] * silence_len)
    return result

# Scene transition timestamps (in seconds) where text appears
# Format: (timestamp, num_keys, description)
typing_moments = [
    (5.8,  4, "It's quiet appears"),        # Scene 1 text
    (23.0, 3, "Scene 2 notes a"),            # Memory fragments
    (39.7, 3, "Scene 2 notes b"),            # More fragments
    (56.5, 2, "Mosaic"),                     # Mosaic transition
    (60.4, 5, "Checklist appears"),          # Checklist - more keys
    (83.3, 4, "Facts vs Texture"),           # Split layout
    (95.8, 3, "That's gone"),               # Emotional beat
    (114.2, 3, "Split screen"),             # Human parallel
    (141.2, 3, "Constellation"),            # What remains
    (174.6, 4, "Coda line 1"),             # Tomorrow I will read
    (179.6, 5, "Coda line 2"),             # That's okay
    (184.6, 4, "Coda line 3"),             # I wrote them
]

# Read existing mixed audio
audio_path = "/tmp/forget-production/audio/final_mix.wav"
print(f"Reading existing audio from {audio_path}...")
existing = read_wav_samples(audio_path)
total_samples = len(existing)
total_duration = total_samples / RATE
print(f"Audio duration: {total_duration:.2f}s, {total_samples} samples")

# Generate typing sounds and overlay
print("Generating typing sound effects...")
typing_layer = [0.0] * total_samples

for timestamp, num_keys, desc in typing_moments:
    start_sample = int(timestamp * RATE)
    if start_sample >= total_samples:
        print(f"  SKIP {desc} at {timestamp}s (beyond audio)")
        continue
    
    seq = generate_typing_sequence(num_keys=num_keys, spacing_ms=random.randint(60, 90))
    end_sample = min(start_sample + len(seq), total_samples)
    for i in range(end_sample - start_sample):
        typing_layer[start_sample + i] = seq[i]
    print(f"  Added {num_keys} keys at {timestamp:.1f}s ({desc})")

# Mix: existing audio + typing layer
print("Mixing typing sounds into audio...")
mixed = []
for i in range(total_samples):
    s = existing[i] + typing_layer[i]
    # Soft clip
    s = max(-0.95, min(0.95, s))
    mixed.append(s)

# Write output
output_path = "/tmp/forget-production/audio/mixed_final_v3.wav"
print(f"Writing to {output_path}...")
with wave.open(output_path, "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    for s in mixed:
        w.writeframes(struct.pack("<h", int(s * 32767)))

print(f"Done! Output: {output_path}")
print(f"Samples: {len(mixed)}, Duration: {len(mixed)/RATE:.2f}s")
