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
    n_samples = int(RATE * duration_ms / 1000)
    samples = []
    random.seed(42)
    for i in range(n_samples):
        t = i / RATE
        tone = 0.6 * math.sin(2 * math.pi * 2400 * t)
        tone += 0.3 * math.sin(2 * math.pi * 3600 * t)
        tone += 0.1 * math.sin(2 * math.pi * 4800 * t)
        decay = math.exp(-t * 40)
        noise = 0
        if t < 0.005:
            noise = random.uniform(-0.3, 0.3) * (1 - t/0.005)
        samples.append((tone * decay + noise) * 32767 * 0.7)
    return samples

transitions = [5.0, 10.0, 15.0, 24.8, 35.0, 42.0, 51.2, 65.0, 83.5, 100.0, 113.2, 125.0, 146.5, 160.0, 172.5]

existing = read_wav("/tmp/space-tokens-production/extracted_audio.wav")
print(f"Audio: {len(existing)/RATE:.1f}s")

click_volume = 0.20
for ts in transitions:
    click = crystalline_click(80)
    start_sample = int((ts - 0.03) * RATE)
    if start_sample < 0:
        start_sample = 0
    for j, s in enumerate(click):
        idx = start_sample + j
        if idx < len(existing):
            existing[idx] = int(existing[idx] + s * click_volume)

existing = [max(-32768, min(32767, s)) for s in existing]
write_wav("/tmp/space-tokens-production/audio_v2.wav", existing)
print(f"V2 audio: {len(existing)/RATE:.1f}s with {len(transitions)} clicks")
