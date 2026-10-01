Motor Estructurador Documental
Repositorio de versionado, ejecución y evaluación del Motor de Procesamiento Estructural No Conversacional
---
📖 Descripción
Este repositorio contiene el historial completo de versiones del Motor Estructurador Documental, un sistema de instrucciones diseñado para transformar texto fuente en documentos estructurados con salida dual: Markdown visual y JSON indexado.
Desarrollado por Xyphrnyx, el motor ha evolucionado desde una plantilla de estructuración hasta un sistema con clasificación documental, trazabilidad, protección anti-inyección, protocolos especializados para scripts y una primera capa de ejecución reproducible mediante GitHub Actions.
Las versiones del motor permanecen separadas de la infraestructura de ejecución:
`versions/` contiene los prompts versionados.
`runner/` contiene la capa de ejecución y validación.
`test-corpus/` contiene documentos sintéticos o públicos para pruebas.
`.github/workflows/` contiene la automatización de GitHub Actions.
`evals/` contiene recursos para evaluación.
---
🗺️ Línea de tiempo de versiones
<!-- VERSIONES_INICIO -->
Versión	Fecha	Tema central
v0.0.0	—	Documento único, sin trazabilidad
beta2	2026-05-23	Salida dual + trazabilidad + auditoría
beta3	2026-05-23	(fantasma) Resumen ejecutivo BLUF
beta4	2026-05-23	Historial de versiones interno
beta5	2026-05-23	Clasificación automática + ISO 15489
beta6	2026-07-28	Honestidad operativa + anti-inyección + protocolo para scripts
beta6.1	2026-09-12	Actualización de autoría (Xyphrnyx)
<!-- VERSIONES_FIN -->
> **Nota:** beta3 no se recibió como archivo independiente; solo existe referenciado en los historiales de beta4 y beta5. Se documenta como versión "fantasma".
---
🚀 Cómo usar este repositorio
Ver una versión específica
```bash
git checkout v0.0.0
# o, por ejemplo:
git checkout beta6.1
```
Comparar dos versiones
```bash
git diff beta4 beta5
```
Probar una versión manualmente
Copia el contenido de `prompt.md` de la versión deseada y úsalo como instrucción principal en el asistente o modelo correspondiente.
El documento fuente debe suministrarse dentro del contenedor esperado por el motor:
```text
<TEXTO_FUENTE>
[contenido del documento]
</TEXTO_FUENTE>
```
---
⚙️ Ejecución automatizada con GitHub Actions
El repositorio incluye una primera capa de ejecución automatizada para probar una versión del motor desde GitHub Actions sin modificar el prompt versionado.
Flujo actual:
```text
GitHub Actions
      ↓
runner/run_motor.py
      ↓
versions/beta6.1/prompt.md
      ↓
API del modelo
      ↓
salida Markdown
      ↓
extracción JSON
      ↓
validación estructural
      ↓
artifact de la ejecución
```
Archivos principales
`.github/workflows/run-motor.yml` — workflow manual de GitHub Actions.
`runner/run_motor.py` — carga el prompt y el documento fuente y ejecuta el modelo.
`runner/extract_output.py` — extrae el bloque JSON de la respuesta.
`runner/validate_output.py` — realiza validaciones estructurales sobre la salida.
`requirements.txt` — dependencias de Python del runner.
`test-corpus/technical/hello-motor.txt` — documento sintético para la prueba inicial.
`GITHUB_ACTIONS_SETUP.md` — guía de configuración de GitHub Actions.
Ejecutar el workflow
En GitHub:
Abre la pestaña Actions.
Selecciona Ejecutar Motor Estructurador.
Pulsa Run workflow.
Selecciona o confirma la versión, el modelo y el documento de prueba.
Ejecuta el workflow.
Al finalizar, descarga el artifact generado para revisar los resultados.
Para usar el proveedor configurado actualmente en esta primera capa se requiere el secret de repositorio:
```text
OPENAI_API_KEY
```
La clave debe guardarse en GitHub → Settings → Secrets and variables → Actions. No debe escribirse dentro del repositorio.
---
🧪 Prueba inicial recomendada
La prueba base usa:
```text
Versión: beta6.1
Fuente: test-corpus/technical/hello-motor.txt
Validación estructural: activada
```
Cuando la ejecución completa correctamente el pipeline, el artifact puede contener:
```text
manifest.json
motor-output.md
motor-output.json
motor-visual.md
validation.json
```
La presencia exacta de los archivos depende de hasta qué punto complete la ejecución.
---
✅ Alcance actual de la automatización
Esta primera capa:
lee `versions/<version>/prompt.md`;
lee una fuente de texto incluida en el repositorio;
envuelve la fuente en `<TEXTO_FUENTE>...</TEXTO_FUENTE>`;
ejecuta el modelo mediante el runner;
guarda la respuesta;
extrae el JSON cuando es posible;
ejecuta validación estructural;
publica los resultados como artifact de GitHub Actions.
La automatización no modifica `versions/beta6.1/prompt.md`.
---
⚠️ Limitaciones actuales
Esta fase todavía no:
porta a GitHub Actions el `motor-manager.sh` completo;
replica sus backups locales ni su historial persistente;
replica automáticamente todo el sistema de versionado SemVer;
integra todos los proveedores externos disponibles en el gestor local;
integra el auditor completo ni el dashboard histórico;
ejecuta una suite de regresión multiproveedor;
actualiza automáticamente este `README.md`;
hace commits automáticos de resultados;
procesa directamente PDF o DOCX en el runner actual;
sustituye la evaluación humana de fidelidad semántica.
La validación existente es principalmente estructural. Una salida puede cumplir el contrato técnico y aun requerir revisión humana sobre fidelidad, interpretación y calidad documental.
---
🔒 Documentos de prueba y privacidad
Este repositorio es público.
Por ello, `test-corpus/` debe contener únicamente documentos:
sintéticos;
anonimizados;
públicos;
o preparados específicamente para regresión.
No deben incorporarse documentos privados, secretos, credenciales ni información sensible al historial Git.
---
📂 Estructura del repositorio
```text
/
├── .github/
│   └── workflows/
│       └── run-motor.yml
├── versions/
│   ├── v0.0.0/
│   ├── beta2/
│   ├── beta3-ghost/
│   ├── beta4/
│   ├── beta5/
│   ├── beta6/
│   └── beta6.1/
├── runner/
│   ├── run_motor.py
│   ├── extract_output.py
│   └── validate_output.py
├── test-corpus/
│   ├── README.md
│   └── technical/
│       └── hello-motor.txt
├── evals/
│   └── metricas-template.md
├── related-tools/
├── GITHUB_ACTIONS_SETUP.md
├── requirements.txt
├── CHANGELOG.md
├── README.md
└── LICENSE
```
---
📋 Registro de cambios
Consulta `CHANGELOG.md` para el detalle de las transiciones entre versiones del motor.
Los cambios de infraestructura —por ejemplo, runners, workflows o documentación— pueden registrarse mediante commits separados sin alterar una versión histórica del prompt.
---
🧪 Pruebas y evaluación
La carpeta `evals/` contiene recursos para registrar métricas y resultados de pruebas.
La incorporación de `runner/`, `test-corpus/` y GitHub Actions permite avanzar hacia pruebas reproducibles y futuras suites de regresión sin mezclar la infraestructura con los prompts versionados.
---
📄 Licencia y autoría
© 2026 Xyphrnyx. Todos los derechos reservados.
El motor y sus versiones son propiedad intelectual de su autor. Este repositorio es público con fines de documentación, trazabilidad y evaluación del proyecto.
Este repositorio es personal y no se aceptan contribuciones externas. Si encuentras un error en la documentación, puedes abrir un issue.
---
Última actualización
2026-09-30 — Añadida la primera capa de ejecución automatizada con GitHub Actions.
