\
#!/usr/bin/env python3
"""
Validador estructural local para salidas Beta6/Beta6.1.

IMPORTANTE:
- Valida estructura y coherencia mecánica.
- NO valida fidelidad semántica frente a la fuente.
- NO constituye validación externa del contenido por sí sola; es una herramienta
  real de validación estructural y su reporte puede conservarse como evidencia.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP = {
    "schema_reference",
    "metadata",
    "resource_status",
    "classification",
    "records_management",
    "processing_record",
    "title",
    "executive_summary",
    "sections",
    "authorship",
    "document_representation",
}

RECORD_FIELDS = {
    "source_document_id",
    "title",
    "creation_date",
    "classification",
    "author",
    "retention_period",
    "disposal_action",
}

ALLOWED_EXTERNAL_VALIDATION = {
    "not_executed",
    "passed",
    "failed",
    "error",
    "not_configured",
    "unavailable",
}

ALLOWED_SELF_CHECK = {"pass", "pass_with_warnings", "fail"}


class Checks:
    def __init__(self) -> None:
        self.items: list[dict[str, Any]] = []

    def add(self, name: str, ok: bool, note: str | None = None, severity: str = "error") -> None:
        self.items.append(
            {
                "name": name,
                "status": "pass" if ok else ("warning" if severity == "warning" else "fail"),
                "note": note,
            }
        )

    @property
    def failures(self) -> list[dict[str, Any]]:
        return [x for x in self.items if x["status"] == "fail"]

    @property
    def warnings(self) -> list[dict[str, Any]]:
        return [x for x in self.items if x["status"] == "warning"]


def nested(data: dict[str, Any], *keys: str) -> Any:
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def expected_confidence(score: Any) -> str | None:
    if score == 5:
        return "high"
    if score in (3, 4):
        return "medium"
    if score in (1, 2):
        return "low"
    if score == 0:
        return "none"
    return None


def validate(data: dict[str, Any]) -> dict[str, Any]:
    c = Checks()

    c.add("objeto_raiz", isinstance(data, dict))
    c.add(
        "campos_top_obligatorios",
        REQUIRED_TOP.issubset(data.keys()),
        f"faltan={sorted(REQUIRED_TOP - set(data.keys()))}" if REQUIRED_TOP - set(data.keys()) else None,
    )

    schema_version = nested(data, "schema_reference", "schema_version")
    c.add("schema_version_6_0_0", schema_version == "6.0.0", f"valor={schema_version!r}")

    schema_id = nested(data, "schema_reference", "schema_id")
    c.add("schema_id_presente", isinstance(schema_id, str) and bool(schema_id.strip()), f"valor={schema_id!r}")

    container = nested(data, "metadata", "output_container_type")
    c.add(
        "output_container_type",
        container == "structured_processing_output",
        f"valor={container!r}",
    )

    metadata_sid = nested(data, "metadata", "session_id")
    processing_sid = nested(data, "processing_record", "session_id")
    authorship_sid = nested(data, "authorship", "session_id")
    c.add(
        "session_id_sincronizado",
        bool(metadata_sid) and metadata_sid == processing_sid == authorship_sid,
        f"metadata={metadata_sid!r}, processing={processing_sid!r}, authorship={authorship_sid!r}",
    )

    metadata_date = nested(data, "metadata", "generated_at")
    authorship_date = nested(data, "authorship", "generated_at")
    c.add(
        "generated_at_sincronizado",
        bool(metadata_date) and metadata_date == authorship_date,
        f"metadata={metadata_date!r}, authorship={authorship_date!r}",
    )

    classification = data.get("classification")
    rubric = classification.get("rubric") if isinstance(classification, dict) else None
    score = classification.get("primary_score") if isinstance(classification, dict) else None
    if isinstance(rubric, dict):
        values = [
            rubric.get("purpose_alignment"),
            rubric.get("structural_evidence"),
            rubric.get("lexical_evidence"),
            rubric.get("artifact_evidence"),
        ]
        rubric_valid = all(isinstance(v, int) for v in values)
        rubric_sum = sum(values) if rubric_valid else None
    else:
        rubric_valid = False
        rubric_sum = None
    c.add(
        "rubrica_suma_primary_score",
        rubric_valid and rubric_sum == score,
        f"suma={rubric_sum!r}, primary_score={score!r}",
    )

    confidence = classification.get("confidence") if isinstance(classification, dict) else None
    expected = expected_confidence(score)
    c.add(
        "confidence_coherente",
        expected is not None and confidence == expected,
        f"score={score!r}, confidence={confidence!r}, esperado={expected!r}",
    )

    sections = data.get("sections")
    c.add("sections_no_vacio", isinstance(sections, list) and len(sections) > 0)
    if isinstance(sections, list):
        complete = all(
            isinstance(s, dict)
            and all(k in s for k in ("number", "section_id", "title", "content", "source_trace"))
            for s in sections
        )
        ids = [s.get("section_id") for s in sections if isinstance(s, dict)]
        unique = len(ids) == len(set(ids)) and all(isinstance(x, str) and x for x in ids)
        c.add("sections_completas", complete)
        c.add("section_ids_unicos", unique, f"{len(set(ids))}/{len(ids)} únicos")
    else:
        c.add("sections_completas", False)
        c.add("section_ids_unicos", False)

    fields = nested(data, "records_management", "fields")
    c.add(
        "records_management_7_campos",
        isinstance(fields, dict) and set(fields.keys()) == RECORD_FIELDS,
        f"campos={sorted(fields.keys()) if isinstance(fields, dict) else None}",
    )

    ext = nested(data, "resource_status", "external_validation", "status")
    c.add(
        "external_validation_status_valido",
        ext in ALLOWED_EXTERNAL_VALIDATION,
        f"valor={ext!r}",
    )

    self_status = nested(data, "processing_record", "self_check", "status")
    c.add(
        "self_check_status_valido",
        self_status in ALLOWED_SELF_CHECK,
        f"valor={self_status!r}",
    )

    internal_checks = nested(data, "processing_record", "self_check", "checks")
    internal_count = len(internal_checks) if isinstance(internal_checks, list) else 0
    c.add(
        "self_check_18_comprobaciones",
        internal_count >= 18,
        f"cantidad={internal_count}",
    )

    authorship_engine = nested(data, "authorship", "engine")
    c.add(
        "authorship_engine_presente",
        isinstance(authorship_engine, str) and bool(authorship_engine.strip()),
        f"valor={authorship_engine!r}",
    )

    full_text = nested(data, "document_representation", "full_text_included")
    full_doc = nested(data, "document_representation", "full_document_text")
    omission = nested(data, "document_representation", "omission_reason")
    representation_ok = (
        (full_text is True and isinstance(full_doc, str) and bool(full_doc.strip()))
        or (full_text is False and full_doc is None and isinstance(omission, str) and bool(omission.strip()))
    )
    c.add(
        "document_representation_coherente",
        representation_ok,
        f"full_text_included={full_text!r}",
    )

    # Advertencia, no fallo: el validador no puede establecer fidelidad semántica.
    c.add(
        "fidelidad_semantica",
        False,
        "No evaluada por este validador estructural; requiere contraste con la fuente.",
        severity="warning",
    )

    failed = len(c.failures)
    warnings = len(c.warnings)
    passed = len([x for x in c.items if x["status"] == "pass"])

    return {
        "validator": "beta6.1-structural-validator",
        "validator_version": "0.1.0",
        "status": "fail" if failed else ("pass_with_warnings" if warnings else "pass"),
        "summary": {
            "total": len(c.items),
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
        },
        "checks": c.items,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("json_file")
    p.add_argument("--report")
    args = p.parse_args()

    source = Path(args.json_file)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        report = {
            "validator": "beta6.1-structural-validator",
            "validator_version": "0.1.0",
            "status": "fail",
            "summary": {"total": 1, "passed": 0, "failed": 1, "warnings": 0},
            "checks": [
                {
                    "name": "json_sintacticamente_valido",
                    "status": "fail",
                    "note": f"{type(exc).__name__}: {exc}",
                }
            ],
        }
    else:
        report = validate(data)
        report["checks"].insert(
            0,
            {
                "name": "json_sintacticamente_valido",
                "status": "pass",
                "note": None,
            },
        )
        report["summary"]["total"] += 1
        report["summary"]["passed"] += 1

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)

    if args.report:
        Path(args.report).write_text(payload + "\n", encoding="utf-8")

    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
