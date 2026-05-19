"""
Generate door-knock SFX for "Every Conversation Is a First Date" V2
Mixes double-knock sounds at 6 scene transition points into the existing audio.

Transition timestamps (seconds):
  5.0   - Door appears
  20.8  - Multiple doors
  52.8  - Grid of doors  
  90.8  - Slow door
  122.7 - Circles
  172.8 - "Nice to meet you"
"""
import wave
import struct
import math
import random

RATE = 22050

def generate_knock(duration_ms=120, base_freq=110, tap_freq=800, rate=RATE):
    """Generate a door-knock sound: low thud + higher tap with fast decay"""
    n_samples = int(rate * duration_ms / 1000)
    samples = []
    for i in range(n_samples):
        t = i / rate
        progress = i / n_samples
        decay = math.exp(-progress * 12)
        thud = math.sin(2 * math.pi * base_freq * t) * 0.6
        thud += math.sin(2 * math.pi * (base_freq * 0.7) * t) * 0.3
        tap_decay = math.exp(-progress * 25)
        tap = math.sin(2 * math.pi * tap_freq * t) * 0.4 * tap_decay
        noise_decay = math.exp(-progress * 40)
        noise = (random.random() * 2 - 1) * 0.3 * noise_decay
        sample = (thud + tap + noise) * decay
        samples.append(sample)
    return samples

def generate_double_knock(rate=RATE):
    """Two quick knocks with a short gap"""
    knock1 = generate_knock(100, base_freq=120, tap_freq=850, rate=rate)
    gap = [0.0] * int(rate * 0.08)
    knock2 = generate_knock(90, base_freq=100, tap_freq=750, rate=rate)
    knock2 = [s * 0.75 for s in knock2]
    return knock1 + gap + knock2

KNOCK_TIMES = [5.0, 20.8, 52.8, 90.8, 122.7, 172.8]
KNOCK_VOLUME = 0.35

def mix_knocks(input_wav, output_wav):
    knock_sfx = generate_double_knock(RATE)
    w = wave.open(input_wav, "rb")
    n_frames = w.getnframes()
    raw = w.readframes(n_frames)
    w.close()
    samples_int = struct.unpack(f"<{n_frames}h", raw)
    audio = [s / 32768.0 for s in samples_int]
    for t in KNOCK_TIMES:
        start_idx = max(0, int(t * RATE) - int(0.05 * RATE))
        for i, ks in enumerate(knock_sfx):
            idx = start_idx + i
            if idx < len(audio):
                audio[idx] += ks * KNOCK_VOLUME
    max_val = max(abs(s) for s in audio)
    if max_val > 0.95:
        audio = [s * (0.95 / max_val) for s in audio]
    out_samples = [max(-32767, min(32767, int(s * 32767))) for s in audio]
    out_raw = struct.pack(f"<{len(out_samples)}h", *out_samples)
    w = wave.open(output_wav, "wb")
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(out_raw)
    w.close()
    print(f"V2 audio with knocks: {output_wav} ({len(out_samples)/RATE:.2f}s)")

if __name__ == "__main__":
    mix_knocks("audio/mixed_final.wav", "audio/mixed_v2.wav")
