# CubeRoller

A small collection of browser-only Three.js demos for rolling geometry with orientation tracking.

## Run
- Open `cube3d.html` in a modern browser.
- Open `cube4d.html` for the 4D tesseract version.
- Open `cube4d-5.3eh.html` for the new-from-scratch 4D implementation.

## Controls
- Buttons: Вверх / Вниз / Влево / Вправо
- Arrow keys: Up / Down / Left / Right
- Restart: resets cube position and orientation
- Grid size: set 1–20 and click "Применить"

## Structure
- `cube3d.html`: HTML, CSS, and JavaScript (Three.js via CDN)
- `cube4d.html`: 4D tesseract rolling demo (Three.js via CDN)
- `cube4d-5.3eh.html`: fresh 4D tesseract demo with per-vertex path animation around a 4D pivot edge, switchable projection modes, 4D view-angle controls, and projection-eye tracking to the tesseract center (Three.js via CDN)
