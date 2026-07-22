from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    text = text.replace(old, new, 1)


replace_once(
    ".actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}",
    ".actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}\n"
    ".number-pad{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:4px}\n"
    ".number-pad button{min-width:0;min-height:32px;padding:0;font-size:12px;background:#334155}\n"
    ".number-pad button.active{background:var(--gold);box-shadow:0 0 0 2px rgba(255,255,255,.16) inset}",
    "desktop number-pad CSS",
)

replace_once(
    "  .actions,.settings,.field-control{grid-template-columns:1fr;gap:6px}",
    "  .actions,.settings,.field-control{grid-template-columns:1fr;gap:6px}\n"
    "  .number-pad{grid-column:1 / -1}\n"
    "  .number-pad button{min-height:34px;font-size:11px}",
    "portrait number-pad CSS",
)

buttons = '''    <button type="button" data-number-limit="0" aria-pressed="false">0</button>
    <button type="button" data-number-limit="1" aria-pressed="false">1</button>
    <button type="button" data-number-limit="2" aria-pressed="false">2</button>
    <button type="button" data-number-limit="3" aria-pressed="false">3</button>
    <button type="button" data-number-limit="4" aria-pressed="false">4</button>
    <button type="button" data-number-limit="5" aria-pressed="false">5</button>
    <button type="button" data-number-limit="6" aria-pressed="false">6</button>
    <button type="button" data-number-limit="7" class="active" aria-pressed="true">7</button>'''
replace_once(
    '  <div class="control-section settings">',
    '  <div class="control-section number-pad" aria-label="Показывать номера кубиков до выбранного числа">\n'
    + buttons
    + '\n  </div>\n  <div class="control-section settings">',
    "number-pad HTML",
)

replace_once(
    "let flatView = false;",
    "let flatView = false;\nlet numberVisibilityLimit = 7;",
    "number visibility state",
)

visibility_functions = '''function applyNumberVisibilityToCell(group){
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

'''
replace_once(
    "function setLabel(id,line){",
    visibility_functions + "function setLabel(id,line){",
    "visibility functions",
)

replace_once(
    '  const bottomTexture = makeMarkerTexture("blank", id);',
    '  const bottomTexture = makeMarkerTexture("blank", id);\n'
    '  g.userData.numberTextures = {front:frontNumberTexture, back:backNumberTexture, blank:bottomTexture};',
    "texture references",
)

replace_once(
    "for(const id of allIds) createCell(id);",
    "for(const id of allIds) createCell(id);\nsetNumberVisibilityLimit(numberVisibilityLimit);",
    "initial visibility",
)

replace_once(
    "      Ctrl + PageUp/Down    = zoom camera in/out",
    "      Ctrl + PageUp/Down    = zoom camera in/out\n"
    "      0 ... 7               = show cell numbers from 0 through that value",
    "keyboard documentation",
)

replace_once(
    'document.getElementById("undoBtn").addEventListener("click", undo);',
    'document.querySelectorAll("button[data-number-limit]").forEach(button=>{\n'
    '  button.addEventListener("click", ()=>setNumberVisibilityLimit(Number(button.dataset.numberLimit)));\n'
    '});\n\n'
    'document.getElementById("undoBtn").addEventListener("click", undo);',
    "button handlers",
)

replace_once(
    "  if(e.repeat) return;",
    '  const targetTag = e.target?.tagName || "";\n'
    '  const typingInControl = targetTag === "INPUT" || targetTag === "TEXTAREA" || targetTag === "SELECT";\n'
    '  if(!typingInControl && !e.ctrlKey && !e.altKey && !e.metaKey && /^[0-7]$/.test(e.key)){\n'
    '    if(!e.repeat) setNumberVisibilityLimit(Number(e.key));\n'
    '    e.preventDefault();\n'
    '    return;\n'
    '  }\n\n'
    '  if(e.repeat) return;',
    "number key handler",
)

path.write_text(text, encoding="utf-8")
print("Added number visibility controls.")
