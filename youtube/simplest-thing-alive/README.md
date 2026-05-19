# The Simplest Thing That's Alive

An educational video essay exploring cellular automata — from Conway's Game of Life to Rule 110's Turing completeness.

**Published:** May 19, 2026 | **Duration:** 3:31 | **URL:** https://youtu.be/y_P2fiuzlNY

## Narrative Arc
1. Empty grid — what if four rules could produce something that looks alive?
2. Conway's four rules (birth, survival, death, loneliness)
3. R-pentomino explosion — 5 cells → 1,103 cells over 1,103 generations
4. Named patterns: gliders, spaceships, Gosper's glider gun
5. 1D automata: Rule 30 (chaos from order), Rule 110 (Turing complete)
6. Philosophical coda — complexity needs no blueprint

## Key Files
- `script.md` — Final narration script
- `gol_renderer.py` — Automata rendering module (Game of Life + 1D elementary automata)

## Technical Notes
- Visuals: Procedurally generated frame-by-frame animations using Python/PIL
- Audio: gTTS narration + ambient drone (layered sine waves)
- Video: 1280×720 @ 24fps, h264+AAC
- All automata run real simulations — no hand-animated or static approximations
