# GitHub Actions — instalación del runner del Motor

Este paquete es un **overlay** para el repositorio existente:

`xyphrnyx/motor-estructurador-documental`

No reemplaza `versions/` ni modifica `versions/beta6.1/prompt.md`.

## Archivos añadidos

```text
.github/workflows/run-motor.yml
runner/run_motor.py
runner/extract_output.py
runner/validate_output.py
requirements.txt
test-corpus/README.md
test-corpus/technical/hello-motor.txt
```

## 1. Copiar el overlay

Descomprime el ZIP en la raíz del repositorio, de forma que `.github/`,
`runner/`, `test-corpus/` y `requirements.txt` queden al mismo nivel que
`versions/`, `evals/`, `CHANGELOG.md` y `README.md`.

## 2. Configurar la API key

En GitHub:

1. Abre el repositorio.
2. `Settings`.
3. `Secrets and variables`.
4. `Actions`.
5. Crea un repository secret llamado exactamente `OPENAI_API_KEY`.

No escribas la clave en el YAML, en `requirements.txt`, en el corpus ni en
ningún archivo versionado.

## 3. Commit y push

Ejemplo:

```bash
git add .github runner test-corpus requirements.txt GITHUB_ACTIONS_SETUP.md
git commit -m "feat(actions): añadir runner reproducible del motor"
git push origin main
```

## 4. Ejecutar desde la interfaz

1. Abre `Actions`.
2. Selecciona `Ejecutar Motor Estructurador`.
3. Pulsa `Run workflow`.
4. Valores iniciales recomendados:
   - version: `beta6.1`
   - model: `gpt-6-astra`
   - source: `test-corpus/technical/hello-motor.txt`
   - max_output_tokens: `32000`
   - fail_on_validation: activado
5. Ejecuta el workflow.

El workflow usa el archivo existente:

`versions/beta6.1/prompt.md`

como `instructions` de la Responses API y envuelve la fuente en:

```text
<TEXTO_FUENTE>
...
</TEXTO_FUENTE>
```

## 5. Resultados

Cada ejecución crea un directorio efímero:

```text
runs/YYYYMMDDTHHMMSSZ_beta6.1_MODELO_COMMIT/
├── manifest.json
├── motor-output.md
├── motor-output.json
├── motor-visual.md
└── validation.json
```

El directorio `runs/` se sube como GitHub Actions artifact. No se hace commit
automático de los resultados.

### Significado

- `manifest.json`: versión, modelo, commit y hashes SHA-256 del prompt/fuente.
- `motor-output.md`: respuesta completa original del modelo.
- `motor-output.json`: objeto JSON extraído sin inventar reparaciones.
- `motor-visual.md`: parte visual con el bloque JSON extraído retirado.
- `validation.json`: comprobaciones estructurales.

## 6. Qué valida y qué NO valida

`runner/validate_output.py` comprueba de forma mecánica, entre otras cosas:

- JSON válido;
- schema 6.0.0;
- `schema_id` presente;
- `output_container_type`;
- `session_id` sincronizado;
- `generated_at` sincronizado;
- suma de la rúbrica;
- correspondencia score/confidence;
- `sections` completas y con IDs únicos;
- siete campos de `records_management`;
- estado de validación externa;
- `self_check`;
- representación documental.

**No demuestra fidelidad semántica frente al documento fuente.**
Ese control debe permanecer separado, mediante auditoría humana o una fase
específica de evaluación.

## 7. Seguridad y privacidad

El repositorio indicado es público. Esta primera versión del workflow está
diseñada para procesar archivos presentes dentro del repositorio, por lo que
debe utilizarse solo con corpus público/sintético/anonimizado.

No subas documentos privados al repositorio para poder procesarlos.

Para fuentes privadas, una siguiente fase debería usar una de estas
arquitecturas:

- repositorio privado;
- runner self-hosted;
- almacenamiento privado temporal;
- interfaz de carga separada que invoque `repository_dispatch`.

## 8. Modelo

El modelo es un input editable del workflow. El valor inicial es
`gpt-6-astra`; cámbialo en la interfaz si tu proyecto/API tiene acceso a otro
modelo compatible con Responses API.

## 9. Limitación inicial de formatos

El runner inicial acepta fuentes de texto UTF-8. El soporte PDF/DOCX no está
incluido en este overlay para no introducir extracción documental ambigua ni
dependencias adicionales en la primera prueba.

## 10. Rollback

Todos los archivos de este paquete son aditivos respecto al repositorio
observado. Para retirar la integración:

```bash
git rm -r .github/workflows/run-motor.yml runner test-corpus
git rm requirements.txt GITHUB_ACTIONS_SETUP.md
git commit -m "revert(actions): retirar runner del motor"
```

Esto no toca las carpetas históricas de `versions/`.
