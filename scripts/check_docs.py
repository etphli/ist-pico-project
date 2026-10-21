#!/usr/bin/env python3
"""Check local documentation links, illustration files, BOM maths and viewer freshness.

Run with python3 scripts/check_docs.py. No third-party packages are required.
External links, rendered layouts and physical assembly require separate review.
"""

import csv
import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    failures = []
    documents = [ROOT / "README.md", ROOT / "cad/README.md", *sorted((ROOT / "docs").glob("*.md")),
                 ROOT / "cad/viewer/README.md", ROOT / "illustrations/README.md"]
    checked_links = 0
    for document in documents:
        if not document.is_file():
            failures.append(f"Missing document: {document.relative_to(ROOT)}")
            continue
        # This repository uses inline Markdown links without spaces in their targets.
        for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", document.read_text()):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            checked_links += 1
            if not (document.parent / unquote(parsed.path)).exists():
                failures.append(f"Broken local link in {document.relative_to(ROOT)}: {target}")

    original = sorted((ROOT / "docs/images/assembly").glob("*.png"))
    if len(original) != 8:
        failures.append(f"Expected eight original assembly illustrations, found {len(original)}")
    pictures = sorted((ROOT / "docs/images").rglob("*.png"))
    for picture in pictures:
        data = picture.read_bytes()
        if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 1000:
            failures.append(f"Invalid PNG: {picture.relative_to(ROOT)}")
        elif min(struct.unpack(">II", data[16:24])) < 500:
            failures.append(f"Illustration below 500 pixels on its shorter edge: {picture.relative_to(ROOT)}")
        if picture.parent.name == "wiring" and not picture.with_suffix(".svg").is_file():
            failures.append(f"Wiring diagram has no editable SVG: {picture.relative_to(ROOT)}")
    vectors = sorted((ROOT / "docs/images").rglob("*.svg"))
    for vector in vectors:
        try:
            tree = ET.parse(vector)
            if not tree.findall(".//{http://www.w3.org/2000/svg}text"):
                failures.append(f"SVG has no editable text: {vector.relative_to(ROOT)}")
            if not vector.with_suffix(".png").is_file():
                failures.append(f"SVG has no PNG companion: {vector.relative_to(ROOT)}")
        except ET.ParseError as error:
            failures.append(f"Invalid SVG {vector.relative_to(ROOT)}: {error}")

    with (ROOT / "docs/bom.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    priced = [row for row in rows if "full" in row["option"].split(";") and row["ext_aud_inc_gst"]]
    for row in priced:
        expected = Decimal(row["qty"]) * Decimal(row["unit_aud_inc_gst"])
        if expected != Decimal(row["ext_aud_inc_gst"]):
            failures.append(f"BOM extension does not match quantity × unit price: {row['id']}")
    subtotal = sum((Decimal(row["ext_aud_inc_gst"]) for row in priced), Decimal(0))
    if f"**{subtotal:.2f}**" not in (ROOT / "docs/08-bom-budget-sourcing.md").read_text():
        failures.append(f"Budget document does not contain computed subtotal {subtotal:.2f}")

    manifest_path = ROOT / "cad/viewer/model-manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for name, expected in manifest["sourceHashes"].items():
            actual = hashlib.sha256((ROOT / "cad" / name).read_bytes()).hexdigest()
            if actual != expected:
                failures.append(f"Viewer geometry is stale relative to {name}. Run scripts/viewer.sh")
        html = (ROOT / "cad/viewer/index.html").read_text()
        for marker in ("/* THREE_LIBRARY */", "/* MODEL_DATA */", "/* VIEWER_CODE */"):
            if marker in html:
                failures.append(f"Unexpanded viewer template marker: {marker}")
        for source in ("viewer.js",):
            if (ROOT / "cad/viewer" / source).read_text() not in html:
                failures.append(f"Generated viewer does not include current {source}")
    else:
        failures.append("Missing viewer manifest")

    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        raise SystemExit(1)
    print(f"PASS: {len(documents)} documents, {checked_links} local links, {len(pictures)} PNGs, {len(vectors)} editable SVGs")
    print(f"PASS: priced full-concept BOM subtotal AU${subtotal:.2f}; unpriced items remain excluded")
    print(f"PASS: viewer CAD hashes and generated JavaScript match current sources")


if __name__ == "__main__":
    main()
