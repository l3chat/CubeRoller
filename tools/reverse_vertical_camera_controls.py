from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")
old = '''    else if(e.key === "ArrowUp") orbitCameraByKeyboard(0, -cameraOrbitStep);
    else if(e.key === "ArrowDown") orbitCameraByKeyboard(0, cameraOrbitStep);'''
new = '''    else if(e.key === "ArrowUp") orbitCameraByKeyboard(0, cameraOrbitStep);
    else if(e.key === "ArrowDown") orbitCameraByKeyboard(0, -cameraOrbitStep);'''

if new in text:
    print("Vertical camera controls already reversed.")
elif text.count(old) == 1:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("Reversed Ctrl+Up and Ctrl+Down camera directions.")
else:
    raise SystemExit(f"Expected exactly one camera-control block, found {text.count(old)}")
