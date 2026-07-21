from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old[:100]!r}")
    text = text.replace(old, new, 1)


replace_once(
    '    <label><span>Путь</span><input id="trailCheckbox" type="checkbox"></label>',
    '    <label><span>Путь</span><input id="trailCheckbox" type="checkbox"></label>\n'
    '    <label><span>Плоский вид</span><input id="flatViewCheckbox" type="checkbox"></label>',
)

replace_once(
    'let trailVisible = false;',
    'let trailVisible = false;\n'
    '// Alternative representation: hide cube bodies and edges, leaving only a numbered square at each cell center.\n'
    'let flatView = false;',
)

replace_once(
    '''function setCubeOpacity(group, opacity){
  opacity = Number.isFinite(opacity) ? Math.max(0, Math.min(1, opacity)) : 1;
  const body = group.getObjectByName("body");
  if(!body) return;
  const mats = Array.isArray(body.material) ? body.material : [body.material];
  for(const m of mats){
    m.transparent = opacity < 0.999;
    m.opacity = opacity;
  }
}''',
    '''function setCubeOpacity(group, opacity){
  opacity = Number.isFinite(opacity) ? Math.max(0, Math.min(1, opacity)) : 1;
  const body = group.getObjectByName("body");
  if(body){
    const mats = Array.isArray(body.material) ? body.material : [body.material];
    for(const m of mats){
      m.transparent = opacity < 0.999;
      m.opacity = opacity;
    }
  }

  const flatFace = group.getObjectByName("flatFace");
  if(flatFace){
    flatFace.material.transparent = opacity < 0.999;
    flatFace.material.opacity = opacity;
  }
}

function applyCellRenderMode(group){
  const body = group.getObjectByName("body");
  const edges = group.getObjectByName("edges");
  const flatFace = group.getObjectByName("flatFace");

  if(body) body.visible = !flatView;
  if(edges) edges.visible = !flatView;
  if(flatFace) flatFace.visible = flatView;
}

function applyRenderMode(){
  for(const id of allIds){
    const group = cells.get(id);
    if(group) applyCellRenderMode(group);
  }
}''',
)

replace_once(
    '''  const cube = new THREE.Mesh(new THREE.BoxGeometry(1,1,1), bodyMat);
  cube.name = "body";
  g.add(cube);''',
    '''  const cube = new THREE.Mesh(new THREE.BoxGeometry(1,1,1), bodyMat);
  cube.name = "body";
  g.add(cube);

  // Alternative flat representation. The plane is centered in the cell group and
  // shares the cube quaternion, so it preserves the orientation of the original +Z face.
  const flatFace = new THREE.Mesh(
    new THREE.PlaneGeometry(1,1),
    new THREE.MeshBasicMaterial({
      map: frontNumberTexture,
      side: THREE.DoubleSide,
      transparent: false,
      opacity: 1.0,
      depthWrite: true
    })
  );
  flatFace.name = "flatFace";
  flatFace.visible = false;
  g.add(flatFace);''',
)

replace_once(
    '    setCubeOpacity(g, isExternal ? externalBodyOpacity : 1.0);',
    '    setCubeOpacity(g, isExternal ? externalBodyOpacity : 1.0);\n'
    '    applyCellRenderMode(g);',
)

replace_once(
    '''document.getElementById("trailCheckbox").addEventListener("change", e=>{
  trailVisible = e.target.checked;
  rebuildTrail();
});''',
    '''document.getElementById("trailCheckbox").addEventListener("change", e=>{
  trailVisible = e.target.checked;
  rebuildTrail();
});

document.getElementById("flatViewCheckbox").addEventListener("change", e=>{
  flatView = e.target.checked;
  applyRenderMode();
});''',
)

path.write_text(text, encoding="utf-8")
print("Patched cube4d2.html with flat-face view")
