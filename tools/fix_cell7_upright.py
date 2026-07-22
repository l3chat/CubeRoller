from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

old = "orientations[7] = {x:1,y:0,z:0,w:0};"
new = "orientations[7] = {x:0,y:0,z:0,w:1};"

if new not in text:
    if text.count(old) != 1:
        raise SystemExit(f"Expected exactly one cell 7 orientation, found {text.count(old)}")
    text = text.replace(old, new, 1)

text = text.replace(
    "after the first closed U-D-F-B cycle: 180 degrees around local/world X.",
    "matching all other cells: front face toward the camera and local up pointing upward.",
    1,
)

path.write_text(text, encoding="utf-8")
print("Restored cell 7 to the common initial facing while preserving its external-state normal.")
