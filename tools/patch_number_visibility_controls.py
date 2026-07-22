from pathlib import Path

path = Path('cube4d2.html')
text = path.read_text(encoding='utf-8')

pairs = [
('.actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}\n.settings{display:grid;grid-template-columns:1fr 1fr;gap:6px}', '.actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}\n.number-pad{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:4px}\n.number-pad button{min-width:0;min-height:32px;padding:0;font-size:12px;background:#334155}\n.number-pad button.active{background:var(--gold);box-shadow:0 0 0 2px rgba(255,255,255,.16) inset}\n.settings{display:grid;grid-template-columns:1fr 1fr;gap:6px}'),
('  .actions,.settings,.field-control{grid-template-columns:1fr;gap:6px}\n  button{min-height:42px;border-radius:10px;font-size:12px;padding:0 6px}', '  .actions,.settings,.field-control{grid-template-columns:1fr;gap:6px}\n  .number-pad{grid-column:1 / -1}\n  button{min-height:42px;border-radius:10px;font-size:12px;padding:0 6px}\n  .number-pad button{min-height:34px;font-size:11px}'),
('  <div class="control-section settings">\n    <label><span>Путь</span><input id="trailCheckbox" type="checkbox"></label>', '  <div class="control-section number-pad" aria-label="Показывать номера кубиков до выбранного числа">\n' + ''.join(f'    <button type="button" data-number-limit="{i}" class="{"active" if i == 7 else ""}" aria-pressed="{"true" if i == 7 else "false"}">{i}</button>\n' for i in range(8)) + '  </div>\n  <div class="control-section settings">\n    <label><span>Путь</span><input id="trailCheckbox" type="checkbox"></label>'),
('let flatView = false;\nlet fieldVisible = true;', 'let flatView = false;\n// Highest cell id whose front/back number is currently displayed.\nlet numberVisibilityLimit = 7;\nlet fieldVisible = true;'),
('function applyRenderMode(){\n  for(const id of allIds){\n    const group = cells.get(id);\n    if(group) applyCellRenderMode(group);\n  }\n}\n\nfunction setLabel(id,line){', '''function applyRenderMode(){
  for(const id of allIds){
    const group = cells.get(id);
    if(group) applyCellRenderMode(group);
  }
}

function applyNumberVisibilityToCell(group){
  const id = group.userData.id;
  const textures = group.userData.numberTextures;
  if(!textures) return;
  const showNumber = id <= numberVisibilityLimit;
  const body = group.getObjectByName("body");
  if(body && Array.isArray(body.material)){
    body.material[4].map = showNumber ? textures.front : textures.blank;
    body.material[5].map = showNumber ? textures.back : textures.blank;
    body.material[4].needsUpdate = true;
    body.material[5].needsUpdate = true;
  }
  const flatFace = group.getObjectByName("flatFace");
  if(flatFace){
    flatFace.material.map = showNumber ? textures.front : textures.blank;
    flatFace.material.needsUpdate = true;
  }
}

function setNumberVisibilityLimit(limit){
  numberVisibilityLimit = THREE.MathUtils.clamp(Math.round(limit), 0, 7);
  for(const id of allIds){
    const group = cells.get(id);
    if(group) applyNumberVisibilityToCell(group);
  }
  document.querySelectorAll("button[data-number-limit]").forEach(button=>{
    const active = Number(button.dataset.numberLimit) === numberVisibilityLimit;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

function setLabel(id,line){'''),
('  const bottomTexture = makeMarkerTexture("blank", id);\n  const rightTexture = makeMarkerTexture("topLeft", id);', '  const bottomTexture = makeMarkerTexture("blank", id);\n  g.userData.numberTextures = {front:frontNumberTexture, back:backNumberTexture, blank:bottomTexture};\n  const rightTexture = makeMarkerTexture("topLeft", id);'),
('for(const id of allIds) createCell(id);\n\n/*\n  applyStateVisual(state)', 'for(const id of allIds) createCell(id);\nsetNumberVisibilityLimit(numberVisibilityLimit);\n\n/*\n  applyStateVisual(state)'),
('      Ctrl + PageUp/Down    = zoom camera in/out\n */', '      Ctrl + PageUp/Down    = zoom camera in/out\n      0 ... 7               = show cell numbers from 0 through that value\n */'),
('document.getElementById("undoBtn").addEventListener("click", undo);', 'document.querySelectorAll("button[data-number-limit]").forEach(button=>{\n  button.addEventListener("click", ()=>setNumberVisibilityLimit(Number(button.dataset.numberLimit)));\n});\n\ndocument.getElementById("undoBtn").addEventListener("click", undo);'),
('  if(e.repeat) return;\n  if(e.key === "ArrowLeft") runMove(0,-1);', '  const targetTag = e.target?.tagName || "";\n  const typingInControl = targetTag === "INPUT" || targetTag === "TEXTAREA" || targetTag === "SELECT";\n  if(!typingInControl && !e.ctrlKey && !e.altKey && !e.metaKey && /^[0-7]$/.test(e.key)){\n    if(!e.repeat) setNumberVisibilityLimit(Number(e.key));\n    e.preventDefault();\n    return;\n  }\n\n  if(e.repeat) return;\n  if(e.key === "ArrowLeft") runMove(0,-1);')
]

for old, new in pairs:
    if new in text:
        continue
    if text.count(old) != 1:
        raise SystemExit(f'Expected one match, found {text.count(old)}: {old[:100]!r}')
    text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
print('Added number visibility controls.')

# Trigger workflow.
