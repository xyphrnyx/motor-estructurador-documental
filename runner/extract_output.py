\
#!/usr/bin/env python3
"""
Extrae el bloque JSON indexado de la salida dual del Motor.

Estrategia:
1) Busca bloques ```json ... ```.
2) Si no hay uno válido, usa JSONDecoder.raw_decode sobre cada "{".
3) Prefiere objetos que parezcan salida Beta6 (`schema_reference`, `metadata`,
   `sections`).
4) Escribe motor-output.json y motor-visual.md.

No corrige el JSON del modelo: o puede parsearse tal cual o la extracción falla.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FENCE_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.IGNORECASE | re.DOTALL)


def motor_likeness(value: Any) -> int:
    if not isinstance(value, dict):
        return 0
    keys = set(value)
    expected = {
        "schema_reference",
        "metadata",
        "classification",
        "processing_record",
        "sections",
        "authorship",
    }
    return len(keys & expected)


def fenced_candidates(text: str) -> list[tuple[int, int, dict[str, Any], str]]:
    out = []
    for m in FENCE_RE.finditer(text):
        raw = m.group(1)
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            out.append((m.start(), m.end(), value, raw))
    return out


def decoder_candidates(text: str) -> list[tuple[int, int, dict[str, Any], str]]:
    decoder = json.JSONDecoder()
    out = []
    for m in re.finditer(r"\{", text):
        start = m.start()
        try:
            value, size = decoder.raw_decode(text[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            raw = text[start:start + size]
            out.append((start, start + size, value, raw))
    return out


def choose_candidate(text: str) -> tuple[int, int, dict[str, Any], str, str]:
    fenced = fenced_candidates(text)
    candidates = fenced or decoder_candidates(text)
    if not candidates:
        raise ValueError("No se encontró un objeto JSON válido en la salida.")

    # Prioriza semejanza con el contrato; en empate, el objeto más largo.
    best = max(
        candidates,
        key=lambda item: (motor_likeness(item[2]), len(item[3])),
    )
    source = "fenced_json" if fenced else "raw_json"
    return (*best, source)


def extract_output_files(input_path: Path, output_dir: Path) -> dict[str, Any]:
    text = input_path.read_text(encoding="utf-8")
    start, end, value, raw, source = choose_candidate(text)

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "motor-output.json"
    visual_path = output_dir / "motor-visual.md"

    # Canonicaliza solo la representación del JSON extraído. El original completo
    # permanece intacto en motor-output.md.
    json_path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    visual = (text[:start] + text[end:]).strip()
    visual_path.write_text(visual + ("\n" if visual else ""), encoding="utf-8")

    return {
        "json_extracted": True,
        "extraction_method": source,
        "json_bytes": len(raw.encode("utf-8")),
        "visual_bytes": len(visual.encode("utf-8")),
        "json_filename": json_path.name,
        "visual_filename": visual_path.name,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--output-dir", required=True)
    args = p.parse_args()

    result = extract_output_files(Path(args.input), Path(args.output_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
