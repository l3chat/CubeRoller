# Project Memory

## Summary
CubeRoller is a single-file Three.js demo that renders a numbered cube on a grid and lets the user roll it across the grid with buttons or arrow keys. The cube animates in 90° steps, preserving face orientation as it moves.

## Current State
- No build system or dependencies managed in-repo.
- Everything lives in a single HTML file.
- UI is in Russian with simple controls for movement, restart, and grid size.

## Key Features
- 3D scene with ambient + directional light.
- Numbered cube faces generated as canvas textures.
- Grid size configurable (1–20) with camera recentering.
- Movement constrained to grid bounds.

## Project Structure
- `cube3d.html`: Entire app (HTML, CSS, JS). Includes Three.js via CDN.

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
