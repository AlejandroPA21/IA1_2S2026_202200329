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
│   │   ├── app.py
│   │   ├── prolog_engine.py      # Puente Python <-> Prolog (pyswip)
│   │   └── routes/               # Blueprints: paciente y administrador
│   └── rpa/
│       └── admin_rpa.py          # Automatización de carga de enfermedades
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

🚧 En desarrollo — Entrega No. 1 (avance inicial).

## Instalación y ejecución

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python src/backend/app.py
```

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
