/* Run this expression through T3 preview_evaluate on the generated viewer. */
(async () => {
  const checks = [];
  const $ = (id) => document.getElementById(id);
  const state = () => window.pipViewerState();
  const assert = (condition, message) => {
    if (!condition) throw new Error(message);
    checks.push(message);
  };
  const frame = () =>
    new Promise((resolve) =>
      requestAnimationFrame(() => requestAnimationFrame(resolve)),
    );
  const fingerprint = () => {
    const sample = document.createElement("canvas");
    sample.width = sample.height = 80;
    const ctx = sample.getContext("2d");
    ctx.drawImage(document.querySelector("#stage canvas"), 0, 0, 80, 80);
    return sample.toDataURL();
  };
  $("reset").click();
  await frame();
  assert(
    state().parts === 44 && state().triangles === 57330,
    "44 current registry entries and 57,330 triangles loaded",
  );
  assert(
    state().visible.length === 44 && !state().cuts.some((c) => c.enabled),
    "Reset restores all parts and disables every cut",
  );
  assert(
    getComputedStyle($("selection-actions")).display === "none",
    "Selection actions are hidden until a part is selected",
  );
  const assembly = fingerprint();
  document.querySelector('[data-preset="quarter"]').click();
  await frame();
  assert(
    state().cuts[0].enabled &&
      state().cuts[1].enabled &&
      !state().cuts[2].enabled,
    "Quarter preset independently enables X and Y",
  );
  const quarter = fingerprint();
  assert(quarter !== assembly, "Quarter cut changes the rendered pixels");
  $("range-X").value = "-22.5";
  $("range-X").dispatchEvent(new Event("input"));
  await frame();
  assert(
    state().cuts[0].value === -22.5 && state().cuts[1].value === 0,
    "X slider changes X while retaining the Y position",
  );
  assert(
    fingerprint() !== quarter,
    "Moving the X plane changes the rendered section",
  );
  $("range-Y").value = "14.5";
  $("range-Y").dispatchEvent(new Event("input"));
  await frame();
  assert(
    state().cuts[1].value === 14.5 && state().cuts[0].value === -22.5,
    "Y slider changes Y while retaining the X position",
  );
  const belowY = fingerprint();
  $("side-Y").value = "above";
  $("side-Y").dispatchEvent(new Event("change"));
  await frame();
  assert(
    state().cuts[1].direction === "above",
    "Y direction selector reverses the retained half",
  );
  assert(
    fingerprint() !== belowY,
    "Reversing the Y cut changes the rendered half",
  );
  $("cut-Z").click();
  $("range-Z").value = "210";
  $("range-Z").dispatchEvent(new Event("input"));
  await frame();
  assert(
    state().cuts.every((c) => c.enabled) && state().cuts[2].value === 210,
    "All three cutting planes work together",
  );
  const capped = fingerprint();
  $("caps").click();
  await frame();
  assert(
    !state().capped && fingerprint() !== capped,
    "Cut-face toggle changes the actual rendered image",
  );
  $("reset").click();
  $("shell-toggle").click();
  await frame();
  assert(
    state().visible.length === 40 && !state().visible.includes("head_cap"),
    "Covers toggle removes four outer covers",
  );
  $("group-4").click();
  await frame();
  assert(
    !state().visible.some((name) => name.startsWith("ref_")),
    "Purchased-envelope group visibility hides every purchased envelope",
  );
  $("all-show").click();
  $("search").value = "QW01";
  $("search").dispatchEvent(new Event("input"));
  assert(
    document.querySelectorAll(".part-row").length === 1,
    "Part search finds the named power bank",
  );
  document.querySelector(".part-row button").click();
  assert(
    state().selected === "ref_power_bank" &&
      $("selection-type").textContent.includes("PLACEHOLDER"),
    "Selecting a purchased part labels it PLACEHOLDER",
  );
  $("isolate").click();
  await frame();
  assert(
    state().visible.length === 1 && state().visible[0] === "ref_power_bank",
    "Isolate displays only the selected bank",
  );
  $("reset").click();
  await frame();
  const canvas = document.querySelector("#stage canvas");
  const beforeOrbit = state().camera.azimuth;
  canvas.dispatchEvent(
    new KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true }),
  );
  await frame();
  assert(
    state().camera.azimuth !== beforeOrbit,
    "Keyboard orbit changes the camera",
  );
  const beforeZoom = state().camera.distance;
  canvas.dispatchEvent(
    new WheelEvent("wheel", { deltaY: -100, bubbles: true, cancelable: true }),
  );
  await frame();
  assert(
    state().camera.distance < beforeZoom,
    "Wheel zoom moves the camera closer",
  );
  $("axes").click();
  assert(!state().axes, "Reference axes toggle responds");
  const originalClick = HTMLAnchorElement.prototype.click;
  let exported = null;
  try {
    HTMLAnchorElement.prototype.click = function () {
      exported = { name: this.download, data: this.href };
    };
    $("save").click();
  } finally {
    HTMLAnchorElement.prototype.click = originalClick;
  }
  assert(
    exported?.name === "pip-v0.3-section.png" &&
      exported.data.startsWith("data:image/png;base64,"),
    "Save PNG produces a named PNG from the rendered view",
  );
  $("reset").click();
  await frame();
  assert(
    document.documentElement.scrollWidth <= innerWidth,
    "Page has no horizontal overflow at this viewport",
  );
  assert(
    performance.getEntriesByType("resource").length === 0,
    "Page loads no external resource dependencies",
  );
  return {
    passed: checks.length,
    checks,
    viewport: [innerWidth, innerHeight],
    state: state(),
  };
})();
