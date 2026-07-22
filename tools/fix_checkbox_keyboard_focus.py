from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        '''document.getElementById("trailCheckbox").addEventListener("change", e=>{
  trailVisible = e.target.checked;
  rebuildTrail();
});''',
        '''document.getElementById("trailCheckbox").addEventListener("change", e=>{
  trailVisible = e.target.checked;
  rebuildTrail();
  e.target.blur();
});'''
    ),
    (
        '''document.getElementById("flatViewCheckbox").addEventListener("change", e=>{
  flatView = e.target.checked;
  applyRenderMode();
});''',
        '''document.getElementById("flatViewCheckbox").addEventListener("change", e=>{
  flatView = e.target.checked;
  applyRenderMode();
  e.target.blur();
});'''
    ),
    (
        '''function isKeyboardInputTarget(target){
  if(!(target instanceof Element)) return false;
  return Boolean(target.closest('input, textarea, select, [contenteditable="true"]'));
}''',
        '''function isKeyboardInputTarget(target){
  if(!(target instanceof Element)) return false;
  if(target.closest('textarea, select, [contenteditable="true"]')) return true;

  const input = target.closest('input');
  if(!input) return false;

  const nonEditingTypes = new Set(["checkbox", "radio", "button", "submit", "reset"]);
  return !nonEditingTypes.has((input.type || "text").toLowerCase());
}'''
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
print("Fixed checkbox focus and keyboard guard.")
