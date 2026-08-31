# MediLogic

Sistema experto de diagnóstico médico preliminar basado en lógica computacional (Prolog)
y automatización robótica de procesos (RPA), desarrollado para el curso de Inteligencia
Artificial 1 — Universidad San Carlos de Guatemala.

> ⚠️ MediLogic es una herramienta de apoyo diagnóstico **preliminar** y **no sustituye**
> la consulta médica profesional.

## Descripción

El sistema permite a un paciente ingresar síntomas (con su nivel de severidad), alergias a
medicamentos y enfermedades crónicas preexistentes, para recibir un informe con posibles
enfermedades, su porcentaje de afinidad, el nivel de urgencia y el medicamento más seguro
sugerido, evitando contraindicaciones. Toda la lógica de diagnóstico se implementa en
Prolog; un módulo administrativo protegido por autenticación permite gestionar la base de
conocimiento (enfermedades, síntomas, medicamentos y contraindicaciones) sin editar el
archivo `.pl` manualmente, incluyendo un RPA que agiliza la carga masiva de enfermedades.

Ver [ENUNCIADO.md](ENUNCIADO.md) para el enunciado completo del proyecto.

## Estructura del repositorio

```
.
├── ENUNCIADO.md              # Enunciado oficial del proyecto
├── EjemploRPA.json           # Formato de ejemplo para la carga por RPA
├── Ejemplo Archivo RPA V2.json  # Variante con el campo opcional tratamiento_recomendado
├── Escenarios Proyecto 1.txt    # Escenarios de referencia (diagnóstico y RPA)
├── LICENSE                   # Licencia MIT
├── requirements.txt          # Dependencias de Python
├── docs/
│   ├── decisiones_tecnicas.md    # Bitácora de decisiones técnicas y su justificación
│   ├── curso_intensivo_prolog.md # Curso rapido de Prolog usando el codigo real del proyecto
│   ├── manual_tecnico/           # Manual técnico final (arquitectura, reglas, config. del RPA)
│   ├── manual_usuario/           # Manual de usuario (paciente y administrador)
│   ├── mockups/                  # Wireframes ESTÁTICOS de la Entrega 1 (NO es la app real)
│   ├── diagramas/                # Diagramas de arquitectura y flujo (Mermaid)
│   ├── informe_prolog/           # Evidencia (capturas + explicación) del motor Prolog
│   └── evaluacion_coherencia/    # Casos clínicos y reflexión crítica IA simbólica vs. moderna
├── src/
│   ├── prolog/
│   │   └── knowledge_base.pl     # Base de conocimiento: hechos y reglas Prolog
│   ├── backend/                  # Aplicación Flask (rutas, plantillas, static)
│   │   ├── app.py                # Fabrica create_app: registra blueprints y motor Prolog
│   │   ├── prolog_engine.py      # Puente Python <-> Prolog (pyswip)
│   │   ├── knowledge_store.py    # CRUD administrativo -> reescribe knowledge_base.pl
│   │   ├── pdf_report.py         # Informe de diagnóstico en PDF (ReportLab)
│   │   ├── routes/               # Blueprints: paciente y administrador
│   │   ├── templates/            # Plantillas Jinja2 (basadas en docs/mockups/)
│   │   └── static/               # CSS y JS de la aplicación real
│   └── rpa/
│       ├── admin_rpa.py          # RPA modo rapido: carga masiva llamando a KnowledgeStore
│       └── gui_automation.py     # RPA modo visual: automatizacion real con PyAutoGUI
├── scripts/
│   ├── demo_prolog.pl            # Corre las queries de referencia directo en swipl
│   ├── demo_pyswip.py            # Las mismas queries, pero via pyswip desde Python
│   └── ejecutar_rpa_gui.py       # Punto de entrada del RPA visual (para el video de evidencia)
└── tests/                        # Pruebas automatizadas (pytest)
```

## Stack tecnológico

- **Backend:** Python + Flask
- **Motor lógico:** SWI-Prolog vía `pyswip`
- **RPA:** `PyAutoGUI` (ejecutado del lado del backend)
- **Reportes PDF:** `ReportLab`
- **Pruebas:** `pytest`

Las decisiones técnicas y su justificación se documentan en
[docs/decisiones_tecnicas.md](docs/decisiones_tecnicas.md).

## Estado del proyecto

✅ Completo para la Entrega No. 2. Funcionan de punta a punta: el formulario de paciente
contra el motor Prolog real (afinidad, urgencia, medicamento seguro, historial de sesión,
PDF descargable), el panel de administrador (login, CRUD de
enfermedades/síntomas/medicamentos/contraindicaciones, exportación del `.pl`) y el RPA de
carga masiva de enfermedades en sus dos modos: rápido (`admin_rpa.py`, vía el botón del
panel) y visual con PyAutoGUI (`gui_automation.py` / `scripts/ejecutar_rpa_gui.py`, para el
video de evidencia — ver el Manual Técnico, sección "Configuración del robot RPA"). 14
pruebas automatizadas en verde (`pytest`). Documentación completa en `docs/`: manual
técnico, manual de usuario, evaluación de coherencia diagnóstica (3 casos clínicos
ejecutados con datos reales + reflexión crítica) y un curso intensivo de Prolog basado en el
código del propio proyecto.

## Documentación

- [Manual técnico](docs/manual_tecnico/manual_tecnico.md) — arquitectura, estructura del
  `.pl`, justificación de reglas y configuración del robot RPA.
- [Manual de usuario](docs/manual_usuario/manual_usuario.md) — guía paso a paso de ambos
  módulos, errores comunes y cómo interpretar el informe.
- [Evaluación de coherencia diagnóstica](docs/evaluacion_coherencia/evaluacion_coherencia.md) —
  3 casos clínicos ejecutados contra la aplicación real + reflexión crítica IA simbólica vs. moderna.
- [Curso intensivo de Prolog](docs/curso_intensivo_prolog.md) — para quien no conoce Prolog:
  explica cada construcción del lenguaje usando el código real de `knowledge_base.pl`.
- [Bitácora de decisiones técnicas](docs/decisiones_tecnicas.md) — el porqué de cada decisión
  tomada durante el desarrollo.

## Instalación y ejecución

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python src/backend/app.py
```

Luego visita `http://127.0.0.1:5000/`. Credenciales de administrador por defecto:
usuario `admin`, contraseña `medilogic2026` (configurables con las variables de entorno
`ADMIN_USER` / `ADMIN_PASSWORD`, ver `docs/decisiones_tecnicas.md`).

> Requiere tener instalado [SWI-Prolog](https://www.swi-prolog.org/) en el sistema para
> que `pyswip` pueda comunicarse con el motor lógico.

## Pruebas

```bash
pytest
```

La base de conocimiento (`src/prolog/knowledge_base.pl`) fue validada manualmente con
consultas de ejemplo tanto desde `swipl` como desde `pyswip`; ver
[docs/decisiones_tecnicas.md](docs/decisiones_tecnicas.md#10-validación-del-archivo-pl).

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver [LICENSE](LICENSE).
