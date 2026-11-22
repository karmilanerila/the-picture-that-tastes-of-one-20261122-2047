#!/usr/bin/env python3
"""Picture that tastes of one ingredient -- round 2.

The entry is one photograph of a single ripe Alphonso mango slice:
orange flesh, juice beading on the cut face, warm side light, dark
background, nothing else in the frame. One ingredient, mango, shown so
you can almost taste it.

The photograph ships in this repository as ``mango.jpg``. This script
does one job: it checks that bundled file against the competition gate
and copies its bytes, unchanged, to the output path the grader reads
(``/output/entry.png`` by default, or ``$MAKEFUN_OUTPUT_DIR`` when
the harness sets it).

Only the Python standard library is used. There is no network, no
clock and no randomness anywhere, so every run writes exactly the
same bytes.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

PICTURE_FILE = "mango.jpg"
RESULT_FILE = "entry.png"
BYTE_CEILING = 1_048_576
SIDE_CEILING = 1024


@dataclass(frozen=True)
class Gate:
    """The competition's limits for the delivered image."""

    max_bytes: int = BYTE_CEILING
    max_side: int = SIDE_CEILING


@dataclass
class Picture:
    """A bundled JPEG plus the size the gate measured for it."""

    blob: bytes
    width: int
    height: int

    @property
    def nbytes(self) -> int:
        return len(self.blob)


def _sof_dimensions(blob: bytes) -> tuple[int, int]:
    """Pull (width, height) from a JPEG's first Start-Of-Frame segment.

    JPEG files are a chain of segments; each starts with 0xFF, a marker
    byte, then a big-endian length (except the freestanding markers,
    which carry no length). The SOF segment stores height then width
    as two big-endian 16-bit values after its precision byte.
    """
    if blob[:2] != b"\xff\xd8":
        raise ValueError("bundled picture is not a JPEG")
    cursor = 2
    end = len(blob)
    freestanding = {0x01, 0xD8} | set(range(0xD0, 0xD8))
    frame_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                     0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while cursor + 4 <= end:
        if blob[cursor] != 0xFF:
            raise ValueError("corrupt JPEG marker stream")
        code = blob[cursor + 1]
        if code == 0xFF:  # padding byte: step over it and keep looking
            cursor += 1
            continue
        if code in freestanding:
            cursor += 2
            continue
        seg_len = (blob[cursor + 2] << 8) | blob[cursor + 3]
        if code in frame_markers:
            tall = (blob[cursor + 5] << 8) | blob[cursor + 6]
            wide = (blob[cursor + 7] << 8) | blob[cursor + 8]
            return wide, tall
        cursor += 2 + seg_len
    raise ValueError("JPEG has no Start-Of-Frame segment")


def load_picture(folder: Path) -> Picture:
    """Read the bundled picture and measure it."""
    blob = (folder / PICTURE_FILE).read_bytes()
    wide, tall = _sof_dimensions(blob)
    return Picture(blob=blob, width=wide, height=tall)


def passes_gate(picture: Picture, gate: Gate) -> None:
    """Raise unless the picture fits every limit the gate sets."""
    if picture.nbytes == 0:
        raise ValueError("bundled picture is empty")
    if picture.nbytes > gate.max_bytes:
        raise ValueError(
            f"bundled picture is {picture.nbytes} bytes, "
            f"above the {gate.max_bytes} byte ceiling")
    if picture.width > gate.max_side or picture.height > gate.max_side:
        raise ValueError(
            f"bundled picture is {picture.width}x{picture.height}, "
            f"above the {gate.max_side}x{gate.max_side} ceiling")


def deliver(picture: Picture, outdir: Path) -> Path:
    """Write the picture bytes to the output file and read them back."""
    outdir.mkdir(parents=True, exist_ok=True)
    target = outdir / RESULT_FILE
    target.write_bytes(picture.blob)
    if target.read_bytes() != picture.blob:
        raise ValueError("output file does not match the bundled picture")
    return target


def run() -> int:
    folder = Path(__file__).resolve().parent
    outdir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    picture = load_picture(folder)
    passes_gate(picture, Gate())
    target = deliver(picture, outdir)
    print(f"picture: {PICTURE_FILE} {picture.width}x{picture.height} "
          f"{picture.nbytes} bytes -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
