# Project Memory

## Summary
CubeRoller is a set of single-file Three.js demos: a 3D numbered cube roller and multiple 4D tesseract rollers projected to 3D. The 4D demos preserve orientation while moving across a bounded 3D grid.

## Current State
- No build system or dependencies managed in-repo.
- Everything lives in single HTML files.
- UI is in Russian with simple controls for movement, restart, and grid size.
- `cube4d2.html` is the active annotated universal mobile tesseract roller prototype and contains an architecture/spec comment at the top of the file.

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
- In the new 4D variant, one cubic cell (`w = -0.5`) is selected and its 6 faces are labeled `1..6` with cube3d numbering.
- `cube4d2.html` renders a local 3D unfolding of a tesseract: one active cubic cell, six visible neighbors, and one external opposite cell.
- `cube4d2.html` initial local axes are oriented so cells 1, 2, and 3 begin on the camera-facing side without changing opposite pairs.
- `cube4d2.html` uses persistent per-cell quaternions in `state.orientations` and stores external detach normals in `state.pendingNormals`.
- `cube4d2.html` keeps the external cell visible and semi-transparent by storing its outside position in `state.externalPositions`; its initial fallback position sits behind cube 5 on the local forward axis, and returning external cells travel back along a high clearance arc while slerping to the required orientation, except direct back-through-same-face returns which snap into place.
- `cube4d2.html` uses the universal transition rule `A -> B`: `enter = opposite[A]`, `out = opposite[B]`, with the four common neighbors rotating on the unused axes.
- `cube4d2.html` avoids negative scale for external cells by combining two conceptual reflections into one rotation in `rotationFromTwoReflections()`.
- `cube4d2.html` has a responsive rebuilt control panel with static movement labels, path display disabled by default, and default field size 7.
- `cube4d2.html` renders Three.js inside `#sceneFrame`, keeping controls outside the canvas, using a bottom panel in portrait and a right-side vertical panel in landscape, fitting the camera close to the full field from a lower angle after resize/orientation/UI/field-size changes, and constraining OrbitControls pan/zoom so the field is not accidentally lost.
- `cube4d2.html` field projections draw red wall-surface dots plus one mutually perpendicular red surface line per coordinate axis with unit-spaced red markers only on dynamically selected far/back field faces; the blue field cube uses the same wall planes so red lines lie on its faces.
- `cube4d2.html` face numbers remain on numbered faces, with initial back (-Z) number faces mirrored; orientation markers use dot positions with dot count equal to the cell id, a small square for 0, and a blank bottom marker.

## Project Structure
- `cube3d.html`: Entire app (HTML, CSS, JS). Includes Three.js via CDN.
- `cube4d.html`: 4D tesseract rolling demo (HTML, CSS, JS). Includes Three.js via CDN.
- `cube4d2.html`: Annotated universal mobile tesseract roller. Single-file HTML using Three.js CDN and OrbitControls CDN.
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
- In `cube4d2.html`, preserve cell IDs `0..7` and opposite pairs `0<->7`, `1<->6`, `2<->5`, `3<->4`.
- In `cube4d2.html`, movement/orientation edits should start with `makeNextState()`, `runMove()`, `recenterPhase()`, and `rotationFromTwoReflections()`; visual edits should usually start with `createCell()`, face texture helpers, field/projection rebuilds, or CSS media queries.
