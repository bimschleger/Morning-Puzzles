#!/usr/bin/env python3
"""
Compresses portal.html with gzip and generates esp32-firmware/src/time/PortalHtml.h.
"""

import gzip
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_HTML_PATH = ROOT_DIR / "portal.html"
OUTPUT_HEADER_PATH = ROOT_DIR / "esp32-firmware" / "src" / "time" / "PortalHtml.h"


def build_portal_header() -> None:
    if not PORTAL_HTML_PATH.exists():
        raise FileNotFoundError(f"portal.html not found at {PORTAL_HTML_PATH}")

    raw_bytes = PORTAL_HTML_PATH.read_bytes()
    compressed = gzip.compress(raw_bytes, compresslevel=9, mtime=0)

    lines = []
    lines.append("// Automatically generated from portal.html by scripts/build_portal_header.py")
    lines.append("// Do not edit directly!")
    lines.append("#ifndef PORTAL_HTML_H")
    lines.append("#define PORTAL_HTML_H")
    lines.append("")
    lines.append("#include <Arduino.h>")
    lines.append("")
    lines.append(f"// Original size: {len(raw_bytes)} bytes | Compressed size: {len(compressed)} bytes")
    lines.append("static const uint8_t PORTAL_HTML_GZ[] PROGMEM = {")

    for i in range(0, len(compressed), 16):
        chunk = compressed[i : i + 16]
        hex_str = ", ".join(f"0x{b:02X}" for b in chunk)
        if i + 16 < len(compressed):
            lines.append(f"    {hex_str},")
        else:
            lines.append(f"    {hex_str}")

    lines.append("};")
    lines.append("")
    lines.append("#endif // PORTAL_HTML_H")
    lines.append("")

    OUTPUT_HEADER_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HEADER_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {OUTPUT_HEADER_PATH} ({len(compressed)} bytes compressed from {len(raw_bytes)} bytes).")


if __name__ == "__main__":
    build_portal_header()
