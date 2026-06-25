# Agent Notes

## Project Context
- Browser-only Three.js demos with no build tooling.
- Main entry files are `cube3d.html`, `cube4d.html`, `cube4d2.html`, and `cube4d-5.3eh.html`.
- `cube4d2.html` is the annotated universal mobile tesseract roller prototype. Its top architecture comment is part of the working spec and should be read before edits.
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
- For `cube4d2.html`, preserve the universal movement model `A -> B`, cell numbering `0..7`, opposite pairs `0<->7`, `1<->6`, `2<->5`, `3<->4`, persistent `state.orientations`, and `state.pendingNormals` handling.
- Do not reset cube quaternions after a `cube4d2.html` move, and do not introduce negative scale unless explicitly requested and documented.
- In `cube4d2.html`, be especially careful with `makeNextState()`, `runMove()`, `recenterPhase()`, and `rotationFromTwoReflections()` when changing movement or orientation logic.
- Keep `PROJECT_MEMORY.md` and `AGENTS.md` updated automatically when changes affect structure, behavior, dependencies, or contributor guidance.

## Quick Test
- Open the edited HTML file in a browser.
- Verify movement controls, restart behavior, and grid-size application.
- For 4D files, verify edge-path animation is continuous and final orientation is stable after each move.
- For `cube4d2.html`, also verify entering/exiting external cells, undo, field-size application, wall projections, and that face markers remain coherent across repeated moves.
