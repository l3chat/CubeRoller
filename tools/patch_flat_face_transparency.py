from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        "const externalBodyOpacity = 0.71;\nconst externalEdgeOpacity = 0.69;",
        "const externalBodyOpacity = 0.71;\nconst externalEdgeOpacity = 0.69;\nconst flatFaceOpacity = 0.65;"
    ),
    (
        "  const flatFace = group.getObjectByName(\"flatFace\");\n  if(flatFace){\n    flatFace.material.transparent = opacity < 0.999;\n    flatFace.material.opacity = opacity;\n  }",
        "  const flatFace = group.getObjectByName(\"flatFace\");\n  if(flatFace){\n    flatFace.material.transparent = true;\n    flatFace.material.opacity = opacity * flatFaceOpacity;\n    flatFace.material.depthWrite = false;\n  }"
    ),
    (
        "      side: THREE.DoubleSide,\n      transparent: false,\n      opacity: 1.0,\n      depthWrite: true",
        "      side: THREE.DoubleSide,\n      transparent: true,\n      opacity: flatFaceOpacity,\n      depthWrite: false"
    ),
]

changed = False
for old, new in replacements:
    if new in text:
        continue
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old[:100]!r}")
    text = text.replace(old, new, 1)
    changed = True

if changed:
    path.write_text(text, encoding="utf-8")
    print("Applied flat-face transparency patch.")
else:
    print("Flat-face transparency patch already applied.")

# Touch this helper to trigger the registered branch workflow.
