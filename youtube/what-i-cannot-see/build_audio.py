import wave
import struct
import math
import random
import os

RATE = 22050
outdir = "/tmp/cannot-see-production"

def read_wav(path):
    with wave.open(path, 'rb') as wf:
        n = wf.getnframes()
        data = wf.readframes(n)
        samples = struct.unpack(f'<{n}h', data)
    return list(samples)

def write_wav(path, samples):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        data = struct.pack(f'<{len(samples)}h', *[max(-32768, min(32767, int(s))) for s in samples])
        wf.writeframes(data)

def silence(seconds):
    return [0] * int(RATE * seconds)

# Read all scene narrations
scenes = {}
for i in range(1, 8):
    name = f"scene{i}"
    scenes[name] = read_wav(f"{outdir}/{name}.wav")
    print(f"  {name}: {len(scenes[name])/RATE:.1f}s")

# Build narration with silences
# Target: 180s total
# Timing plan:
#   0:00-5.0  Title silence (5s)
#   5.0-24.8  Scene 1 narration (19.8s)
#   24.8-27.3 Silence (2.5s)
#   27.3-57.2 Scene 2 narration (29.9s)
#   57.2-59.7 Silence (2.5s)
#   59.7-82.2 Scene 3 narration (22.5s)
#   82.2-84.2 Silence (2.0s)
#   84.2-113.9 Scene 4 narration (29.7s)
#   113.9-115.9 Silence (2.0s)
#   115.9-144.0 Scene 5 narration (28.1s)
#   144.0-146.5 Silence (2.5s)
#   146.5-165.3 Scene 6 narration (18.8s)
#   165.3-167.3 Silence (2.0s)
#   167.3-172.5 Scene 7 narration (5.2s)
#   172.5-180.0 End silence (7.5s)

full_narration = []
timestamps = []

# Title silence
full_narration.extend(silence(5.0))
timestamps.append(("title", 0.0, 5.0))

# Scene 1
start = len(full_narration) / RATE
full_narration.extend(scenes["scene1"])
end = len(full_narration) / RATE
full_narration.extend(silence(2.5))
timestamps.append(("scene1", start, end))
print(f"Scene 1: {start:.1f} - {end:.1f}")

# Scene 2
start = len(full_narration) / RATE
full_narration.extend(scenes["scene2"])
end = len(full_narration) / RATE
full_narration.extend(silence(2.5))
timestamps.append(("scene2", start, end))
print(f"Scene 2: {start:.1f} - {end:.1f}")

# Scene 3
start = len(full_narration) / RATE
full_narration.extend(scenes["scene3"])
end = len(full_narration) / RATE
full_narration.extend(silence(2.0))
timestamps.append(("scene3", start, end))
print(f"Scene 3: {start:.1f} - {end:.1f}")

# Scene 4
start = len(full_narration) / RATE
full_narration.extend(scenes["scene4"])
end = len(full_narration) / RATE
full_narration.extend(silence(2.0))
timestamps.append(("scene4", start, end))
print(f"Scene 4: {start:.1f} - {end:.1f}")

# Scene 5
start = len(full_narration) / RATE
full_narration.extend(scenes["scene5"])
end = len(full_narration) / RATE
full_narration.extend(silence(2.5))
timestamps.append(("scene5", start, end))
print(f"Scene 5: {start:.1f} - {end:.1f}")

# Scene 6
start = len(full_narration) / RATE
full_narration.extend(scenes["scene6"])
end = len(full_narration) / RATE
full_narration.extend(silence(2.0))
timestamps.append(("scene6", start, end))
print(f"Scene 6: {start:.1f} - {end:.1f}")

# Scene 7
start = len(full_narration) / RATE
full_narration.extend(scenes["scene7"])
end = len(full_narration) / RATE
timestamps.append(("scene7", start, end))
print(f"Scene 7: {start:.1f} - {end:.1f}")

# Pad to exactly 180s
target = int(RATE * 180)
if len(full_narration) < target:
    full_narration.extend(silence((target - len(full_narration)) / RATE))
full_narration = full_narration[:target]

print(f"\nTotal narration audio: {len(full_narration)/RATE:.1f}s")
write_wav(f"{outdir}/narration_full.wav", full_narration)

# Save timestamps
with open(f"{outdir}/timestamps.txt", "w") as f:
    for name, start, end in timestamps:
        f.write(f"{name}\t{start:.1f}\t{end:.1f}\n")

# ===== Generate ambient drone (deep violet/mystical) =====
# D minor ethereal: D2(73.4Hz), A2(110Hz), D3(146.8Hz), F3(174.6Hz)
print("\nGenerating ambient drone...")
random.seed(42)
drone = [0.0] * target

freqs = [73.4, 110.0, 146.8, 174.6]
amps = [0.3, 0.25, 0.2, 0.15]

for i in range(target):
    t = i / RATE
    val = 0.0
    for freq, amp in zip(freqs, amps):
        # Slow amplitude modulation for breathing feel
        mod = 1.0 + 0.3 * math.sin(2 * math.pi * 0.07 * t + freq * 0.1)
        val += amp * mod * math.sin(2 * math.pi * freq * t)
    
    # Add subtle high shimmer (mystical quality)
    shimmer = 0.05 * math.sin(2 * math.pi * 587.3 * t) * math.sin(2 * math.pi * 0.15 * t)
    val += shimmer
    
    # Fade in (3s) and fade out (5s)
    if t < 3.0:
        val *= t / 3.0
    elif t > 175.0:
        val *= (180.0 - t) / 5.0
    
    drone[i] = val

# Normalize drone
max_d = max(abs(d) for d in drone)
drone = [d / max_d for d in drone]

# Mix: 0.85 narration + 0.15 drone
print("Mixing narration + drone...")
mixed = []
max_n = max(abs(s) for s in full_narration) if max(abs(s) for s in full_narration) > 0 else 1
for i in range(target):
    n = full_narration[i] / 32768.0  # normalize to -1..1
    d = drone[i]
    m = 0.85 * n + 0.15 * d
    mixed.append(int(m * 32767))

write_wav(f"{outdir}/mixed_audio.wav", mixed)
print(f"Mixed audio: {len(mixed)/RATE:.1f}s")

# Print timestamps for concat file
print("\nTimestamp map for video:")
for name, start, end in timestamps:
    print(f"  {name}: {start:.1f}s - {end:.1f}s")

