from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        'body.ui-hidden #panel{display:none}',
        'body.ui-hidden #panel{visibility:hidden;opacity:0;pointer-events:none;overflow:hidden;padding:0;border:0;box-shadow:none;backdrop-filter:none}'
    ),
    (
        '''document.getElementById("uiToggle").addEventListener("click", ()=>{
  document.body.classList.toggle("ui-hidden");
  requestAnimationFrame(layoutScene);
});''',
        '''document.getElementById("uiToggle").addEventListener("click", e=>{
  document.body.classList.toggle("ui-hidden");
  e.currentTarget.blur();

  // Preserve the user's camera position. Only resize the renderer after the CSS
  // grid has completed both the hide and show layout passes.
  requestAnimationFrame(()=>{
    requestAnimationFrame(()=>{
      resizeRendererToFrame();
      controls.update();
    });
  });
});'''
    ),
    (
        '''  const orientations = identityOrientations();
  // Cell 7 starts external. Its stable physical orientation is the one reached
  // after the first closed U-D-F-B cycle: 180 degrees around local/world X.
  orientations[7] = {x:1,y:0,z:0,w:0};

  const pendingNormals = identityPendingNormals();''',
        '''  // Cell 7 initially faces the same way as every other cube. Only its
  // external-transition metadata differs from the ordinary visible cells.
  const orientations = identityOrientations();

  const pendingNormals = identityPendingNormals();'''
    ),
]

for old, new in replacements:
    if new in text:
        continue
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old[:120]!r}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Applied cell 7 identity orientation and stable UI toggle rendering fixes.")
