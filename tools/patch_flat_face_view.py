from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        '    <label><span>Путь</span><input id="trailCheckbox" type="checkbox"></label>\n    <label><span>Размер</span><input id="fieldSizeInput" type="number" min="3" max="9" step="2" value="7"></label>',
        '    <label><span>Путь</span><input id="trailCheckbox" type="checkbox"></label>\n    <label><span>Плоский вид</span><input id="flatViewCheckbox" type="checkbox"></label>\n    <label><span>Размер</span><input id="fieldSizeInput" type="number" min="3" max="9" step="2" value="7"></label>'
    ),
    (
        'let trailVisible = false;\nlet fieldVisible = true;',
        'let trailVisible = false;\n// Alternative representation: hide cube bodies and edges, leaving only a numbered square at each cell center.\nlet flatView = false;\nlet fieldVisible = true;'
    ),
    (
        'function setCubeOpacity(group, opacity){\n  opacity = Number.isFinite(opacity) ? Math.max(0, Math.min(1, opacity)) : 1;\n  const body = group.getObjectByName("body");\n  if(!body) return;\n  const mats = Array.isArray(body.material) ? body.material : [body.material];\n  for(const m of mats){\n    m.transparent = opacity < 0.999;\n    m.opacity = opacity;\n  }\n}',
        'function setCubeOpacity(group, opacity){\n  opacity = Number.isFinite(opacity) ? Math.max(0, Math.min(1, opacity)) : 1;\n  const body = group.getObjectByName("body");\n  if(body){\n    const mats = Array.isArray(body.material) ? body.material : [body.material];\n    for(const m of mats){\n      m.transparent = opacity < 0.999;\n      m.opacity = opacity;\n    }\n  }\n\n  const flatFace = group.getObjectByName("flatFace");\n  if(flatFace){\n    flatFace.material.transparent = opacity < 0.999;\n    flatFace.material.opacity = opacity;\n  }\n}\n\nfunction applyCellRenderMode(group){\n  const body = group.getObjectByName("body");\n  const edges = group.getObjectByName("edges");\n  const flatFace = group.getObjectByName("flatFace");\n\n  if(body) body.visible = !flatView;\n  if(edges) edges.visible = !flatView;\n  if(flatFace) flatFace.visible = flatView;\n}\n\nfunction applyRenderMode(){\n  for(const id of allIds){\n    const group = cells.get(id);\n    if(group) applyCellRenderMode(group);\n  }\n}'
    ),
    (
        '  const cube = new THREE.Mesh(new THREE.BoxGeometry(1,1,1), bodyMat);\n  cube.name = "body";\n  g.add(cube);',
        '  const cube = new THREE.Mesh(new THREE.BoxGeometry(1,1,1), bodyMat);\n  cube.name = "body";\n  g.add(cube);\n\n  // Alternative flat representation. The plane is centered in the cell group and\n  // shares the cube quaternion, so it preserves the orientation of the original +Z face.\n  const flatFace = new THREE.Mesh(\n    new THREE.PlaneGeometry(1,1),\n    new THREE.MeshBasicMaterial({\n      map: frontNumberTexture,\n      side: THREE.DoubleSide,\n      transparent: false,\n      opacity: 1.0,\n      depthWrite: true\n    })\n  );\n  flatFace.name = "flatFace";\n  flatFace.visible = false;\n  g.add(flatFace);'
    ),
    (
        '    setCubeOpacity(g, isExternal ? externalBodyOpacity : 1.0);\n    g.userData.baseEdgeOpacity',
        '    setCubeOpacity(g, isExternal ? externalBodyOpacity : 1.0);\n    applyCellRenderMode(g);\n    g.userData.baseEdgeOpacity'
    ),
    (
        'document.getElementById("trailCheckbox").addEventListener("change", e=>{\n  trailVisible = e.target.checked;\n  rebuildTrail();\n});',
        'document.getElementById("trailCheckbox").addEventListener("change", e=>{\n  trailVisible = e.target.checked;\n  rebuildTrail();\n});\n\ndocument.getElementById("flatViewCheckbox").addEventListener("change", e=>{\n  flatView = e.target.checked;\n  applyRenderMode();\n});'
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old[:90]!r}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Patched cube4d2.html with flat-face view")
