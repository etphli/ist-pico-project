"""Drawing kit shared by every Pip illustration.

One canvas unit is one PNG pixel. x grows right and y grows DOWN, as in SVG, so the
coordinates in wiring.py and the other layout files read like screen positions.
Every label is real text: SVG output keeps it as editable <text> elements.

Colours, badge styles and font sizes live here. Change them here, not per drawing.
"""

from pathlib import Path
import re
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Circle, Polygon

DPI = 100
REPO = Path(__file__).resolve().parents[1]

# ----------------------------------------------------------------------------- palette
BG = "#E4E2DC"          # medium-light neutral page
PANEL = "#F3F2EE"       # zone panels
CARD = "#FCFBF8"        # component boxes
INK = "#14305A"         # dark blue body text and outlines
INK2 = "#3D4F66"        # secondary text
MUTED = "#8A94A3"       # unused / not connected
EDGE = "#33475B"

NETS = {
    #  key        colour     casing      legend text
    "5V":     ("#D62828", "#7A1010", "5 V supply (BODY_5V / HEAD_5V)"),
    "3V3":    ("#C0168C", "#5E0A45", "3.3 V (Pico 3V3 OUT, 3V terminal)"),
    "GND":    ("#161616", "#161616", "Ground"),
    "SDA":    ("#1F5BD6", "#0D2D6E", "I2C SDA (data)"),
    "SCL":    ("#F2C200", "#6B5800", "I2C SCL (clock)"),
    "SIG":    ("#0E9384", "#06463F", "Signal (servo PWM)"),
    "MOTOR_A": ("#7A4EB5", "#3B2160", "Motor terminal A (separate conductor)"),
    "MOTOR_B": ("#A0522D", "#4E2410", "Motor terminal B (separate conductor)"),
    "WIFI":   ("#5B6B7F", "#5B6B7F", "Wi-Fi data only (no wire, no power)"),
    "USB":    ("#D62828", "#55606E", "USB cable carrying 5 V"),
    "PROPOSED": ("#E0590B", "#7A2E04", "Proposed route (not modelled)"),
}

INSULATION = {"black": "#161616", "red": "#D62828", "blue": "#1F5BD6", "yellow": "#F2C200"}

BADGES = {
    # kind:        (fill,      text,      edge,      dashed)
    "HOLD":         ("#F5A623", "#2B1A00", "#9A6200", False),
    "STOP":         ("#8E1B1B", "#FFFFFF", "#5A0F0F", False),
    "UNVERIFIED":   ("#E3DDF5", "#3A2C80", "#5B4BB0", False),
    "NOT SELECTED": ("#FFFFFF", "#33475B", "#33475B", True),
    "FUTURE":       ("#D4E6F9", "#14305A", "#3C6EA8", False),
    "LOGICAL":      ("#14305A", "#FFFFFF", "#14305A", False),
    "CAD":          ("#2F6B4F", "#FFFFFF", "#1E4634", False),
    "OK":           ("#DCEFE3", "#1E4634", "#2F6B4F", False),
    "PROPOSED":     ("#FCE3D2", "#7A2E04", "#E0590B", False),
    "PENDING":      ("#FFFFFF", "#3D4F66", "#8A94A3", True),
}

FONT = "DejaVu Sans"            # bundled with matplotlib: identical PNGs on every machine
SVG_FONT_STACK = "'DejaVu Sans', 'Helvetica Neue', Arial, sans-serif"

plt.rcParams.update({
    "font.family": FONT,
    "svg.fonttype": "none",       # keep <text>, do not outline glyphs
    "svg.hashsalt": "pip-illustrations",
    "path.simplify": False,
})


def pt(px):
    """Font size in canvas pixels -> matplotlib points."""
    return px * 72.0 / DPI


def wrap(text, width_px, size_px):
    """Wrap to a pixel width. DejaVu Sans averages ~0.56 em per character."""
    chars = max(8, int(width_px / (0.56 * size_px)))
    out = []
    for para in text.split("\n"):
        out.append(textwrap.fill(para, chars) if para else "")
    return "\n".join(out)


class Canvas:
    def __init__(self, width, height, title, subtitle="", badges=(), footer=None, number=None):
        self.W, self.H = width, height
        self.fig = plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI)
        self.fig.patch.set_facecolor(BG)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(height, 0)
        self.ax.set_axis_off()
        self.ax.set_facecolor(BG)
        self.pins = {}
        self.labels = []          # text artists checked for collisions
        self.allow = set()        # pairs of gids allowed to touch
        head = f"{number} · {title}" if number else title
        self.text(56, 46, head, 44, bold=True, gid="title")
        if subtitle:
            self.text(58, 112, subtitle, 25, color=INK2, gid="subtitle")
        x = width - 56
        for kind, label in reversed(list(badges)):
            x = self.badge(x, 58, kind, label, size=24, anchor="right") - 16
        if footer is None:
            footer = "Pip v0.3 · no part of Pip has been built or tested · all bought parts are placeholders"
        self.text(56, height - 34, footer, 20, color=INK2, gid="footer")

    # ------------------------------------------------------------------ primitives
    def text(self, x, y, s, size=24, color=INK, bold=False, ha="left", va="center",
             gid=None, check=True, box=None, italic=False, z=10, linespacing=1.25):
        kw = {}
        if box:
            fc, ec = box
            kw["bbox"] = dict(boxstyle="round,pad=0.35,rounding_size=0.5", fc=fc, ec=ec, lw=1.5)
        t = self.ax.text(x, y, s, fontsize=pt(size), color=color, ha=ha, va=va,
                         fontweight="bold" if bold else "normal",
                         fontstyle="italic" if italic else "normal",
                         zorder=z, linespacing=linespacing, **kw)
        if gid:
            t.set_gid(gid)
        if check:
            self.labels.append(t)
        return t

    def para(self, x, y, s, width, size=22, **kw):
        return self.text(x, y, wrap(s, width, size), size, va="top", **kw)

    def rect(self, x, y, w, h, fc=CARD, ec=EDGE, lw=2.0, r=14, ls="-", z=2, gid=None, alpha=1.0):
        p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                           fc=fc, ec=ec, lw=lw, ls=ls, zorder=z, alpha=alpha)
        if gid:
            p.set_gid(gid)
        self.ax.add_patch(p)
        return p

    def line(self, pts, color, lw=4.0, ls="-", z=4, casing=None, gid=None, alpha=1.0):
        xs, ys = zip(*pts)
        if casing:
            c = Line2D(xs, ys, color=casing, lw=lw + 3, ls=ls, zorder=z - 0.1,
                       solid_capstyle="round", solid_joinstyle="round", alpha=alpha)
            self.ax.add_line(c)
        ln = Line2D(xs, ys, color=color, lw=lw, ls=ls, zorder=z,
                    solid_capstyle="round", solid_joinstyle="round",
                    dash_capstyle="butt", alpha=alpha)
        if gid:
            ln.set_gid(gid)
        self.ax.add_line(ln)
        return ln

    def arrow(self, a, b, color=INK, lw=3.0, z=6, head=18):
        self.ax.annotate("", xy=b, xytext=a, zorder=z,
                         arrowprops=dict(arrowstyle=f"-|>,head_length={head / 20},head_width={head / 40}",
                                         color=color, lw=lw, shrinkA=0, shrinkB=0))

    def dot(self, x, y, r=7, color=INK, z=7):
        self.ax.add_patch(Circle((x, y), r, fc=color, ec="none", zorder=z))

    def cross(self, x, y, s=16, color="#8E1B1B", lw=5, z=8):
        self.line([(x - s, y - s), (x + s, y + s)], color, lw, z=z)
        self.line([(x - s, y + s), (x + s, y - s)], color, lw, z=z)

    def poly(self, pts, fc, ec=EDGE, lw=2, z=3):
        self.ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=z))

    # ------------------------------------------------------------------ badges and tags
    def badge(self, x, y, kind, label=None, size=20, anchor="left", gid=None):
        """Status pill. Returns the x of its far edge (left edge when anchor='right')."""
        fill, ink, edge, dashed = BADGES[kind]
        label = label or kind
        ha = {"left": "left", "right": "right", "center": "center"}[anchor]
        t = self.ax.text(x, y, label, fontsize=pt(size), color=ink, fontweight="bold",
                         ha=ha, va="center", zorder=12,
                         bbox=dict(boxstyle="round,pad=0.42,rounding_size=0.9", fc=fill, ec=edge,
                                   lw=2.0, ls="--" if dashed else "-"))
        t.set_gid(gid or f"badge-{label}".replace(" ", "-"))
        self.labels.append(t)
        self.fig.canvas.draw()
        bb = t.get_bbox_patch().get_window_extent()
        inv = self.ax.transData.inverted()
        (x0, _), (x1, _) = inv.transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
        return max(x0, x1) if anchor == "left" else min(x0, x1)

    def tag(self, x, y, text, net, sub=None, swatch=None, size=22, gid=None, dashed=False):
        """Wire ID tag sitting on a wire: white pill with a net-coloured border."""
        colour = NETS[net][0] if net in NETS else net
        s = text if not sub else f"{text}  {sub}"
        t = self.ax.text(x, y, s, fontsize=pt(size), color=INK, fontweight="bold",
                         ha="center", va="center", zorder=13,
                         bbox=dict(boxstyle="round,pad=0.38,rounding_size=0.7", fc="white",
                                   ec=colour, lw=3.0, ls="--" if dashed else "-"))
        t.set_gid(gid or f"tag-{text}")
        self.labels.append(t)
        if swatch:
            # insulation colour chip, placed just left of the tag text
            self.fig.canvas.draw()
            bb = t.get_bbox_patch().get_window_extent()
            inv = self.ax.transData.inverted()
            (x0, y0), (x1, y1) = inv.transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
            cy = (y0 + y1) / 2
            self.rect(x0 - 34, cy - 11, 22, 22, fc=INSULATION[swatch], ec=INK, lw=1.5, r=4, z=14)
        return t

    # ------------------------------------------------------------------ components
    def component(self, cid, x, y, w, h, title, sub=None, pins=(), fc=CARD, ec=EDGE,
                  ls="-", title_size=27, sub_size=21, pin_size=21, title_y=None, lw=2.5):
        """Box with a title and optional pins.

        pins: (name, side, offset, label, net) with side in l/r/t/b and offset measured
        from the box top (l/r) or left (t/b). The pin label is drawn inside the box.
        """
        self.rect(x, y, w, h, fc=fc, ec=ec, ls=ls, lw=lw, gid=f"box-{cid}")
        ty = title_y if title_y is not None else y + 34
        self.text(x + w / 2, ty, title, title_size, bold=True, ha="center", gid=f"title-{cid}")
        if sub:
            self.text(x + w / 2, ty + title_size * 0.62 + sub_size * 0.75, sub, sub_size,
                      color=INK2, ha="center", va="top", gid=f"sub-{cid}", linespacing=1.2)
        for name, side, off, label, net in pins:
            if side == "l":
                px, py, tx, ha = x, y + off, x + 22, "left"
            elif side == "r":
                px, py, tx, ha = x + w, y + off, x + w - 22, "right"
            elif side == "t":
                px, py, tx, ha = x + off, y, x + off, "center"
            else:
                px, py, tx, ha = x + off, y + h, x + off, "center"
            self.pins[(cid, name)] = (px, py)
            if net == "anchor":          # attachment point only, nothing drawn
                continue
            colour = NETS[net][0] if net in NETS else (MUTED if net == "unused" else (net or EDGE))
            self.rect(px - 9, py - 9, 18, 18, fc=colour, ec=INK, lw=1.5, r=3, z=6)
            if label:
                ty2 = py if side in "lr" else (py + 30 if side == "t" else py - 30)
                self.text(tx, ty2, label, pin_size, bold=True, ha=ha, gid=f"pin-{cid}-{name}",
                          color=INK if net != "unused" else MUTED)
            self.pins[(cid, name)] = (px, py)
        return (x, y, w, h)

    def P(self, cid, name, dx=0, dy=0):
        x, y = self.pins[(cid, name)]
        return (x + dx, y + dy)

    def wire(self, pts, net, lw=6, dashed=False, gid=None, z=4):
        colour, casing, _ = NETS[net]
        ls = (0, (5, 3)) if dashed else "-"
        if net == "WIFI":
            return self.line(pts, colour, lw=4, ls=(0, (2, 2.5)), z=z, gid=gid)
        if net == "USB":
            self.line(pts, "#9AA3AD", lw=lw + 10, z=z - 0.2, casing=casing)
            return self.line(pts, colour, lw=lw - 1, z=z, ls=ls, gid=gid)
        if dashed:   # solid pale underlay keeps a dashed (unselected) wire readable
            self.line(pts, "#FFFFFF", lw=lw + 4, z=z - 0.2)
            return self.line(pts, colour, lw=lw, ls=ls, z=z, gid=gid)
        return self.line(pts, colour, lw=lw, ls=ls, z=z, casing=casing, gid=gid)

    def bundle(self, pts, gap=7, lw=3.6, gid=None, z=4, order=("GND", "3V3", "SDA", "SCL")):
        """Four-conductor PiicoDev cable: grey jacket with all four nets inside."""
        self.line(pts, "#B8BEC6", lw=gap * 4 + 10, z=z - 0.3, casing="#55606E")
        import numpy as np
        p = np.array(pts, float)
        for i, net in enumerate(order):
            off = (i - 1.5) * gap
            q = []
            for k in range(len(p)):
                a = p[max(k - 1, 0)]
                b = p[min(k + 1, len(p) - 1)]
                d = b - a
                n = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-9)
                q.append(tuple(p[k] + n * off))
            self.line(q, NETS[net][0], lw=lw, z=z)

    # ------------------------------------------------------------------ panels
    def panel(self, x, y, w, h, heading=None, fc=PANEL, ec="#B9B4AA", heading_size=26, badge=None, gid=None):
        self.rect(x, y, w, h, fc=fc, ec=ec, lw=2, r=18, z=1, gid=gid)
        if heading:
            self.text(x + 24, y + 34, heading, heading_size, bold=True, gid=f"heading-{gid or heading[:20]}")
            if badge:
                kind, label = badge if isinstance(badge, tuple) else (badge, None)
                self.badge(x + w - 24, y + 34, kind, label, size=20, anchor="right")

    def notes(self, x, y, w, items, size=22, numbered=True, gap=12, color=INK, bullet_badges=None):
        """Numbered or bulleted note list. Returns the y below the last note."""
        cy = y
        for i, item in enumerate(items, 1):
            prefix = f"{i}." if numbered else "•"
            self.text(x, cy, prefix, size, bold=True, va="top", color=color, check=False)
            body = wrap(item, w - 44, size)
            t = self.text(x + 40, cy, body, size, va="top", color=color)
            cy += (body.count("\n") + 1) * size * 1.28 + gap
        return cy

    def legend(self, x, y, nets, size=21, col_w=560, rows=None):
        rows = rows or len(nets)
        for i, net in enumerate(nets):
            cx = x + (i // rows) * col_w
            cy = y + (i % rows) * (size * 1.7)
            colour, casing, label = NETS[net]
            if net == "WIFI":
                self.line([(cx, cy), (cx + 70, cy)], colour, lw=4, ls=(0, (2, 2.5)), z=6)
            elif net == "PROPOSED":
                self.line([(cx, cy), (cx + 70, cy)], colour, lw=6, ls=(0, (4, 2)), z=6)
            else:
                self.wire([(cx, cy), (cx + 70, cy)], net, z=6)
            self.text(cx + 90, cy, label, size, gid=f"legend-{net}")

    def callout(self, text, anchor, at, size=22, width=None, ha="left", color=INK, ec="#9DA9B8",
                fc="white", gid=None, dot=True):
        """Label box at `at` (top-left when ha='left') with a leader line to `anchor`."""
        body = wrap(text, width, size) if width else text
        t = self.text(at[0], at[1], body, size, va="top", ha=ha, color=color, box=(fc, ec), gid=gid, z=15)
        self.fig.canvas.draw()
        bb = t.get_bbox_patch().get_window_extent()
        inv = self.ax.transData.inverted()
        (x0, y0), (x1, y1) = inv.transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
        x0, x1 = sorted((x0, x1))
        y0, y1 = sorted((y0, y1))
        ax_, ay_ = anchor
        ex = min(max(ax_, x0), x1)
        ey = min(max(ay_, y0), y1)
        if x0 <= ax_ <= x1:
            ey = y0 if ay_ < y0 else y1
        elif y0 <= ay_ <= y1:
            ex = x0 if ax_ < x0 else x1
        self.line([(ex, ey), anchor], "#1B2F4B", lw=2.4, z=14)
        if dot:
            self.ax.add_patch(Circle(anchor, 7, fc="#1B2F4B", ec="white", lw=2, zorder=16))
        return t

    def marker(self, x, y, label, fc="#14305A", size=22, r=20):
        self.ax.add_patch(Circle((x, y), r, fc=fc, ec="white", lw=2.5, zorder=16))
        t = self.ax.text(x, y, label, fontsize=pt(size), color="white", fontweight="bold",
                         ha="center", va="center", zorder=17)
        return t

    # ------------------------------------------------------------------ CAD image
    def image(self, img, extent, box, fit="contain", border=True):
        """Place a rendered CAD image (from cad/render.py) inside box=(x, y, w, h).
        Returns a function mapping projected millimetres (right, up) to canvas pixels."""
        x, y, w, h = box
        bx0, bx1, by0, by1 = extent
        sw, sh = bx1 - bx0, by1 - by0
        s = min(w / sw, h / sh)
        iw, ih = sw * s, sh * s
        ox, oy = x + (w - iw) / 2, y + (h - ih) / 2
        if border:
            self.rect(x - 6, y - 6, w + 12, h + 12, fc="#F7F7F5", ec="#C9C5BD", lw=1.5, r=14, z=1)
        self.ax.imshow(img, extent=(ox, ox + iw, oy + ih, oy), zorder=2, interpolation="lanczos")

        def to_canvas(u, v):
            return (ox + (u - bx0) * s, oy + (by1 - v) * s)
        return to_canvas

    # ------------------------------------------------------------------ output
    def check(self):
        """Report labels that overlap each other or leave the canvas."""
        self.fig.canvas.draw()
        inv = self.ax.transData.inverted()
        boxes = []
        for t in self.labels:
            if not t.get_text().strip():
                continue
            patch = t.get_bbox_patch()
            bb = patch.get_window_extent() if patch else t.get_window_extent()
            (x0, y0), (x1, y1) = inv.transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
            x0, x1 = sorted((x0, x1))
            y0, y1 = sorted((y0, y1))
            boxes.append((t.get_text().split("\n")[0][:40], x0, y0, x1, y1))
        problems = []
        for i, a in enumerate(boxes):
            if a[1] < 4 or a[2] < 4 or a[3] > self.W - 4 or a[4] > self.H - 4:
                problems.append(f"off-canvas: {a[0]!r}")
            for b in boxes[i + 1:]:
                if a[1] < b[3] - 1 and b[1] < a[3] - 1 and a[2] < b[4] - 1 and b[2] < a[4] - 1:
                    problems.append(f"overlap: {a[0]!r} / {b[0]!r}")
        return problems

    def save(self, out_dir, stem, svg=True):
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        problems = self.check()
        png = out_dir / f"{stem}.png"
        self.fig.savefig(png, dpi=DPI, facecolor=BG, metadata={"Software": None})
        written = [png]
        if svg:
            path = out_dir / f"{stem}.svg"
            self.fig.savefig(path, facecolor=BG, metadata={"Date": None, "Creator": None})
            src = path.read_text()
            src = re.sub(r"'DejaVu Sans'|DejaVu Sans", SVG_FONT_STACK, src)
            path.write_text(src)
            written.append(path)
        plt.close(self.fig)
        return written, problems
