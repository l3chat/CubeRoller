# Agent Notes

## Project Context
- Browser-only Three.js demos with no build tooling.
- Main entry files are `cube3d.html`, `cube4d.html`, and `cube4d-5.3eh.html`.
- UI language is Russian unless the user explicitly asks to change localization.

## Where To Work
- Keep each demo self-contained in its own HTML file.
- External runtime dependency is Three.js via CDN.
- Prefer editing the specific demo file requested by the user.

## Implementation Conventions
- Keep changes minimal and consistent with the selected file's architecture.
- Do not introduce build steps or package tooling unless explicitly requested.
- Preserve grid bounds checks and 90-degree step semantics for rolling behavior.
- For 4D motion updates, keep matrix math and per-vertex animation paths coherent and documented.
- Keep `PROJECT_MEMORY.md` and `AGENTS.md` updated automatically when changes affect structure, behavior, dependencies, or contributor guidance.

## Quick Test
- Open the edited HTML file in a browser.
- Verify movement controls, restart behavior, and grid-size application.
- For 4D files, verify edge-path animation is continuous and final orientation is stable after each move.
