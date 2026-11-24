#!/usr/bin/env python3
"""make.fun bounty news-image-20261124: "Sum up 24 November's world news in
one image".

Ships the pre-built entry.png (1024x1024 PNG) beside this script to
$MAKEFUN_OUTPUT_DIR/entry.png, defaulting to /output/entry.png. The copy is
deterministic: no clock reads, no network, no randomness, so repeated runs
write byte-identical files. Standard library only.
"""

import os
import struct
import sys

SOURCE = "entry.png"
MAX_BYTES = 1048576
WANT_W = 1024
WANT_H = 1024
SIG = b"\x89PNG\r\n\x1a\n"


def validate_png(path):
    """Return None if path is an acceptable entry PNG, else a reason string.

    Checks size cap, PNG signature, the IHDR chunk (length 13, 8-bit depth,
    truecolour or truecolour+alpha), the 1024x1024 dimensions and a trailing
    IEND chunk.
    """
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as fh:
            head = fh.read(33)
            fh.seek(-12, os.SEEK_END)
            tail = fh.read(12)
    except OSError:
        return "source image is missing or unreadable"

    if size > MAX_BYTES:
        return "source image is over 1 MiB"
    if len(head) < 33 or head[:8] != SIG:
        return "source image is not a PNG"
    if head[8:12] != b"\x00\x00\x00\r" or head[12:16] != b"IHDR":
        return "source image has a malformed IHDR chunk"
    if head[24] != 8:
        return "source image is not 8 bits per channel"
    if head[25] not in (2, 6):
        return "source image is not truecolour"
    if struct.unpack(">II", head[16:24]) != (WANT_W, WANT_H):
        return "source image is not 1024x1024"
    if tail[4:8] != b"IEND":
        return "source image ends before its IEND chunk"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), SOURCE)

    err = validate_png(src)
    if err:
        sys.stderr.write("entry: " + err + "\n")
        return 1

    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        sys.stderr.write("entry: source image is over 1 MiB\n")
        return 1

    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())

    with open(dest, "rb") as fh:
        back = fh.read()
    if back != data:
        sys.stderr.write("entry: bytes read back from " + dest + " do not match\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
