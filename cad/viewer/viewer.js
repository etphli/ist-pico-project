/* Pip section viewer. Three.js r180 is vendored under the MIT licence. */
(() => {
  "use strict";
  const model = JSON.parse(document.getElementById("model-data").textContent);
  const $ = (id) => document.getElementById(id);
  const stage = $("stage");
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      antialias: true,
      stencil: true,
      preserveDrawingBuffer: true,
    });
  } catch (error) {
    const message = document.createElement("div");
    message.className = "error";
    message.textContent =
      "The 3D view needs WebGL 2. Enable hardware acceleration or open this HTML file in a current desktop browser. " +
      error.message;
    stage.append(message);
    $("status").textContent = "3D renderer unavailable";
    return;
  }
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setClearColor(0xe6eff6, 0);
  renderer.localClippingEnabled = true;
  stage.prepend(renderer.domElement);
  const canvas = renderer.domElement;
  canvas.tabIndex = 0;
  canvas.setAttribute(
    "aria-label",
    "Robot 3D model. Drag to orbit, shift drag to pan, scroll to zoom. Arrow keys orbit.",
  );
  const scene = new THREE.Scene();
  scene.add(new THREE.HemisphereLight(0xeaf6ff, 0x66747f, 2.3));
  const light = new THREE.DirectionalLight(0xffffff, 3.0);
  light.position.set(200, 150, 420);
  scene.add(light);
  const fill = new THREE.DirectionalLight(0xb7d6f4, 1.2);
  fill.position.set(-180, -140, 150);
  scene.add(fill);
  const camera = new THREE.PerspectiveCamera(33, 1, 0.1, 10000);
  camera.up.set(0, 0, 1);
  const center = new THREE.Vector3()
    .fromArray(model.bounds[0])
    .add(new THREE.Vector3().fromArray(model.bounds[1]))
    .multiplyScalar(0.5);
  const target = center.clone();
  let azimuth = 0.65,
    elevation = 0.24,
    distance = 650,
    selected = null;
  let pending = false;
  function requestRender() {
    if (!pending) {
      pending = true;
      requestAnimationFrame(() => {
        pending = false;
        draw();
      });
    }
  }
  function draw() {
    camera.position
      .set(
        Math.cos(elevation) * Math.cos(azimuth),
        Math.cos(elevation) * Math.sin(azimuth),
        Math.sin(elevation),
      )
      .multiplyScalar(distance)
      .add(target);
    camera.lookAt(target);
    renderer.render(scene, camera);
  }
  const reference = new THREE.Group();
  const grid = new THREE.GridHelper(300, 12, 0x9bb4c5, 0xc4d5e0);
  grid.rotation.x = Math.PI / 2;
  grid.position.z = -0.3;
  reference.add(grid);
  reference.add(new THREE.AxesHelper(100));
  // Keep axis labels in model coordinates so they rotate with the assembly.
  for (const [label, colour, position] of [
    ["X", "#b14445", [111, 0, 0]],
    ["Y", "#337b54", [0, 111, 0]],
    ["Z", "#356abb", [0, 0, 111]],
  ]) {
    const tile = document.createElement("canvas");
    tile.width = tile.height = 64;
    const ctx = tile.getContext("2d");
    ctx.fillStyle = colour;
    ctx.font = "bold 44px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(label, 32, 47);
    const sprite = new THREE.Sprite(
      new THREE.SpriteMaterial({
        map: new THREE.CanvasTexture(tile),
        depthTest: false,
      }),
    );
    sprite.position.fromArray(position);
    sprite.scale.set(11, 11, 1);
    sprite.renderOrder = 2000;
    reference.add(sprite);
  }
  scene.add(reference);
  const axisNames = ["X", "Y", "Z"];
  const cutState = axisNames.map((name, i) => ({
    name,
    enabled: false,
    value: i === 2 ? 120 : 0,
    direction: "below",
  }));
  const planes = axisNames.map(
    (_, i) =>
      new THREE.Plane(
        new THREE.Vector3(i === 0 ? -1 : 0, i === 1 ? -1 : 0, i === 2 ? -1 : 0),
        100000,
      ),
  );
  const planeGeometry = new THREE.PlaneGeometry(1500, 1500);
  const entries = [];
  function decode(base64, ArrayType) {
    const binary = atob(base64),
      bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return new ArrayType(bytes.buffer);
  }
  model.parts.forEach((part, index) => {
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute(
      "position",
      new THREE.BufferAttribute(decode(part.vertices, Float32Array), 3),
    );
    geometry.setIndex(
      new THREE.BufferAttribute(decode(part.indices, Uint32Array), 1),
    );
    geometry.computeVertexNormals();
    geometry.computeBoundingSphere();
    const material = new THREE.MeshStandardMaterial({
      color: part.colour,
      roughness: 0.72,
      metalness: 0.03,
      flatShading: true,
      clippingPlanes: planes,
    });
    const surface = new THREE.Mesh(geometry, material);
    surface.renderOrder = 1000;
    surface.userData.partIndex = index;
    const root = new THREE.Group();
    root.add(surface);
    scene.add(root);
    const sections = planes.map((plane, axis) => {
      const group = new THREE.Group();
      root.add(group);
      const order = index * 12 + axis * 3;
      for (const side of [THREE.BackSide, THREE.FrontSide]) {
        const op =
          side === THREE.BackSide
            ? THREE.IncrementWrapStencilOp
            : THREE.DecrementWrapStencilOp;
        const stencil = new THREE.MeshBasicMaterial({
          depthWrite: false,
          depthTest: false,
          colorWrite: false,
          stencilWrite: true,
          stencilFunc: THREE.AlwaysStencilFunc,
          side,
          clippingPlanes: [plane],
          stencilFail: op,
          stencilZFail: op,
          stencilZPass: op,
        });
        const mesh = new THREE.Mesh(geometry, stencil);
        mesh.renderOrder = order;
        group.add(mesh);
      }
      const capMat = new THREE.MeshStandardMaterial({
        color:
          part.kind === "placeholder"
            ? new THREE.Color(part.colour).multiplyScalar(0.82)
            : 0xce913a,
        roughness: 0.8,
        side: THREE.DoubleSide,
        clippingPlanes: planes.filter((p) => p !== plane),
        stencilWrite: true,
        stencilRef: 0,
        stencilFunc: THREE.NotEqualStencilFunc,
        stencilFail: THREE.ReplaceStencilOp,
        stencilZFail: THREE.ReplaceStencilOp,
        stencilZPass: THREE.ReplaceStencilOp,
      });
      const cap = new THREE.Mesh(planeGeometry, capMat);
      cap.renderOrder = order + 1;
      cap.onAfterRender = () => renderer.clearStencil();
      group.add(cap);
      return { group, cap };
    });
    entries.push({ part, root, surface, sections, visible: true });
  });
  const groupNames = [
    "Outer covers",
    "Body structure",
    "Head internals",
    "Drive and casters",
    "Purchased envelopes",
  ];
  axisNames.forEach((name, axis) => {
    const cut = document.createElement("div");
    cut.className = "cut";
    const low = Math.floor(model.bounds[0][axis] - 1),
      high = Math.ceil(model.bounds[1][axis] + 1);
    cut.innerHTML = `<div class="cut-head"><input type="checkbox" id="cut-${name}" aria-label="Enable ${name} cut"><label for="cut-${name}" class="axis-${name.toLowerCase()}">${name} plane</label><output id="value-${name}" for="range-${name}">0.0 mm</output></div><input id="range-${name}" type="range" min="${low}" max="${high}" step="0.1" aria-label="${name} cut position in millimetres"><select id="side-${name}" aria-label="${name} retained side"><option value="below">Keep ${name} ≤ plane</option><option value="above">Keep ${name} ≥ plane</option></select>`;
    $("cuts").append(cut);
    $(`cut-${name}`).onchange = (e) => {
      cutState[axis].enabled = e.target.checked;
      syncCuts();
    };
    $(`range-${name}`).oninput = (e) => {
      cutState[axis].value = Number(e.target.value);
      syncCuts();
    };
    $(`side-${name}`).onchange = (e) => {
      cutState[axis].direction = e.target.value;
      syncCuts();
    };
  });
  function syncCuts() {
    cutState.forEach((state, axis) => {
      const sign = state.direction === "below" ? -1 : 1;
      planes[axis].normal.setComponent(axis, sign);
      planes[axis].constant = state.enabled ? -sign * state.value : 100000;
      $(`cut-${state.name}`).checked = state.enabled;
      $(`range-${state.name}`).value = state.value;
      $(`side-${state.name}`).value = state.direction;
      $(`value-${state.name}`).textContent = state.value.toFixed(1) + " mm";
      entries.forEach((entry) => {
        const section = entry.sections[axis];
        section.group.visible = state.enabled && $("caps").checked;
        section.cap.position.set(0, 0, 0).setComponent(axis, state.value);
        section.cap.quaternion.setFromUnitVectors(
          new THREE.Vector3(0, 0, 1),
          planes[axis].normal,
        );
      });
    });
    updateStatus();
    requestRender();
  }
  groupNames.forEach((name, i) => {
    const label = document.createElement("label");
    label.className = "check";
    const box = document.createElement("input");
    box.type = "checkbox";
    box.checked = true;
    box.id = "group-" + i;
    box.onchange = () => {
      entries
        .filter((e) => e.part.group === name)
        .forEach((e) => (e.visible = box.checked));
      syncVisibility();
    };
    label.append(box, document.createTextNode(name));
    $("groups").append(label);
  });
  function syncVisibility() {
    entries.forEach((e) => (e.root.visible = e.visible));
    groupNames.forEach((name, i) => {
      const group = entries.filter((e) => e.part.group === name);
      const box = $("group-" + i);
      box.checked = group.every((e) => e.visible);
      box.indeterminate = group.some((e) => e.visible) && !box.checked;
    });
    $("shell-toggle").textContent = entries.some(
      (e) => e.part.group === "Outer covers" && e.visible,
    )
      ? "Hide covers"
      : "Show covers";
    renderList();
    updateStatus();
    requestRender();
  }
  function updateStatus() {
    const active = cutState
      .filter((s) => s.enabled)
      .map(
        (s) =>
          `${s.name} ${s.direction === "below" ? "≤" : "≥"} ${s.value.toFixed(1)}`,
      );
    $("status").textContent =
      `${entries.filter((e) => e.visible).length} / ${entries.length} visible` +
      (active.length ? " · " + active.join(", ") + " mm" : " · no cuts");
  }
  function renderList() {
    const query = $("search").value.toLowerCase().trim();
    $("parts").replaceChildren();
    let found = 0;
    groupNames.forEach((name) => {
      const group = entries.filter(
        (e) =>
          e.part.group === name &&
          (e.part.name + " " + e.part.label).toLowerCase().includes(query),
      );
      if (!group.length) return;
      const heading = document.createElement("div");
      heading.className = "group";
      heading.textContent = name;
      $("parts").append(heading);
      group.forEach((entry) => {
        found++;
        const row = document.createElement("div");
        row.className = "part-row" + (selected === entry ? " selected" : "");
        const box = document.createElement("input");
        box.type = "checkbox";
        box.checked = entry.visible;
        box.setAttribute("aria-label", "Show " + entry.part.label);
        box.onchange = () => {
          entry.visible = box.checked;
          syncVisibility();
        };
        const swatch = document.createElement("span");
        swatch.className = "swatch";
        swatch.style.background = entry.part.colour;
        const button = document.createElement("button");
        button.textContent = entry.part.label;
        if (entry.part.kind === "placeholder") {
          const small = document.createElement("small");
          small.textContent = "PLACEHOLDER envelope";
          button.append(small);
        }
        button.onclick = () => select(entry);
        row.append(box, swatch, button);
        $("parts").append(row);
      });
    });
    $("part-count").textContent =
      `${found} entries · checkbox changes visibility`;
  }
  function select(entry) {
    if (selected) selected.surface.material.emissive.set(0x000000);
    selected = entry;
    if (entry) {
      entry.surface.material.emissive.set(0x1c4764);
      $("selection-title").textContent = entry.part.label;
      $("selection-type").textContent =
        entry.part.kind === "placeholder"
          ? "PLACEHOLDER · purchased-part envelope"
          : "Printed part" +
            (entry.part.instance ? " · mirrored / repeated instance" : "");
      $("selection-type").className =
        "badge" + (entry.part.kind === "placeholder" ? " placeholder" : "");
      $("selection-size").textContent =
        entry.part.bounds[1]
          .map((v, i) => (v - entry.part.bounds[0][i]).toFixed(1))
          .join(" × ") + " mm · X × Y × Z";
      $("selection-notes").textContent = entry.part.notes;
      $("selection-actions").hidden = false;
    } else {
      $("selection-title").textContent = "Select in the model or list";
      $("selection-type").className = "";
      $("selection-type").textContent =
        `${entries.length} assembled entries, including 10 purchased envelope entries.`;
      $("selection-size").textContent = "";
      $("selection-notes").textContent =
        "Use the covers toggle to reach the internal parts.";
      $("selection-actions").hidden = true;
    }
    renderList();
    requestRender();
  }
  function fit(list = entries.filter((e) => e.visible)) {
    if (!list.length) {
      $("status").textContent =
        "All parts hidden. Use Show all to restore them.";
      return;
    }
    const box = new THREE.Box3();
    list.forEach((e) => {
      box.expandByPoint(new THREE.Vector3().fromArray(e.part.bounds[0]));
      box.expandByPoint(new THREE.Vector3().fromArray(e.part.bounds[1]));
    });
    box.getCenter(target);
    const radius = box.getSize(new THREE.Vector3()).length() * 0.5;
    const angle = Math.min(
      (camera.fov * Math.PI) / 360,
      Math.atan(Math.tan((camera.fov * Math.PI) / 360) * camera.aspect),
    );
    distance = Math.max(25, (radius / Math.sin(angle)) * 1.12);
    requestRender();
  }
  function reset() {
    cutState.forEach((s, i) => {
      s.enabled = false;
      s.value = i === 2 ? 120 : 0;
      s.direction = "below";
    });
    entries.forEach((e) => (e.visible = true));
    $("caps").checked = true;
    $("axes").checked = true;
    reference.visible = true;
    $("search").value = "";
    azimuth = 0.65;
    elevation = 0.24;
    select(null);
    syncCuts();
    syncVisibility();
    fit();
  }
  $("caps").onchange = syncCuts;
  $("axes").onchange = () => {
    reference.visible = $("axes").checked;
    requestRender();
  };
  $("search").oninput = renderList;
  $("all-show").onclick = () => {
    entries.forEach((e) => (e.visible = true));
    syncVisibility();
  };
  $("shell-toggle").onclick = () => {
    const visible = !entries.some(
      (e) => e.part.group === "Outer covers" && e.visible,
    );
    entries
      .filter((e) => e.part.group === "Outer covers")
      .forEach((e) => (e.visible = visible));
    syncVisibility();
  };
  $("fit").onclick = () => fit();
  $("reset").onclick = reset;
  $("fit-part").onclick = () => {
    if (selected) {
      selected.visible = true;
      syncVisibility();
      fit([selected]);
    }
  };
  $("isolate").onclick = () => {
    if (selected) {
      entries.forEach((e) => (e.visible = e === selected));
      syncVisibility();
      fit([selected]);
    }
  };
  $("save").onclick = () => {
    draw();
    const output = document.createElement("canvas");
    output.width = canvas.width;
    output.height = canvas.height;
    const context = output.getContext("2d");
    context.fillStyle = "#edf3f7";
    context.fillRect(0, 0, output.width, output.height);
    context.drawImage(canvas, 0, 0);
    const link = document.createElement("a");
    link.download = "pip-v0.3-section.png";
    link.href = output.toDataURL("image/png");
    link.click();
  };
  document.querySelectorAll("[data-preset]").forEach(
    (button) =>
      (button.onclick = () => {
        reset();
        const preset = button.dataset.preset;
        if (preset === "x" || preset === "quarter") {
          cutState[0].enabled = true;
          azimuth = preset === "x" ? 0.03 : 0.75;
          elevation = 0.18;
        }
        if (preset === "y" || preset === "quarter") {
          cutState[1].enabled = true;
          if (preset === "y") {
            azimuth = Math.PI / 2;
            elevation = 0.16;
          }
        }
        if (preset === "inside") {
          entries
            .filter((e) => e.part.group === "Outer covers")
            .forEach((e) => (e.visible = false));
          syncVisibility();
        }
        syncCuts();
      }),
  );
  const raycaster = new THREE.Raycaster();
  function pick(x, y) {
    const rect = canvas.getBoundingClientRect();
    raycaster.setFromCamera(
      new THREE.Vector2(
        ((x - rect.left) / rect.width) * 2 - 1,
        (-(y - rect.top) / rect.height) * 2 + 1,
      ),
      camera,
    );
    const hits = raycaster.intersectObjects(
      entries.filter((e) => e.visible).map((e) => e.surface),
    );
    const hit = hits.find((hit) =>
      planes.every((plane) => plane.distanceToPoint(hit.point) >= -0.001),
    );
    if (hit) select(entries[hit.object.userData.partIndex]);
  }
  const pointers = new Map();
  let moved = 0,
    gesture = null;
  function gestureState() {
    const points = [...pointers.values()];
    return {
      x: points.reduce((s, p) => s + p.x, 0) / points.length,
      y: points.reduce((s, p) => s + p.y, 0) / points.length,
      span:
        points.length === 2
          ? Math.hypot(points[0].x - points[1].x, points[0].y - points[1].y)
          : 0,
    };
  }
  function pan(dx, dy) {
    camera.updateMatrixWorld();
    const scale =
      (2 * distance * Math.tan((camera.fov * Math.PI) / 360)) /
      canvas.clientHeight;
    target.addScaledVector(
      new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0),
      -dx * scale,
    );
    target.addScaledVector(
      new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1),
      dy * scale,
    );
  }
  canvas.oncontextmenu = (e) => e.preventDefault();
  canvas.onpointerdown = (event) => {
    canvas.focus({ preventScroll: true });
    canvas.setPointerCapture(event.pointerId);
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    moved = 0;
    gesture = gestureState();
  };
  canvas.onpointermove = (event) => {
    if (!pointers.has(event.pointerId)) return;
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    const next = gestureState(),
      dx = next.x - gesture.x,
      dy = next.y - gesture.y;
    moved += Math.abs(dx) + Math.abs(dy);
    if (pointers.size > 1) {
      if (gesture.span && next.span)
        distance = THREE.MathUtils.clamp(
          (distance * gesture.span) / next.span,
          15,
          4000,
        );
      pan(dx, dy);
    } else if (event.shiftKey || event.buttons === 2 || event.buttons === 4)
      pan(dx, dy);
    else {
      azimuth -= dx * 0.007;
      elevation = THREE.MathUtils.clamp(elevation + dy * 0.007, -1.48, 1.48);
    }
    gesture = next;
    requestRender();
  };
  function release(event) {
    if (!pointers.has(event.pointerId)) return;
    const single = pointers.size === 1;
    pointers.delete(event.pointerId);
    if (single && moved < 4 && event.type === "pointerup" && event.button === 0)
      pick(event.clientX, event.clientY);
    if (pointers.size) {
      gesture = gestureState();
      moved = 10;
    }
  }
  canvas.onpointerup = release;
  canvas.onpointercancel = release;
  canvas.addEventListener(
    "wheel",
    (e) => {
      e.preventDefault();
      distance = THREE.MathUtils.clamp(
        distance * Math.exp(e.deltaY * 0.001),
        15,
        4000,
      );
      requestRender();
    },
    { passive: false },
  );
  canvas.onkeydown = (event) => {
    const actions = {
      ArrowLeft: () => (azimuth += 0.1),
      ArrowRight: () => (azimuth -= 0.1),
      ArrowUp: () => (elevation = Math.min(1.48, elevation + 0.1)),
      ArrowDown: () => (elevation = Math.max(-1.48, elevation - 0.1)),
      "+": () => (distance *= 0.9),
      "=": () => (distance *= 0.9),
      "-": () => (distance *= 1.1),
      Home: () => fit(),
    };
    if (actions[event.key]) {
      event.preventDefault();
      actions[event.key]();
      distance = THREE.MathUtils.clamp(distance, 15, 4000);
      requestRender();
    }
  };
  function resize() {
    const width = stage.clientWidth,
      height = stage.clientHeight;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    requestRender();
  }
  new ResizeObserver(resize).observe(stage);
  resize();
  reset();
  // A read-only state snapshot supports reproducible browser checks without a test UI.
  window.pipViewerState = () => ({
    version: model.version,
    parts: entries.length,
    triangles: model.parts.reduce((n, p) => n + p.triangles, 0),
    visible: entries.filter((e) => e.visible).map((e) => e.part.name),
    selected: selected?.part.name ?? null,
    cuts: cutState.map((s) => ({ ...s })),
    capped: $("caps").checked,
    axes: reference.visible,
    camera: { azimuth, elevation, distance, target: target.toArray() },
    render: {
      calls: renderer.info.render.calls,
      triangles: renderer.info.render.triangles,
    },
    webgl: renderer.getContext().getContextAttributes(),
    sourceHashes: model.sourceHashes,
  });
  console.info(
    `Pip viewer ready: ${entries.length} registry entries, ${model.parts.reduce((n, p) => n + p.triangles, 0)} triangles; all geometry is inline.`,
  );
})();
