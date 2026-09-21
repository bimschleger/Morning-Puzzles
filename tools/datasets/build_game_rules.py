#!/usr/bin/env python3
"""
Morning Puzzles - Unified Game Rules & Guide Compiler Pipeline
Reads canonical JSON from server/data/game_rules.json and:
1. Generates esp32-firmware/src/generators/GameRulesDataset.h
2. Generates docs/GAME_RULES_FAQ.md
3. Injects canonical game rules into portal.html and builds PortalHtml.h
4. Injects canonical game rules into simulator/receipt_simulator.html
5. Synchronizes Arduino IDE sketch via scripts/sync_arduino_sketch.sh
"""

import gzip
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RULES_JSON_PATH = ROOT_DIR / "server" / "data" / "game_rules.json"
GAME_RULES_H_PATH = ROOT_DIR / "esp32-firmware" / "src" / "generators" / "GameRulesDataset.h"
DOCS_MD_PATH = ROOT_DIR / "docs" / "GAME_RULES_FAQ.md"
PORTAL_HTML_PATH = ROOT_DIR / "portal.html"
PORTAL_HEADER_PATH = ROOT_DIR / "esp32-firmware" / "src" / "time" / "PortalHtml.h"
SIMULATOR_HTML_PATH = ROOT_DIR / "simulator" / "receipt_simulator.html"
SYNC_SCRIPT = ROOT_DIR / "scripts" / "sync_arduino_sketch.sh"


def escape_cpp_string(s: str) -> str:
    """Escapes quotes and backslashes for C++ string literals."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def generate_cpp_header(data: dict) -> None:
    print(f"Generating C++ GameRulesDataset.h -> {GAME_RULES_H_PATH}...")
    games = data.get("games", [])
    lines = [
        "// Automatically generated from server/data/game_rules.json by tools/datasets/build_game_rules.py",
        "// Do not edit directly!",
        "#ifndef GAME_RULES_DATASET_H",
        "#define GAME_RULES_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "struct GameFaqItem {",
        "    const char* question;",
        "    const char* answer;",
        "};",
        "",
        "struct GameRuleDef {",
        "    uint8_t id;",
        "    const char* key;",
        "    const char* title;",
        "    const char* instruction;",
        "    const char* objective;",
        "    const char* rules[4];",
        "    uint8_t ruleCount;",
        "    const char* validCaption;",
        "    const char* invalidCaption;",
        "    const char* openingAnchors[2];",
        "    uint8_t anchorCount;",
        "    GameFaqItem faq[2];",
        "    uint8_t faqCount;",
        "};",
        "",
        f"static const size_t TOTAL_GAME_RULES = {len(games)};",
        "static const GameRuleDef GAME_RULES[TOTAL_GAME_RULES] PROGMEM = {",
    ]

    for g in games:
        rules_strs = [f'"{escape_cpp_string(r)}"' for r in g.get("rules", [])[:4]]
        rule_count = len(rules_strs)
        while len(rules_strs) < 4:
            rules_strs.append('""')

        anchors = [f'"{escape_cpp_string(a)}"' for a in g.get("opening_anchors", [])[:2]]
        anchor_count = len(anchors)
        while len(anchors) < 2:
            anchors.append('""')

        faqs = g.get("faq", [])[:2]
        faq_count = len(faqs)
        faq_strs = []
        for item in faqs:
            q = escape_cpp_string(item.get("q", ""))
            a = escape_cpp_string(item.get("a", ""))
            faq_strs.append(f'{{"{q}", "{a}"}}')
        while len(faq_strs) < 2:
            faq_strs.append('{"", ""}')

        lines.append("    {")
        lines.append(f'        {g["id"]},')
        lines.append(f'        "{escape_cpp_string(g["key"]) }",')
        lines.append(f'        "{escape_cpp_string(g["title"]) }",')
        lines.append(f'        "{escape_cpp_string(g["instruction"]) }",')
        lines.append(f'        "{escape_cpp_string(g["objective"]) }",')
        lines.append(f'        {{ {", ".join(rules_strs)} }},')
        lines.append(f"        {rule_count},")
        lines.append(f'        "{escape_cpp_string(g.get("valid_move", {}).get("caption", "")) }",')
        lines.append(f'        "{escape_cpp_string(g.get("invalid_move", {}).get("caption", "")) }",')
        lines.append(f'        {{ {", ".join(anchors)} }},')
        lines.append(f"        {anchor_count},")
        lines.append(f'        {{ {", ".join(faq_strs)} }},')
        lines.append(f"        {faq_count}")
        lines.append("    },")

    lines.append("};")
    lines.append("")
    lines.append("inline const GameRuleDef* getGameRuleDefById(uint8_t id) {")
    lines.append("    for (size_t i = 0; i < TOTAL_GAME_RULES; i++) {")
    lines.append("        if (pgm_read_byte(&(GAME_RULES[i].id)) == id) {")
    lines.append("            return &GAME_RULES[i];")
    lines.append("        }")
    lines.append("    }")
    lines.append("    return nullptr;")
    lines.append("}")
    lines.append("")
    lines.append("#endif // GAME_RULES_DATASET_H")
    lines.append("")

    GAME_RULES_H_PATH.parent.mkdir(parents=True, exist_ok=True)
    GAME_RULES_H_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Successfully wrote {GAME_RULES_H_PATH}")


def generate_markdown_docs(data: dict) -> None:
    print(f"Generating Markdown Docs -> {DOCS_MD_PATH}...")
    games = data.get("games", [])
    lines = [
        "# Morning Puzzles: Comprehensive Game Rules & How-to-Play Guide",
        "",
        "This authoritative guide contains complete rules, core objectives, opening deduction anchors, and visual move specifications for all 18 games in Morning Puzzles.",
        "",
        "---",
        "",
        "## Table of Contents",
        "",
    ]
    for g in games:
        lines.append(f"- [{g['title']}](#{g['key']}) - {g['instruction']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for g in games:
        lines.append(f"<a name=\"{g['key']}\"></a>")
        lines.append(f"## --- {g['title']} ---")
        lines.append("")
        lines.append(f"> **Instruction**: `{g['instruction']}`")
        lines.append("")
        lines.append(f"**Objective**: {g['objective']}")
        lines.append("")
        lines.append("### Rules of Play")
        for r in g.get("rules", []):
            lines.append(f"- {r}")
        lines.append("")

        lines.append("### Move Examples")
        lines.append("")
        lines.append(f"**Valid Move**: {g.get('valid_move', {}).get('caption', '')}")
        v_grid = g.get('valid_move', {}).get('grid', [])
        if v_grid:
            lines.append("```text")
            for row in v_grid:
                lines.append("  " + " ".join(row))
            lines.append("```")
        lines.append("")

        lines.append(f"**Invalid Move**: {g.get('invalid_move', {}).get('caption', '')}")
        iv_grid = g.get('invalid_move', {}).get('grid', [])
        if iv_grid:
            lines.append("```text")
            for row in iv_grid:
                lines.append("  " + " ".join(row))
            lines.append("```")
        lines.append("")

        lines.append("### Where to Start (First Deductions)")
        for a in g.get("opening_anchors", []):
            lines.append(f"- **Tip**: {a}")
        lines.append("")

        lines.append("### Frequently Asked Questions")
        for item in g.get("faq", []):
            lines.append(f"- **Q: {item['q']}**")
            lines.append(f"  *A: {item['a']}*")
        lines.append("")
        lines.append("---")
        lines.append("")

    DOCS_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOCS_MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Successfully wrote {DOCS_MD_PATH}")


def inject_portal_html(data: dict) -> None:
    if not PORTAL_HTML_PATH.exists():
        raise FileNotFoundError(f"portal.html not found at {PORTAL_HTML_PATH}")

    content = PORTAL_HTML_PATH.read_text(encoding="utf-8")
    games_json = json.dumps(data.get("games", []), indent=2)
    start_tag = "/* [[START_GAME_RULES_DATA]] */"
    end_tag = "/* [[END_GAME_RULES_DATA]] */"
    rules_block = f"{start_tag}\nconst GAME_RULES = {games_json};\n{end_tag}"

    if start_tag in content and end_tag in content:
        start_idx = content.find(start_tag)
        end_idx = content.find(end_tag) + len(end_tag)
        content = content[:start_idx] + rules_block + content[end_idx:]
    elif "const GAME_RULES = [" in content:
        start_idx = content.find("const GAME_RULES = [")
        end_marker = "let currentMask ="
        end_idx = content.find(end_marker)
        if end_idx != -1:
            content = content[:start_idx] + rules_block + "\n\n" + content[end_idx:]
    elif "/* [[GAME_RULES_DATA]] */" in content:
        content = content.replace("/* [[GAME_RULES_DATA]] */", rules_block)

    PORTAL_HTML_PATH.write_text(content, encoding="utf-8")
    print(f"  Injected canonical GAME_RULES into {PORTAL_HTML_PATH}")


def inject_simulator_html(data: dict) -> None:
    if not SIMULATOR_HTML_PATH.exists():
        print(f"  Simulator HTML not found at {SIMULATOR_HTML_PATH}, skipping.")
        return

    content = SIMULATOR_HTML_PATH.read_text(encoding="utf-8")
    games_json = json.dumps(data.get("games", []), indent=2)
    start_tag = "/* [[START_GAME_RULES_DATA]] */"
    end_tag = "/* [[END_GAME_RULES_DATA]] */"
    rules_block = f"{start_tag}\n    const GAME_RULES = {games_json};\n    {end_tag}"

    if start_tag in content and end_tag in content:
        start_idx = content.find(start_tag)
        end_idx = content.find(end_tag) + len(end_tag)
        content = content[:start_idx] + rules_block + content[end_idx:]
        SIMULATOR_HTML_PATH.write_text(content, encoding="utf-8")
        print(f"  Injected canonical GAME_RULES into {SIMULATOR_HTML_PATH}")
    else:
        print("  Warning: markers not found in simulator HTML, skipping.")


def build_portal_header() -> None:
    if not PORTAL_HTML_PATH.exists():
        raise FileNotFoundError(f"portal.html not found at {PORTAL_HTML_PATH}")

    raw_bytes = PORTAL_HTML_PATH.read_bytes()
    compressed = gzip.compress(raw_bytes, compresslevel=9, mtime=0)

    lines = [
        "// Automatically generated from portal.html by tools/datasets/build_game_rules.py",
        "// Do not edit directly!",
        "#ifndef PORTAL_HTML_H",
        "#define PORTAL_HTML_H",
        "",
        "#include <Arduino.h>",
        "",
        f"// Original size: {len(raw_bytes)} bytes | Compressed size: {len(compressed)} bytes",
        "static const uint8_t PORTAL_HTML_GZ[] PROGMEM = {",
    ]

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

    PORTAL_HEADER_PATH.parent.mkdir(parents=True, exist_ok=True)
    PORTAL_HEADER_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Generated {PORTAL_HEADER_PATH} ({len(compressed)} bytes compressed from {len(raw_bytes)} bytes).")


def sync_arduino() -> None:
    if SYNC_SCRIPT.exists() and os.access(SYNC_SCRIPT, os.X_OK):
        print("Running sync_arduino_sketch.sh...")
        res = subprocess.run([str(SYNC_SCRIPT)], capture_output=True, text=True)
        if res.returncode == 0:
            print("  Arduino sketch synchronized successfully.")
        else:
            print(f"  Warning: sync_arduino_sketch.sh returned {res.returncode}: {res.stderr}")


def main() -> None:
    if not RULES_JSON_PATH.exists():
        raise FileNotFoundError(f"Rules JSON not found at {RULES_JSON_PATH}")

    with open(RULES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    generate_cpp_header(data)
    generate_markdown_docs(data)
    inject_portal_html(data)
    build_portal_header()
    inject_simulator_html(data)
    sync_arduino()
    print("Game rules compiler pipeline completed successfully!")


if __name__ == "__main__":
    main()

