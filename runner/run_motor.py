\
#!/usr/bin/env python3
"""
Ejecutor reproducible del Motor Estructurador Documental para GitHub Actions.

Lee:
  versions/<version>/prompt.md
  <source>

Envía el prompt como `instructions` y el documento delimitado por
<TEXTO_FUENTE>...</TEXTO_FUENTE> como `input` a OpenRouter Chat Completions API.

No modifica el prompt versionado.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from openai import OpenAI

from extract_output import extract_output_files

RUNNER_VERSION = "0.1.0"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def safe_repo_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"La ruta sale del repositorio: {relative}") from exc
    return candidate


def git_value(root: Path, *args: str) -> str | None:
    try:
        p = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        return p.stdout.strip() or None
    except Exception:
        return None


def sanitize(value: str, limit: int = 50) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return (value or "unknown")[:limit]


def write_github_output(name: str, value: str) -> None:
    target = os.environ.get("GITHUB_OUTPUT")
    if not target:
        return
    with open(target, "a", encoding="utf-8") as fh:
        fh.write(f"{name}={value}\n")


def serializable_usage(response: Any) -> dict[str, Any] | None:
    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    if hasattr(usage, "model_dump"):
        return usage.model_dump(mode="json")
    if isinstance(usage, dict):
        return usage
    return {"value": str(usage)}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--version", default="beta6.1")
    p.add_argument("--model", default=os.getenv("OPENROUTER_MODEL", "openrouter/free"))
    p.add_argument("--source", required=True)
    p.add_argument("--max-output-tokens", type=int, default=32000)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()

    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.version):
        raise SystemExit("Versión inválida.")
    if args.max_output_tokens < 16:
        raise SystemExit("--max-output-tokens debe ser >= 16.")

    prompt_path = safe_repo_path(root, f"versions/{args.version}/prompt.md")
    source_path = safe_repo_path(root, args.source)

    if not prompt_path.is_file():
        raise SystemExit(f"No existe el prompt: {prompt_path.relative_to(root)}")
    if not source_path.is_file():
        raise SystemExit(f"No existe la fuente: {source_path.relative_to(root)}")

    prompt_bytes = prompt_path.read_bytes()
    source_bytes = source_path.read_bytes()

    try:
        prompt = prompt_bytes.decode("utf-8")
        source = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(
            "Esta primera versión del runner acepta fuentes UTF-8 de texto. "
            "Convierte PDF/DOCX a texto antes de ejecutar."
        ) from exc

    now = dt.datetime.now(dt.timezone.utc)
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")
    sha = git_value(root, "rev-parse", "--short=7", "HEAD") or "nogit"
    run_name = (
        f"{timestamp}_{sanitize(args.version)}_{sanitize(args.model)}_{sanitize(sha)}"
    )
    run_dir = root / "runs" / run_name
    run_dir.mkdir(parents=True, exist_ok=False)

    # Publicamos la ruta cuanto antes para que el workflow pueda archivar
    # manifest/error aunque la llamada a la API falle.
    run_rel = run_dir.relative_to(root).as_posix()
    write_github_output("run_dir", run_rel)

    source_payload = f"<TEXTO_FUENTE>\n{source}\n</TEXTO_FUENTE>"

    manifest: dict[str, Any] = {
        "runner_version": RUNNER_VERSION,
        "status": "started",
        "started_at": now.isoformat(),
        "motor_version": args.version,
        "model_requested": args.model,
        "source_path": source_path.relative_to(root).as_posix(),
        "prompt_path": prompt_path.relative_to(root).as_posix(),
        "source_sha256": sha256_bytes(source_bytes),
        "prompt_sha256": sha256_bytes(prompt_bytes),
        "git_commit": git_value(root, "rev-parse", "HEAD"),
        "git_ref": os.getenv("GITHUB_REF"),
        "github_run_id": os.getenv("GITHUB_RUN_ID"),
        "github_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    client = OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )

    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "system",
                    "content": """<RUNTIME_OUTPUT_GUARD>
Cumple íntegramente la sección COMPROBACION_INTERNA_PREVIA del Motor.

processing_record.self_check.checks DEBE contener las 18 comprobaciones
individuales exigidas por Beta6.1, no un resumen ni una selección parcial.

Incluye una entrada separada para cada una de estas comprobaciones:

1. delimitación y existencia de la fuente
2. conservación de información útil
3. clasificación y suma de rúbrica
4. correspondencia score-confianza
5. activación correcta del fallback
6. separación entre fuente y contenedor
7. sincronización visual-JSON
8. estados tipados de metadatos ausentes
9. honestidad de recursos y validación externa
10. código y estados de ejecución, cuando aplique
11. generated_at y session_id coincidentes
12. JSON sintácticamente válido
13. ausencia de secretos evidentes no redactados
14. riesgo de truncamiento
15. contradicciones, cambios de versión y alternativas preservados correctamente
16. fuentes, referencias y activos separados de recursos internos del motor
17. source_trace sin referencias inventadas
18. índice estratégico-operativo activado u omitido según evidencia

No declares self_check.status="pass" si faltan comprobaciones.
No omitas comprobaciones aunque alguna resulte no aplicable; registra su estado
honestamente.
</RUNTIME_OUTPUT_GUARD>"""
                },
                {"role": "user", "content": source_payload},
            ],
            max_completion_tokens=args.max_output_tokens,
            extra_body={
                "reasoning": {
                    "enabled": False
                }
            },
        )

        output_text = response.choices[0].message.content or ""
        if not output_text.strip():
            raise RuntimeError("La API devolvió output_text vacío.")

        raw_output = run_dir / "motor-output.md"
        raw_output.write_text(output_text, encoding="utf-8")

        extraction = extract_output_files(raw_output, run_dir)

        finished = dt.datetime.now(dt.timezone.utc)
        manifest.update(
            {
                "status": "completed",
                "finished_at": finished.isoformat(),
                "api_response_id": getattr(response, "id", None),
                "api_status": getattr(response, "status", None),
                "model_resolved": getattr(response, "model", None),
                "usage": serializable_usage(response),
                "extraction": extraction,
            }
        )
        (run_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        print(f"RUN_DIR={run_rel}")
        print(f"OUTPUT={raw_output.relative_to(root)}")
        print(f"JSON={run_dir.relative_to(root) / 'motor-output.json'}")
        return 0

    except Exception as exc:
        manifest.update(
            {
                "status": "failed",
                "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        )
        (run_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
