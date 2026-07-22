from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

old = '''function initialState(){
  return {
    active: 0,'''
new = '''function initialState(){
  const orientations = identityOrientations();
  // Cell 7 starts external. Its stable physical orientation is the one reached
  // after the first closed U-D-F-B cycle: 180 degrees around local/world X.
  orientations[7] = {x:1,y:0,z:0,w:0};

  const pendingNormals = identityPendingNormals();
  // The initial external placement is behind the forward neighbor. Treat it as
  // having left through the corresponding +world-Z face, so its first return
  // follows the same two-reflection rule as every later return.
  pendingNormals[7] = {x:0,y:0,z:1};

  return {
    active: 0,'''

if new not in text:
    if text.count(old) != 1:
        raise SystemExit(f"Expected one initialState anchor, found {text.count(old)}")
    text = text.replace(old, new, 1)

text = text.replace(
    '    orientations: identityOrientations(),\n    pendingNormals: identityPendingNormals(),',
    '    orientations,\n    pendingNormals,',
    1
)

path.write_text(text, encoding="utf-8")
print("Initialized cell 7 with its stable external orientation and pending normal.")
# Capture browser snapshots for the candidate initial state.
