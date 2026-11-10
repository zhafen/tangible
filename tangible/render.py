"""Render the top level of a repository as labelled rectangles (SVG)."""

import math
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

IGNORED = {".git"}
CHAR_W, HEIGHT, PAD, GAP = 9, 60, 12, 20


@dataclass(frozen=True)
class Rect:
    name: str
    is_dir: bool
    x: int
    y: int
    w: int
    h: int


def layout(root) -> list[Rect]:
    """Place one rectangle per top-level entry of `root` on a grid."""
    entries = sorted(
        (p for p in Path(root).iterdir() if p.name not in IGNORED),
        key=lambda p: (not p.is_dir(), p.name),
    )
    if not entries:
        return []
    w = max(len(p.name) for p in entries) * CHAR_W + 2 * PAD
    cols = math.ceil(math.sqrt(len(entries)))
    return [
        Rect(
            name=p.name,
            is_dir=p.is_dir(),
            x=GAP + (i % cols) * (w + GAP),
            y=GAP + (i // cols) * (HEIGHT + GAP),
            w=w,
            h=HEIGHT,
        )
        for i, p in enumerate(entries)
    ]


def render_svg(root) -> str:
    """Return an SVG document drawing `root`'s top-level entries."""
    rects = layout(root)
    width = max((r.x + r.w for r in rects), default=0) + GAP
    height = max((r.y + r.h for r in rects), default=0) + GAP
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="monospace" font-size="14">'
    ]
    for r in rects:
        kind = "dir" if r.is_dir else "file"
        lines += [
            f'  <g class="{kind}">',
            f'    <rect x="{r.x}" y="{r.y}" width="{r.w}" height="{r.h}" '
            f'fill="none" stroke="black"/>',
            f'    <text x="{r.x + r.w / 2}" y="{r.y + r.h / 2}" text-anchor="middle" '
            f'dominant-baseline="middle">{escape(r.name)}</text>',
            "  </g>",
        ]
    lines.append("</svg>")
    return "\n".join(lines) + "\n"
