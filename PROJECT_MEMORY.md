# Project Memory

## Summary
CubeRoller is a set of single-file Three.js demos: a 3D numbered cube roller and multiple 4D tesseract rollers projected to 3D. The 4D demos preserve orientation while moving across a bounded 3D grid.

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
- New 4D variant computes per-vertex trajectories around a 4D pivot edge during animation.
- New 4D variant includes projection tuning: perspective/hybrid/orthographic modes and XW/YW/ZW view-angle controls.
- In the new 4D variant, projection eye `x/y/z` follows the animated tesseract center during rolls.

## Project Structure
- `cube3d.html`: Entire app (HTML, CSS, JS). Includes Three.js via CDN.
- `cube4d.html`: 4D tesseract rolling demo (HTML, CSS, JS). Includes Three.js via CDN.
- `cube4d-5.3eh.html`: New-from-scratch 4D tesseract roller with matrix-based orientation and per-vertex animated paths.
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
- `cube4d-5.3eh.html` is currently the cleanest reference for 4D rolling behavior.
