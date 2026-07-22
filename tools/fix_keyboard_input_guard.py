from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

old = '''window.addEventListener("keydown", e=>{
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

  const targetTag = e.target?.tagName || "";
  const typingInControl = targetTag === "INPUT" || targetTag === "TEXTAREA" || targetTag === "SELECT";
  if(!typingInControl && !e.ctrlKey && !e.altKey && !e.metaKey && /^[0-7]$/.test(e.key)){
    if(!e.repeat) setNumberVisibilityLimit(Number(e.key));
    e.preventDefault();
    return;
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

new = '''function isKeyboardInputTarget(target){
  if(!(target instanceof Element)) return false;
  return Boolean(target.closest('input, textarea, select, button, [contenteditable="true"]'));
}

function numberLimitFromKeyboardEvent(e){
  const match = /^(?:Digit|Numpad)([0-7])$/.exec(e.code);
  return match ? Number(match[1]) : null;
}

window.addEventListener("keydown", e=>{
  // Controls keep their native keyboard behaviour. In particular, arrow keys,
  // PageUp/PageDown and Backspace must not also move the tesseract while the
  // field-size input or another UI control has focus.
  if(isKeyboardInputTarget(e.target)) return;

  if(e.ctrlKey && !e.altKey && !e.metaKey){
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

  if(!e.ctrlKey && !e.altKey && !e.metaKey){
    const numberLimit = numberLimitFromKeyboardEvent(e);
    if(numberLimit !== null){
      if(!e.repeat) setNumberVisibilityLimit(numberLimit);
      e.preventDefault();
      return;
    }
  }

  if(e.ctrlKey || e.altKey || e.metaKey || e.repeat) return;

  let handled = true;
  if(e.key === "ArrowLeft") runMove(0,-1);
  else if(e.key === "ArrowRight") runMove(0,1);
  else if(e.key === "PageUp") runMove(1,1);
  else if(e.key === "PageDown") runMove(1,-1);
  else if(e.key === "ArrowUp") runMove(2,1);
  else if(e.key === "ArrowDown") runMove(2,-1);
  else if(e.key === "Backspace") undo();
  else handled = false;

  if(handled) e.preventDefault();
});'''

if new in text:
    print("Keyboard input guard already fixed.")
elif text.count(old) == 1:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("Fixed keyboard input guard.")
else:
    raise SystemExit(f"Expected exactly one old keydown handler, found {text.count(old)}")
