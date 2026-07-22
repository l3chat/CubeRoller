from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

old = "orientations[7] = {x:1,y:0,z:0,w:0};"
new = "orientations[7] = {x:0,y:1,z:0,w:0};"

if new not in text:
    if text.count(old) != 1:
        raise SystemExit(f"Expected exactly one cell 7 orientation, found {text.count(old)}")
    text = text.replace(old, new, 1)

text = text.replace(
    "after the first closed U-D-F-B cycle: 180 degrees around local/world X.",
    "after the first closed U-D-F-B cycle, corrected upright: 180 degrees around world Y.",
    1,
)

path.write_text(text, encoding="utf-8")
print("Turned initial cell 7 upright while preserving its stable external state.")
