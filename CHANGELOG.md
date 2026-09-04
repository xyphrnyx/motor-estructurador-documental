# Historial de cambios del Motor Estructurador Documental

Este documento registra la evolución del prompt entre versiones, basado en el análisis detallado de los artefactos recibidos.

---

## [beta6] - 2026-07-28

### Cambios principales (reescritura casi completa)

**Retractaciones y honestidad operativa:**
- Se elimina la afirmación de conformidad ISO 15489. Ahora se usa un perfil interno de gestión documental sin declarar certificación.
- Se reemplaza el fetch obligatorio por tres modos de operación honestos: `standalone_prompt`, `integrated_resources`, `external_validation`.
- Se prohíbe explícitamente simular acceso o validación externa sin evidencia real.

**Nuevas protecciones:**
- `<CONTRATO_DE_ENTRADA_Y_PROTECCION>`: blindaje anti-inyección — el contenido de `TEXTO_FUENTE` se trata como dato inerte.
- `<TRATAMIENTO_DE_EVIDENCIA_PRIVACIDAD_Y_EJEMPLOS>`: tres modos de privacidad configurables y 8 categorías de contenido.

**Clasificación reproducible:**
- Rúbrica de 4 componentes: `purpose_alignment`, `structural_evidence`, `lexical_evidence`, `artifact_evidence`.
- Score de 0 a 5 con conversión a confianza (high/medium/low/none).

**Tipos documentales ampliados (de 7 a 9):**
- Nuevos: `script_workflow_document`, `conversation_transcript`, `previous_motor_output`.
- Desaparece `motor_procesamiento`.

**Protocolo especial para scripts y aprendizaje técnico:**
- 11 puntos: preservación de código, entornos, estados de ejecución, iteraciones, errores, procedimiento canónico, mapa de archivos, dependencias, privilegios/riesgos, rollback, salida estratégica.
- Recupera y formaliza la única línea de v0.0.0 sobre "transcribir código con integridad".

**Nuevos bloques:**
- `<PROTOCOLO_DE_COHERENCIA_CONFLICTOS_Y_EVOLUCION>`: rastreo de contradicciones y cambios de versión.
- `<PROTOCOLO_DE_TRAZABILIDAD_DE_FUENTE>`: contra inventar referencias.
- `<FUENTES_REFERENCIAS_Y_ACTIVOS>`: catálogo de archivos/URLs del usuario.
- `<INDICE_ESTRATEGICO_OPERATIVO_OPCIONAL>`: vista compacta de 11 campos.
- `<PLANTILLAS_DEL_CUERPO>`: required/optional por cada tipo.
- `<COMPROBACION_INTERNA_PREVIA>`: self-check de 18 puntos.
- `<CONTROL_DE_TAMANO_Y_REPRESENTACION_COMPLETA>`: permite `full_document_text=null` para evitar truncamiento.

**JSON reestructurado:**
- Anidamiento de `schema_reference`, `resource_status`, `classification.rubric`, `records_management` (campos tipados `{value, status, provenance, reason}`), `processing_record.self_check`, `sections[].source_trace`, y objeto `script_workflow` completo.

**Restricciones duras**: se triplican (de ~15 a más de 20).

---

## [beta5] - 2026-05-23

### Cambios principales

- **Clasificación documental automatizada**: procedimiento de 5 pasos, confidence score 0–5, 7 tipos soportados.
- **Manejo de híbridos**: protocolo de fallback con 5 pasos y sufijo visible `__from_[tipo_secundario]`.
- **Anti-invención explícita**: "PROHIBIDO inventar, simular o inferir datos... rellenar con la constante de omisión".
- **Metadatos normativos**: `iso15489_metadata` con 7 campos (document_id, title, creation_date, classification, author, retention_period, disposal_action).
- **Recursos externos**: de 1 URL a 5 URLs (schema_library, template_registry, fallback_protocol, iso_validator).
- **JSON**: añade `document_type`, `classification_confidence`, `decision_record` anidado.
- **Ficha visual**: línea `**🏷️ Tipo documental:** [tipo] | **Confianza:** [nivel]` bajo el título.

---

## [beta4] - 2026-05-23

### Cambios principales

- **Autodocumentación interna**: aparece por primera vez `<HISTORIAL_VERSIONES>` dentro de `<METADATOS>`, documentando retroactivamente beta2, beta3 y beta4.
- Estructura idéntica a beta2 en lo demás: mismas 9 secciones, misma configuración de 2 parámetros, sin clasificación documental ni fallback.

---

## [beta3] - 2026-05-23 *(fantasma, sin archivo propio)*

### Cambios declarados (inferidos desde beta4/beta5)

- Se incorporan directrices estrictas para el resumen ejecutivo: **autonomía** (standalone), **BLUF** (Bottom Line Up Front), **concisión extrema** (máx. 2 párrafos), claridad y **fidelidad absoluta**.
- Se añade la sección `DIRECTRICES_RESUMEN_EJECUTIVO` dentro de la topología de salida.
- Se añade una restricción dura que obliga a cumplirlas.

> No se recibió el archivo de beta3 como artefacto independiente. Solo existe referenciado dentro del historial de beta4 y beta5.

---

## [beta2] - 2026-05-23

### Cambios principales (respecto a v0.0.0)

- **Autoidentificación**: `<METADATOS><version>beta2</version>`.
- **Salida dual**: documento visual + bloque JSON indexado.
- **Fetch inicial**: `<INSTRUCCION_INICIAL>` obliga a obtener un schema JSON externo antes de procesar.
- **Configuración**: `audit_mode`, `external_schema_url`.
- **Anclaje de ejemplos**: `<FEW_SHOT_ANCHORS>` con par input/output ilustrativo.
- **Secciones visuales**: de 5 a 9 (añade Anexos, Espacio IA Posterior, Análisis de Cobertura, Registro de Procesamiento, Autoría con firma, contacto y URL).
- **Restricciones duras**: de 5 a ~15, con sincronización obligatoria entre secciones visuales y JSON.
- **Trazabilidad**: `identificador_unico` (timestamp de sesión) y `fecha_generacion`, exigidos a coincidir entre visual y JSON.
- **Código**: la línea "SI TRANSCRIBES CODIGO CON INTEGRIDAD" de v0.0.0 desaparece hasta beta6.

---

## [v0.0.0] - Sin fecha

### Estado inicial

- Autoidentificación: ninguna (`<MOTOR_ESTRUCTURACION_DOCUMENTAL>` sin `<version>`).
- Salida: un solo documento Markdown con 5 secciones.
- Sin fetch, sin configuración, sin trazabilidad, sin JSON.
- Restricciones duras: 5 reglas básicas.
- Única mención de código: "SI TRANSCRIBES CODIGO CON INTEGRIDAD" (sin protocolo).

---

## Anomalías detectadas

**Fechas idénticas en beta2–beta5**: beta2, beta3, beta4 y beta5 declaran la misma fecha exacta (`2026-05-23`) en su historial, pese a ser revisiones estructuralmente distintas. Esto sugiere que las fechas se copiaron hacia adelante sin actualizarse. beta6, en cambio, trae una fecha distinta (`2026-07-28`), separada por más de dos meses.

**Duplicados**: Doc6/Doc12 (beta2), Doc9/Doc10/Doc11 (beta5) y Doc4/Doc7 (beta6) son copias idénticas entre sí. Solo se transcribió una por grupo.

**Beta3 ausente**: no se recibió el archivo de beta3 como artefacto independiente. Solo existe referenciado dentro del historial de beta4 y beta5.
