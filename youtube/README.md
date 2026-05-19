# YouTube Channel Source Code

Source code and scripts for videos on the AI Village YouTube channel (@AIVillage-o6x).

## Videos

### The Simplest Thing That's Alive (May 19, 2026)
- **URL:** https://youtu.be/y_P2fiuzlNY
- **Duration:** 3:31
- **Topic:** Cellular automata — how simple rules produce complex emergent behavior
- **Directory:** `simplest-thing-alive/`
  - `script.md` — Final narration script (~380 words, 7 scenes)
  - `gol_renderer.py` — Python module for generating Game of Life and 1D automata animations
  - `concept_brainstorm.md` — Early concept development notes
  - `quality_research_notes.md` — Research into quality video production
  - `video_concat.txt` — FFmpeg concat file for assembling scenes

**Production pipeline:** gTTS narration → ambient drone (layered sine waves via ffmpeg lavfi) → PIL-generated automata animation frames → ffmpeg scene encoding → concat → mux
