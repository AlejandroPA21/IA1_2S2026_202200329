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
├── LICENSE                   # Licencia MIT
├── requirements.txt          # Dependencias de Python
├── docs/
│   ├── decisiones_tecnicas.md    # Bitácora de decisiones técnicas y su justificación
│   ├── guia_informe_prolog.md    # Guía de qué correr/capturar para el PDF de evidencia Prolog
│   ├── manual_tecnico/           # Manual técnico (borrador en Entrega No. 1)
│   ├── manual_usuario/           # Manual de usuario (paciente y administrador)
│   ├── mockups/                  # Diseño de interfaz / wireframes navegables
│   ├── diagramas/                # Diagramas de arquitectura y flujo (Mermaid)
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
│       └── admin_rpa.py          # Automatización de carga masiva de enfermedades
├── scripts/
│   ├── demo_prolog.pl            # Corre las queries de referencia directo en swipl
│   └── demo_pyswip.py            # Las mismas queries, pero via pyswip desde Python
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

🚧 En desarrollo. Ya funcionan de punta a punta: el formulario de paciente contra el motor
Prolog real (afinidad, urgencia, medicamento seguro, PDF descargable), y el panel de
administrador (login, CRUD de enfermedades/síntomas/medicamentos/contraindicaciones,
exportación del `.pl` y carga masiva vía RPA), reemplazando los mockups estáticos de
`docs/mockups/` por plantillas Jinja2 que consumen las rutas Flask reales. Pendiente para la
Entrega No. 2: automatización de la interfaz gráfica del RPA con PyAutoGUI (por ahora
`admin_rpa.py` ejecuta la misma lógica de alta que usa el formulario manual, ver
`docs/decisiones_tecnicas.md`), y los entregables de documentación/evaluación de coherencia.

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
