# Project Memory

## Summary
CubeRoller is a set of single-file Three.js demos: a 3D numbered cube rolling on a grid and a 4D tesseract analog projected to 3D that rolls across a 3D grid. Both animate in 90° steps with orientation preserved.

## Current State
- No build system or dependencies managed in-repo.
- Everything lives in single HTML files.
- UI is in Russian with simple controls for movement, restart, and grid size.

## Key Features
- 3D scene with ambient + directional light.
- Numbered cube faces generated as canvas textures.
- Grid size configurable (1–20) with camera recentering.
- Movement constrained to grid bounds.
- 4D tesseract projected into 3D as line segments.
- 4D rolling via rotations in axis–w planes.

## Project Structure
- `cube3d.html`: Entire app (HTML, CSS, JS). Includes Three.js via CDN.
- `cube4d.html`: 4D tesseract rolling demo (HTML, CSS, JS). Includes Three.js via CDN.
- `README.md`: Basic usage and project overview.

## How To Run
- Open `cube3d.html` directly in a modern browser.
- Controls:
  - Buttons: Вверх/Вниз/Влево/Вправо
  - Arrow keys: Up/Down/Left/Right
  - Restart resets cube orientation/position
  - Grid size input + apply button

## Notes
- Cube face numbering is defined by `numberMap` in `cube3d.html`.
- Movement uses a pivot object for animated rolling.
- Grid bounds are enforced before starting a rotation.
