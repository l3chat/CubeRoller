// Patch for cube4d2.html: keep the external cube visible and animate it
// as part of the 4D net. Load this file after the main cube4d2.html script.
(function(){
  "use strict";

  if (typeof THREE === "undefined" || typeof state === "undefined" || typeof cells === "undefined") {
    console.warn("cube4d2_patch.js: cube4d2 globals are not ready; patch skipped.");
    return;
  }

  function externalDirectionFor(id, s){
    const pending = s && s.pendingNormals ? s.pendingNormals[id] : null;
    if(pending){
      const v = objToVec(pending);
      if(v.lengthSq() > 1e-9) return v.normalize();
    }

    if(s && s.fieldPath && s.fieldPath.length >= 2){
      const last = objToVec(s.fieldPath[s.fieldPath.length - 1]);
      const prev = objToVec(s.fieldPath[s.fieldPath.length - 2]);
      const d = last.sub(prev);
      if(d.lengthSq() > 1e-9) return d.normalize();
    }

    return new THREE.Vector3(1,0,0);
  }

  function externalPositionFor(id, s){
    return fieldVec(s).add(externalDirectionFor(id, s).multiplyScalar(2 * spacing));
  }

  currentPositionFor = function(id, s){
    const base = fieldVec(s);

    if(id === s.active) return base;
    if(id === externalCell(s)) return externalPositionFor(id, s);

    for(let i=0;i<3;i++){
      if(s.axes[i].plus === id) return base.clone().add(dirVectors[i].clone().multiplyScalar(spacing));
      if(s.axes[i].minus === id) return base.clone().add(dirVectors[i].clone().multiplyScalar(-spacing));
    }

    return externalPositionFor(id, s);
  };

  applyStateVisual = function(s){
    clearGroup(edgeGroup);

    for(const id of allIds){
      const g = cells.get(id);
      const isActive = id === s.active;
      const isExternal = id === externalCell(s);

      g.position.copy(currentPositionFor(id,s));
      g.quaternion.copy(objToQuat(s.orientations?.[id] || {x:0,y:0,z:0,w:1}));
      g.visible = true;
      setCubeOpacity(g, 1.0);

      const ed = g.getObjectByName("edges");
      g.userData.baseEdgeOpacity = isActive ? 1.00 : isExternal ? 0.50 : 0.65;
      g.userData.baseEdgeColor = isActive ? 0xffffff : isExternal ? 0x7aa9d8 : 0xaebdca;
      ed.material.color.set(g.userData.baseEdgeColor);
      ed.material.opacity = g.userData.baseEdgeOpacity;

      const labelSprite = g.getObjectByName("label");
      labelSprite.visible = false;
      labelSprite.material.opacity = 0.0;

      if(isActive) setLabel(id, "активный");
      else if(isExternal) setLabel(id, "внешний");
      else setLabel(id, "сосед " + s.active);
    }

    rebuildTrail();
    rebuildProjections();
    applyLocalFog();
    updateButtons();
    updateInfo();
  };

  runMove = function(axisIndex, sign){
    if(busy) return;

    const nextField = objToVec(state.field).add(dirVectors[axisIndex].clone().multiplyScalar(sign));
    if(!inBounds(nextField)){
      updateInfo({blocked:true, axisIndex, sign, nextField});
      return;
    }

    const A = state.active;
    const B = sign > 0 ? state.axes[axisIndex].plus : state.axes[axisIndex].minus;
    const enter = opposite[A];
    const out = opposite[B];
    const next = makeNextState(state, axisIndex, sign);
    const bDir = dirVectors[axisIndex].clone().multiplyScalar(sign);
    const spinners = commonSpinners(state, axisIndex);
    const base = fieldVec(state);

    history.push(cloneState(state));
    busy = true;
    clearGroup(edgeGroup);

    setLabel(A, "старый активный");
    setLabel(B, "новый активный");
    cells.get(A).userData.baseEdgeOpacity = 1.00;
    cells.get(A).userData.baseEdgeColor = 0xffffff;
    cells.get(B).userData.baseEdgeOpacity = 0.65;
    cells.get(B).userData.baseEdgeColor = 0xaebdca;

    const enterGroup = cells.get(enter);
    const enterEdges = enterGroup.getObjectByName("edges");
    const enterLabel = enterGroup.getObjectByName("label");
    const enterStartPosition = currentPositionFor(enter, state);
    const enterTargetPosition = currentPositionFor(enter, next);

    enterGroup.visible = true;
    enterGroup.position.copy(enterStartPosition);
    enterGroup.quaternion.copy(objToQuat(state.orientations?.[enter] || {x:0,y:0,z:0,w:1}));
    const enterRotation = rotationFromTwoReflections(state.pendingNormals?.[enter], bDir);
    enterGroup.quaternion.premultiply(enterRotation);
    next.pendingNormals[enter] = null;
    enterEdges.material.opacity = 0.75;
    setCubeOpacity(enterGroup, 1.0);
    enterLabel.visible = false;
    enterLabel.material.opacity = 0.0;
    setLabel(enter, "входит");

    const outGroup = cells.get(out);
    const outEdges = outGroup.getObjectByName("edges");
    const outLabel = outGroup.getObjectByName("label");
    const outStartPosition = currentPositionFor(out, state);
    const outTargetPosition = currentPositionFor(out, next);

    outGroup.visible = true;
    outLabel.visible = false;
    outLabel.material.opacity = 0.0;
    setLabel(out, "выходит");

    const per = {};
    for(const S of spinners){
      const sDir = localDirFor(S, state);
      const pivot = base.clone().add(bDir.clone().add(sDir).multiplyScalar(h));
      const start = base.clone().add(sDir.clone().multiplyScalar(spacing));
      const target = base.clone().add(bDir.clone().add(sDir).multiplyScalar(spacing));
      const v0 = start.clone().sub(pivot);
      const v1 = target.clone().sub(pivot);
      const axis = new THREE.Vector3().crossVectors(v0, v1).normalize();
      const angle = v0.angleTo(v1);
      const edgeName = `${A}${S}${B}`;

      per[S] = {pivot, axis, angle, done:0, edgeName};
      addAxisLine(edgeName, pivot, axis);
      setLabel(S, edgeName);
      setCubeOpacity(cells.get(S), 1.0);
    }

    updateInfo({A, B, enter, out, spinners, axisIndex, sign});
    updateButtons();

    function rotatePhase(){
      let finished = true;

      for(const S of spinners){
        const p = per[S];
        const rest = p.angle - p.done;
        if(rest > 1e-5){
          const da = Math.min(rollStep, rest);
          rotateAround(cells.get(S), p.pivot, p.axis, da);
          p.done += da;
          finished = false;
        }
      }

      const sample = per[spinners[0]];
      const fade = sample ? Math.min(1, sample.done / sample.angle) : 1;

      enterGroup.position.lerpVectors(enterStartPosition, enterTargetPosition, fade);
      outGroup.position.lerpVectors(outStartPosition, outTargetPosition, fade);

      enterEdges.material.opacity = 0.75;
      setCubeOpacity(enterGroup, 1.0);
      enterLabel.material.opacity = 0.0;

      outEdges.material.opacity = 0.50;
      setCubeOpacity(outGroup, 1.0);
      outLabel.material.opacity = 0.0;

      const oldColor = new THREE.Color(0xffffff);
      const idleColor = new THREE.Color(0xaebdca);
      const aColor = oldColor.clone().lerp(idleColor, fade);
      const bColor = idleColor.clone().lerp(oldColor, fade);
      cells.get(A).userData.baseEdgeOpacity = 1.00 - 0.35 * fade;
      cells.get(B).userData.baseEdgeOpacity = 0.65 + 0.35 * fade;
      cells.get(A).userData.baseEdgeColor = aColor.getHex();
      cells.get(B).userData.baseEdgeColor = bColor.getHex();

      applyLocalFog();

      if(!finished){
        requestAnimationFrame(rotatePhase);
        return;
      }

      next.pendingNormals[out] = vecToObj(bDir.clone());
      recenterPhase(next, {A, B, enter, out, spinners});
    }

    rotatePhase();
  };

  if(state) applyStateVisual(state);
})();
