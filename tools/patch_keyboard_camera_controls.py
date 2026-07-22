from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

old_comment = '''  Keyboard:
      ArrowLeft / ArrowRight = local X
      PageUp / PageDown     = local Y
      ArrowUp / ArrowDown   = local Z
*/'''
new_comment = '''  Keyboard:
      ArrowLeft / ArrowRight = local X
      PageUp / PageDown     = local Y
      ArrowUp / ArrowDown   = local Z
      Ctrl + Arrow keys     = orbit camera around controls.target
      Ctrl + PageUp/Down    = zoom camera in/out
*/'''

old_handler = '''window.addEventListener("keydown", e=>{
  if(e.repeat) return;
  if(e.key === "ArrowLeft") runMove(0,-1);
  if(e.key === "ArrowRight") runMove(0,1);
  if(e.key === "PageUp") runMove(1,1);
  if(e.key === "PageDown") runMove(1,-1);
  if(e.key === "ArrowUp") runMove(2,1);
  if(e.key === "ArrowDown") runMove(2,-1);
  if(e.key === "Backspace") undo();
});'''

new_handler = '''const cameraOrbitStep = THREE.MathUtils.degToRad(4);
const cameraZoomFactor = 0.9;

function orbitCameraByKeyboard(deltaAzimuth, deltaPolar){
  const offset = camera.position.clone().sub(controls.target);
  const spherical = new THREE.Spherical().setFromVector3(offset);

  spherical.theta += deltaAzimuth;
  spherical.phi = THREE.MathUtils.clamp(
    spherical.phi + deltaPolar,
    0.05,
    Math.PI - 0.05
  );

  camera.position.copy(controls.target).add(
    new THREE.Vector3().setFromSpherical(spherical)
  );
  camera.lookAt(controls.target);
  controls.update();
}

function zoomCameraByKeyboard(factor){
  const offset = camera.position.clone().sub(controls.target);
  const currentDistance = offset.length();
  const nextDistance = THREE.MathUtils.clamp(
    currentDistance * factor,
    controls.minDistance,
    controls.maxDistance
  );

  if(currentDistance > 0){
    offset.setLength(nextDistance);
    camera.position.copy(controls.target).add(offset);
    camera.lookAt(controls.target);
    controls.update();
  }
}

window.addEventListener("keydown", e=>{
  if(e.ctrlKey){
    let handled = true;
    if(e.key === "ArrowLeft") orbitCameraByKeyboard(cameraOrbitStep, 0);
    else if(e.key === "ArrowRight") orbitCameraByKeyboard(-cameraOrbitStep, 0);
    else if(e.key === "ArrowUp") orbitCameraByKeyboard(0, -cameraOrbitStep);
    else if(e.key === "ArrowDown") orbitCameraByKeyboard(0, cameraOrbitStep);
    else if(e.key === "PageUp") zoomCameraByKeyboard(cameraZoomFactor);
    else if(e.key === "PageDown") zoomCameraByKeyboard(1 / cameraZoomFactor);
    else handled = false;

    if(handled){
      e.preventDefault();
      return;
    }
  }

  if(e.repeat) return;
  if(e.key === "ArrowLeft") runMove(0,-1);
  if(e.key === "ArrowRight") runMove(0,1);
  if(e.key === "PageUp") runMove(1,1);
  if(e.key === "PageDown") runMove(1,-1);
  if(e.key === "ArrowUp") runMove(2,1);
  if(e.key === "ArrowDown") runMove(2,-1);
  if(e.key === "Backspace") undo();
});'''

for old, new in [(old_comment, new_comment), (old_handler, new_handler)]:
    if new in text:
        continue
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old[:100]!r}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Added keyboard camera controls.")
