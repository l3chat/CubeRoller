# Agent Notes

## Project Context
- Single-file Three.js demo in `cube3d.html`.
- No build tooling; open the HTML file directly in a browser.
- UI text is in Russian; keep localization consistent unless asked to change.

## Where To Work
- All logic, styling, and markup are in `cube3d.html`.
- External dependency is Three.js via CDN.

## Implementation Conventions
- Keep changes minimal and inline with the existing structure.
- Avoid introducing a build system or extra files unless explicitly requested.
- Preserve grid bounds logic and 90° step animation behavior.
- Keep `PROJECT_MEMORY.md` and `AGENTS.md` updated automatically when changes affect structure, behavior, dependencies, or contributor guidance.

## Quick Test
- Open `cube3d.html` in a browser and use arrow keys and buttons.
- Verify grid size updates recenters the camera and restarts the cube.
