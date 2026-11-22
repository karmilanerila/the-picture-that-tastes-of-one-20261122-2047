"""The picture that tastes of one ingredient.

Writes one image to /output/entry.png: a macro close-up of golden
honeycomb dripping warm honey -- a single ingredient, honey, shown at
its most appetising: gloss, drip, warm light, nothing else in frame.

The picture is bundled with this program as honeycomb.jpg (a 1024x1024
JPEG, 257,995 bytes, well inside the 1 MiB gate). This program copies
those exact bytes to /output/entry.png, after verifying the bundled
asset itself: it parses the JPEG header to confirm the dimensions and
checks the byte size against the competition limits, so a damaged or
oversized asset fails loudly instead of producing a bad entry.

Standard library only. No network, no randomness, no clock: run it
twice and the output is byte-identical.
"""

import hashlib
import os
import struct
import sys

ASSET_NAME = "honeycomb.jpg"
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")
OUTPUT_NAME = "entry.png"

MAX_BYTES = 1_048_576
MAX_WIDTH = 1024
MAX_HEIGHT = 1024


def asset_path() -> str:
    """Path of the bundled picture, next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, ASSET_NAME)


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Read width and height out of a JPEG's SOF marker, stdlib only.

    Walks the marker segments from the SOI marker until it finds a
    Start-Of-Frame segment (baseline or progressive) and reads the
    height and width stored there, big-endian, 16 bits each.
    """
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        raise ValueError("asset is not a JPEG (missing SOI marker)")
    pos = 2
    while pos + 9 <= len(data):
        if data[pos] != 0xFF:
            raise ValueError(f"bad marker prefix at offset {pos}")
        marker = data[pos + 1]
        # Standalone markers carry no length field; skip past them.
        if marker in (0x01, 0xD0, 0xD1, 0xD2, 0xD3,
                      0xD4, 0xD5, 0xD6, 0xD7, 0xD8):
            pos += 2
            continue
        (length,) = struct.unpack(">H", data[pos + 2:pos + 4])
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + length
    raise ValueError("no SOF marker found in JPEG")


def check_asset(data: bytes) -> tuple[int, int]:
    """Enforce the competition gate on the bundled bytes before writing."""
    if len(data) == 0:
        raise ValueError("bundled asset is empty")
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"bundled asset is {len(data)} bytes, over the "
            f"{MAX_BYTES} byte limit")
    width, height = jpeg_dimensions(data)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise ValueError(
            f"bundled asset is {width}x{height}, over the "
            f"{MAX_WIDTH}x{MAX_HEIGHT} limit")
    return width, height


def main() -> int:
    path = asset_path()
    with open(path, "rb") as handle:
        data = handle.read()

    width, height = check_asset(data)
    digest = hashlib.sha256(data).hexdigest()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    with open(out_path, "wb") as handle:
        handle.write(data)

    # Read the output back and prove it is exactly the verified asset:
    # a short write, a disk hiccup or a stray byte must fail here,
    # never silently ship a different picture to the judge.
    with open(out_path, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).hexdigest() != digest:
        raise ValueError("output differs from the verified asset")
    if len(written) > MAX_BYTES:
        raise ValueError("output exceeds the 1 MiB limit")

    print(f"asset: {ASSET_NAME} ({width}x{height}, {len(data)} bytes)")
    print(f"sha256: {digest}")
    print(f"wrote: {out_path} (verified identical)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
