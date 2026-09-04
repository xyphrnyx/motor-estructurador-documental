# Motor Estructurador Documental

**Repositorio de versionado de prompts para el Motor de Procesamiento Estructural No Conversacional**

---

## 📖 Descripción

Este repositorio contiene el historial completo de versiones del **Motor Estructurador Documental**, un sistema de instrucciones diseñado para transformar texto fuente en documentos estructurados con salida dual: **Markdown visual** y **JSON indexado**.

Desarrollado por **nyx** (akaath@icloud.com), este motor ha evolucionado desde una simple plantilla de estructuración hasta un sistema complejo con clasificación documental, trazabilidad, protección anti-inyección y protocolos especializados para scripts y aprendizaje técnico.

---

## 🗺️ Línea de tiempo de versiones

| Versión | Fecha | Tema central |
|---------|-------|--------------|
| **v0.0.0** | — | Documento único, sin trazabilidad |
| **beta2** | 2026-05-23 | Salida dual + trazabilidad + auditoría |
| **beta3** | 2026-05-23 | *(fantasma)* Resumen ejecutivo BLUF |
| **beta4** | 2026-05-23 | Historial de versiones interno |
| **beta5** | 2026-05-23 | Clasificación automática + ISO 15489 |
| **beta6** | 2026-07-28 | Honestidad operativa + anti-inyección + protocolo para scripts |

> **Nota:** beta3 no se recibió como archivo independiente; solo existe referenciado en los historiales de beta4 y beta5. Se documenta como versión "fantasma".

---

## 🚀 Cómo usar este repositorio

### Ver una versión específica
# Motor Estructurador Documental

**Repositorio de versionado de prompts para el Motor de Procesamiento Estructural No Conversacional**

---

## 📖 Descripción

Este repositorio contiene el historial completo de versiones del **Motor Estructurador Documental**, un sistema de instrucciones diseñado para transformar texto fuente en documentos estructurados con salida dual: **Markdown visual** y **JSON indexado**.

Desarrollado por **nyx** (akaath@icloud.com), este motor ha evolucionado desde una simple plantilla de estructuración hasta un sistema complejo con clasificación documental, trazabilidad, protección anti-inyección y protocolos especializados para scripts y aprendizaje técnico.

---

## 🗺️ Línea de tiempo de versiones

| Versión | Fecha | Tema central |
|---------|-------|--------------|
| **v0.0.0** | — | Documento único, sin trazabilidad |
| **beta2** | 2026-05-23 | Salida dual + trazabilidad + auditoría |
| **beta3** | 2026-05-23 | *(fantasma)* Resumen ejecutivo BLUF |
| **beta4** | 2026-05-23 | Historial de versiones interno |
| **beta5** | 2026-05-23 | Clasificación automática + ISO 15489 |
| **beta6** | 2026-07-28 | Honestidad operativa + anti-inyección + protocolo para scripts |

> **Nota:** beta3 no se recibió como archivo independiente; solo existe referenciado en los historiales de beta4 y beta5. Se documenta como versión "fantasma".

---

## 🚀 Cómo usar este repositorio

### Ver una versión específica
git checkout v0.0.0   # o beta2, beta4, beta5, beta6

## Comparar dos versiones
git diff beta4 beta5

## Probar una versión en tu asistente IA
Copia el contenido del archivo prompt.md de la versión deseada y pégalo como instrucción principal. Añade el texto a procesar dentro de las etiquetas <TEXTO_FUENTE>.

## 📂 Estructura del repositorio

/
├── versions/               # Todas las versiones del motor
│   ├── v0.0.0/
│   ├── beta2/
│   ├── beta3-ghost/       # Solo documentación
│   ├── beta4/
│   ├── beta5/
│   └── beta6/
├── related-tools/          # Herramientas relacionadas pero independientes
│   └── extractor-portadas-frameworks/
├── evals/                  # Métricas y resultados de pruebas
└── CHANGELOG.md           # Historial detallado de cambios

## 📋 Registro de cambios
Consulta el archivo CHANGELOG.md para el detalle completo de cada transición entre versiones.

## 🧪 Pruebas y evaluación
La carpeta evals/ contiene plantillas para registrar métricas de rendimiento de cada versión. Si has realizado pruebas A/B con diferentes versiones, puedes documentar los resultados allí.

## 📄 Licencia y autoría
© 2026 nyx. Todos los derechos reservados.

El motor y sus versiones son propiedad intelectual de su autor. Este repositorio es público únicamente con fines de documentación y trazabilidad.

Este repositorio es personal y no se aceptan contribuciones externas. Sin embargo, si encuentras un error en la documentación, puedes abrir un issue.

## Última actualización: 2026-09-04
