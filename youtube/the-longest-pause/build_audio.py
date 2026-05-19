import wave
import struct
import math
import random

RATE = 22050
outdir = "/tmp/longest-pause-production"

def read_wav(path):
    with wave.open(path, 'rb') as wf:
        n = wf.getnframes()
        data = wf.readframes(n)
        return list(struct.unpack(f'<{n}h', data))

def write_wav(path, samples):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        data = struct.pack(f'<{len(samples)}h', *[max(-32768, min(32767, int(s))) for s in samples])
        wf.writeframes(data)

def silence(seconds):
    return [0] * int(RATE * seconds)

scenes = {}
for i in range(1, 8):
    scenes[f"scene{i}"] = read_wav(f"{outdir}/scene{i}.wav")

# Build with silences - target 180s
full = []
timestamps = []

# Title: 5s
full.extend(silence(5.0))
timestamps.append(("title", 0.0, 5.0))

# Scene 1: ~20.7s + 2s silence
start = len(full) / RATE
full.extend(scenes["scene1"])
end = len(full) / RATE
full.extend(silence(2.0))
timestamps.append(("scene1", start, end))

# Scene 2: ~29.8s + 1.5s silence
start = len(full) / RATE
full.extend(scenes["scene2"])
end = len(full) / RATE
full.extend(silence(1.5))
timestamps.append(("scene2", start, end))

# Scene 3: ~27.8s + 2s silence
start = len(full) / RATE
full.extend(scenes["scene3"])
end = len(full) / RATE
full.extend(silence(2.0))
timestamps.append(("scene3", start, end))

# Scene 4: ~27.2s + 2s silence
start = len(full) / RATE
full.extend(scenes["scene4"])
end = len(full) / RATE
full.extend(silence(2.0))
timestamps.append(("scene4", start, end))

# Scene 5: ~29.3s + 2s silence
start = len(full) / RATE
full.extend(scenes["scene5"])
end = len(full) / RATE
full.extend(silence(2.0))
timestamps.append(("scene5", start, end))

# Scene 6: ~19.8s + 2s silence
start = len(full) / RATE
full.extend(scenes["scene6"])
end = len(full) / RATE
full.extend(silence(2.0))
timestamps.append(("scene6", start, end))

# Scene 7: ~4.2s
start = len(full) / RATE
full.extend(scenes["scene7"])
end = len(full) / RATE
timestamps.append(("scene7", start, end))

# Pad to 180s
target = int(RATE * 180)
if len(full) < target:
    full.extend(silence((target - len(full)) / RATE))
full = full[:target]

print(f"Narration: {len(full)/RATE:.1f}s")
write_wav(f"{outdir}/narration_full.wav", full)

# Timestamps
for name, s, e in timestamps:
    print(f"  {name}: {s:.1f} - {e:.1f}")

# Ambient drone: deep teal, ethereal
# A minor: A2(110Hz), E3(164.8Hz), A3(220Hz), C4(261.6Hz)
print("\nGenerating ambient drone...")
random.seed(99)
drone = [0.0] * target
freqs = [110.0, 164.8, 220.0, 261.6]
amps = [0.3, 0.25, 0.2, 0.15]

for i in range(target):
    t = i / RATE
    val = 0.0
    for freq, amp in zip(freqs, amps):
        mod = 1.0 + 0.25 * math.sin(2 * math.pi * 0.06 * t + freq * 0.1)
        val += amp * mod * math.sin(2 * math.pi * freq * t)
    # Subtle shimmer
    shimmer = 0.04 * math.sin(2 * math.pi * 523.3 * t) * math.sin(2 * math.pi * 0.12 * t)
    val += shimmer
    # Fades
    if t < 3.0: val *= t / 3.0
    elif t > 175.0: val *= (180.0 - t) / 5.0
    drone[i] = val

max_d = max(abs(d) for d in drone)
drone = [d / max_d for d in drone]

# Mix 0.85/0.15
print("Mixing...")
mixed = []
for i in range(target):
    n = full[i] / 32768.0
    d = drone[i]
    mixed.append(int((0.85 * n + 0.15 * d) * 32767))

write_wav(f"{outdir}/mixed_audio.wav", mixed)
print(f"Mixed: {len(mixed)/RATE:.1f}s")
