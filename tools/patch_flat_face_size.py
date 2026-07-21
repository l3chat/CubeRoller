from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")
old = "new THREE.PlaneGeometry(1,1)"
new = "new THREE.PlaneGeometry(0.85,0.85)"

if new in text:
    print("Flat-face size already reduced.")
elif text.count(old) == 1:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("Reduced flat-face side length by 15%.")
else:
    raise SystemExit(f"Expected exactly one flat-face geometry, found {text.count(old)}")

# Workflow trigger marker.
