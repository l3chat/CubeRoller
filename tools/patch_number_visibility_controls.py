from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        '.actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}\n.settings{display:grid;grid-template-columns:1fr 1fr;gap:6px}',
        '.actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}\n.number-pad{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:4px}\n.number-pad button{min-width:0;min-height:32px;padding:0;font-size:12px;background:#334155}\n.number-pad button.active{background:var(--gold);box-shadow:0 0 0 2px rgba(255,255,255,.16) inset}\n.settings{display:grid;grid-template-columns:1fr 1fr;gap:6px}'
    ),
    (
        '  .actions,.settings,.field-control{grid-template-columns:1fr;gap:6px}\n  button{min-height:42px;border-radius:10px;font-size:12px;padding:0 6px}',
        '  .actions,.settings,.field-control{grid-template-columns:1fr;gap:6px}\n  .number-pad{grid-column:1 / -1}\n  button{min-height:42px;border-radius:10px;font-size:12px;padding:0 6px}\n  .number-pad button{min-height:34px;font-size:11px}'
    ),
    (
        '  <div class="control-section settings">\n    <label><span>Путь</span><input id="trailCheckbox" type="checkbox"></label>',
        '  <div class="control-section number-pad" aria-label="Показывать номера кубиков до выбранного числа">\n    <button type="button" data-number-limit="0" aria-pressed="false">0</button>\n    <button type="button" data-number-limit="1" aria-pressed="false">1</button>\n    <button type="button" data-number-limit="2" aria-pressed="false">2</button>\n    <button type="button" data-number-limit="3" aria-pressed="false">3</button>\n    <button type="button" data-number-limit="4" aria-pressed="false">4</button>\n    <button type="button" data-number-limit="5" aria-pressed="false">5</button>\n    <button type="button" data-number-limit="6" aria-pressed="false">6</button>\n    <button type="button" data-number-limit="7" class="active" aria-pressed="true">7</button>\n  </div>\n  <div class="control-section settings">\n    <label><span>Путь</span><input id="trailCheckbox" type="checkbox"></label>'
    ),
    ('let flatView = false;\nlet fieldVisible = true;', 'let flatView = false;\nlet numberVisibilityLimit = 7;\nlet fieldVisible = true;'),
    (
        'function applyRenderMode(){\n  for(const id of allIds){\n    const group = cells.get(id);\n    if(group) applyCellRenderMode(group);\n  }\n}\n\nfunction setLabel(id,line){',
        'function applyRenderMode(){\n  for(const id of allIds){\n    const group = cells.get(id);\n    if(group) applyCellRenderMode(group);\n  }\n}\n\nfunction applyNumberVisibilityToCell(group){\n  const id = group.userData.id;\n  const textures = group.userData.numberTextures;\n  if(!textures) return;\n  const showNumber = id <= numberVisibilityLimit;\n  const body = group.getObjectByName("body");\n  if(body && Array.isArray(body.material)){\n    body.material[4].map = showNumber ? textures.front : textures.blank;\n    body.material[5].map = showNumber ? textures.back : textures.blank;\n    body.material[4].needsUpdate = true;\n    body.material[5].needsUpdate = true;\n  }\n  const flatFace = group.getObjectByName("flatFace");\n  if(flatFace){\n    flatFace.material.map = showNumber ? textures.front : textures.blank;\n    flatFace.material.needsUpdate = true;\n  }\n}\n\nfunction setNumberVisibilityLimit(limit){\n  numberVisibilityLimit = THREE.MathUtils.clamp(Math.round(limit), 0, 7);\n  for(const id of allIds){\n    const group = cells.get(id);\n    if(group) applyNumberVisibilityToCell(group);\n  }\n  document.querySelectorAll("button[data-number-limit]").forEach(button=>{\n    const active = Number(button.dataset.numberLimit) === numberVisibilityLimit;\n    button.classList.toggle("active", active);\n    button.setAttribute("aria-pressed", String(active));\n  });\n}\n\nfunction setLabel(id,line){'
    ),
    ('  const bottomTexture = makeMarkerTexture("blank", id);\n  const rightTexture = makeMarkerTexture("topLeft", id);', '  const bottomTexture = makeMarkerTexture("blank", id);\n  g.userData.numberTextures = {front:frontNumberTexture, back:backNumberTexture, blank:bottomTexture};\n  const rightTexture = makeMarkerTexture("topLeft", id);'),
    ('for(const id of allIds) createCell(id);\n\n/*\n  applyStateVisual(state)', 'for(const id of allIds) createCell(id);\nsetNumberVisibilityLimit(numberVisibilityLimit);\n\n/*\n  applyStateVisual(state)'),
    ('      Ctrl + PageUp/Down    = zoom camera in/out\n */', '      Ctrl + PageUp/Down    = zoom camera in/out\n      0 ... 7               = show cell numbers from 0 through that value\n */'),
    ('document.getElementById("undoBtn").addEventListener("click", undo);', 'document.querySelectorAll("button[data-number-limit]").forEach(button=>{\n  button.addEventListener("click", ()=>setNumberVisibilityLimit(Number(button.dataset.numberLimit)));\n});\n\ndocument.getElementById("undoBtn").addEventListener("click", undo);'),
    ('  if(e.repeat) return;\n  if(e.key === "ArrowLeft") runMove(0,-1);', '  const targetTag = e.target?.tagName || "";\n  const typingInControl = targetTag === "INPUT" || targetTag === "TEXTAREA" || targetTag === "SELECT";\n  if(!typingInControl && !e.ctrlKey && !e.altKey && !e.metaKey && /^[0-7]$/.test(e.key)){\n    if(!e.repeat) setNumberVisibilityLimit(Number(e.key));\n    e.preventDefault();\n    return;\n  }\n\n  if(e.repeat) return;\n  if(e.key === "ArrowLeft") runMove(0,-1);')
]

for old, new in replacements:
    if new in text:
        continue
    if text.count(old) != 1:
        raise SystemExit(f"Expected one match, found {text.count(old)}: {old[:100]!r}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Added number visibility controls.")
