# Viewer verification

Date: 21 October 2026. Model: `0.3-prototype`.

- `scripts/viewer.sh` exported 44 non-calibration registry entries and 57,330 triangles, including all 10 purchased envelope entries.
- `verify_export.py` passed. Every embedded vertex and triangle index matches the current manifold CAD, and all four geometry source hashes match.
- `node --check` passed for `viewer.js` and `browser-check.js`.
- The initial T3 browser check passed 20 desktop checks at 1440 × 950. The main agent then ran the final `browser-check.js` after regeneration: **23 checks passed at 1280 × 800**, including actual rendered-pixel comparisons, independent X and Y movement, Y reversal, all three cuts, caps, group visibility, part search and selection, isolation, reset, keyboard orbit, wheel zoom, axes and PNG generation. [main-review.json](evidence/main-review.json) records the results and CAD hashes.
- The main agent independently inspected the desktop quarter cut and the responsive layout at an actual 390 × 844 viewport. The phone layout had a 390 px scroll width with no horizontal overflow, and controls stacked below the model. Its 10 functional checks passed.
- Saved main-agent page captures: [desktop quarter cut](evidence/main-desktop-quarter.png) and [phone layout](evidence/main-mobile.png). These precede the final help-text update. Geometry and interaction controls are unchanged.
- [quarter-cut.png](evidence/quarter-cut.png) is the rendered viewport exported through the viewer's **Save PNG** handler. It shows true shell thickness, cut material caps, and the internal envelopes.

T3 full-page snapshots timed out in the subagent-owned background tab. Click and evaluate worked, and the rendered canvas was inspected directly. The main agent's own T3 tab produced successful desktop and phone snapshots. The subagent did not substitute external browser automation. The Browser plugin was absent. T3 `html_preview` rejected the complete offline HTML because it exceeds that tool's 512 KB input limit.

Mouse pan, touch gesture feel, and opening the downloaded file through a local `file:` URL were not automated. The generated page contains no external resources, fetches, or module imports. The inspected HTTP-served page loaded no external resource dependencies. These checks concern the viewer and geometric fidelity, not real hardware fit or manufacturing readiness.
