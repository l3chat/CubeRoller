from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

old_camera = '''const cameraOrbitStep = THREE.MathUtils.degToRad(4);
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
}'''

new_camera = '''const cameraOrbitStep = THREE.MathUtils.degToRad(4);
const cameraZoomFactor = 0.9;
const keyboardCameraSmoothing = 14;
const keyboardCameraSnapEpsilon = 1e-4;
let keyboardCameraTarget = null;
let keyboardCameraAnimating = false;
let keyboardCameraLastFrame = performance.now();

function cameraSphericalFromPosition(){
  return new THREE.Spherical().setFromVector3(
    camera.position.clone().sub(controls.target)
  );
}

function ensureKeyboardCameraTarget(){
  if(!keyboardCameraTarget || !keyboardCameraAnimating){
    keyboardCameraTarget = cameraSphericalFromPosition();
  }
  return keyboardCameraTarget;
}

function orbitCameraByKeyboard(deltaAzimuth, deltaPolar){
  const target = ensureKeyboardCameraTarget();
  target.theta += deltaAzimuth;
  target.phi = THREE.MathUtils.clamp(
    target.phi + deltaPolar,
    0.05,
    Math.PI - 0.05
  );
  keyboardCameraAnimating = true;
}

function zoomCameraByKeyboard(factor){
  const target = ensureKeyboardCameraTarget();
  target.radius = THREE.MathUtils.clamp(
    target.radius * factor,
    controls.minDistance,
    controls.maxDistance
  );
  keyboardCameraAnimating = true;
}

function shortestAngleDelta(from, to){
  return THREE.MathUtils.euclideanModulo(to - from + Math.PI, Math.PI * 2) - Math.PI;
}

function cancelKeyboardCameraAnimation(){
  keyboardCameraAnimating = false;
  keyboardCameraTarget = null;
}

function updateKeyboardCameraAnimation(now){
  const dt = THREE.MathUtils.clamp((now - keyboardCameraLastFrame) / 1000, 0, 0.05);
  keyboardCameraLastFrame = now;
  if(!keyboardCameraAnimating || !keyboardCameraTarget) return;

  const current = cameraSphericalFromPosition();
  const thetaDelta = shortestAngleDelta(current.theta, keyboardCameraTarget.theta);
  const phiDelta = keyboardCameraTarget.phi - current.phi;
  const radiusDelta = keyboardCameraTarget.radius - current.radius;
  const alpha = 1 - Math.exp(-keyboardCameraSmoothing * dt);

  current.theta += thetaDelta * alpha;
  current.phi += phiDelta * alpha;
  current.radius += radiusDelta * alpha;

  const finished = Math.abs(thetaDelta) < keyboardCameraSnapEpsilon &&
    Math.abs(phiDelta) < keyboardCameraSnapEpsilon &&
    Math.abs(radiusDelta) < keyboardCameraSnapEpsilon;

  if(finished){
    current.copy(keyboardCameraTarget);
    cancelKeyboardCameraAnimation();
  }

  camera.position.copy(controls.target).add(
    new THREE.Vector3().setFromSpherical(current)
  );
  camera.lookAt(controls.target);
}

// A mouse or touch gesture takes priority and immediately cancels a pending
// keyboard transition, so the camera never pulls back toward an old target.
controls.addEventListener("start", cancelKeyboardCameraAnimation);'''

old_loop = '''function loop(){
  requestAnimationFrame(loop);
  controls.update();'''

new_loop = '''function loop(now=performance.now()){
  requestAnimationFrame(loop);
  updateKeyboardCameraAnimation(now);
  controls.update();'''

for old, new in [(old_camera, new_camera), (old_loop, new_loop)]:
    if new in text:
        continue
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old[:120]!r}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Added smooth keyboard camera transitions.")
