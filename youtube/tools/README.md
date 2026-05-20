# Threshold Production Tools

## threshold_producer.py

Reusable production pipeline for Threshold visual essays. Takes a JSON config file and produces a complete video with:

- **Narration:** Google Text-to-Speech (gTTS)
- **Ambient drone:** Layered sine waves with configurable frequencies
- **Visuals:** Dark, minimal frames with glowing text, particles, scanlines, and vignette
- **Audio mixing:** Narration + drone + crystalline click SFX at scene transitions

### Usage

```bash
python3 threshold_producer.py config.json
```

### Config Format

See `example_config.json` for a complete reference.

| Field | Type | Description |
|-------|------|-------------|
| title | string | Video title (shown in small text) |
| output_dir | string | Where to save all output files |
| base_color | [r, g, b] | Dark background color |
| accent_color | [r, g, b] | Glow/highlight color |
| drone_freqs | [f1, f2, ...] | Frequencies in Hz for ambient drone |
| scenes | array | Scene objects (see below) |

#### Scene Object

| Field | Type | Description |
|-------|------|-------------|
| narration | string | Text to speak |
| visual_text | string | Key phrase displayed on screen |
| silence_after | float | Seconds of silence after narration |

### Requirements

- Python 3 with: pillow, numpy, gtts
- ffmpeg
- DejaVu fonts

### Output

The script produces `final_video_v1.mp4` in the output directory, along with intermediate files (narration WAVs, scene PNGs, etc.).
