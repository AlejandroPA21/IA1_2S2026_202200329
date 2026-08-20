# Manual Técnico — MediLogic (Borrador, Entrega No. 1 — Tarea 1)

> Este documento es el **borrador inicial** del Manual Técnico que pide la Entrega No. 1
> (sección 7 del cronograma del enunciado). Se ampliará y se convertirá a PDF final en la
> Entrega No. 2, cuando el sistema esté completamente funcional.

## 1. Resumen del proyecto

MediLogic es un sistema experto de diagnóstico médico preliminar. Un motor de inferencia
escrito íntegramente en Prolog (`src/prolog/knowledge_base.pl`) recibe los síntomas, alergias
y enfermedades crónicas de un paciente y calcula, para cada enfermedad conocida, un porcentaje
de afinidad, un nivel de urgencia y un medicamento seguro sugerido. Un módulo administrativo
(protegido por autenticación) permite mantener esa base de conocimiento sin editar el archivo
`.pl` a mano, incluyendo un robot (RPA) que agiliza el alta masiva de enfermedades.

## 2. Arquitectura del sistema

Arquitectura cliente-servidor: un cliente web (navegador) consume una aplicación Flask que
actúa como orquestador entre la interfaz y el motor lógico Prolog (vía `pyswip`). Ver los
diagramas completos en [docs/diagramas/arquitectura.md](../diagramas/arquitectura.md).

Componentes principales:

| Componente | Ubicación | Responsabilidad |
|---|---|---|
| Interfaz web | `src/backend/templates/`, `src/backend/static/` | Presentar formularios y resultados al paciente/administrador |
| Rutas Flask | `src/backend/routes/` | Recibir peticiones HTTP y orquestar la respuesta |
| Puente Prolog | `src/backend/prolog_engine.py` | Consultar/recargar `knowledge_base.pl` vía `pyswip` |
| Base de conocimiento | `src/prolog/knowledge_base.pl` | Toda la lógica de diagnóstico (hechos y reglas) |
| RPA administrativo | `src/rpa/admin_rpa.py` | Automatizar el alta masiva de enfermedades desde un JSON |

## 3. Herramientas y tecnologías utilizadas

- **Python 3 + Flask** — capa web ligera, ver justificación en `docs/decisiones_tecnicas.md` §1.
- **pyswip (sobre SWI-Prolog)** — integración con el motor lógico real, ver §2.
- **PyAutoGUI** — automatización RPA del lado del backend, ver §3.
- **ReportLab** — generación del informe de diagnóstico en PDF, ver §4.
- **pytest** — pruebas automatizadas del backend.

## 4. Estructura del archivo `knowledge_base.pl`

El archivo está organizado en 12 secciones numeradas y comentadas:

1. Catálogo de síntomas (`sintoma/1`)
2. Catálogo de medicamentos (`medicamento/1`)
3. Enfermedades (`enfermedad/4`: nombre, descripción, sistema del cuerpo, tipo)
4. Relación enfermedad–síntoma (`enfermedad_sintoma/2`)
5. Relación enfermedad–medicamento que la trata (`medicamento_para/2`)
6. Contraindicaciones fármaco–patología (`contraindicacion_enfermedad/2`)
7. Catálogos derivados: `alergia/1` (deriva de `medicamento/1`) y `enfermedad_cronica/1`
   (deriva de `enfermedad/4` filtrando `tipo = cronico`)
8. Ponderación de severidad (`peso_severidad/2`) y cálculo de afinidad (`afinidad/3`)
9. Nivel de urgencia (`nivel_urgencia/3`)
10. Seguridad de medicamentos: contraindicación por alergia y por enfermedad crónica
    (`medicamento_seguro/3`, `medicamento_sugerido/4`)
11. Diagnóstico e informe completo (`diagnosticar/2`, `informe/4`)
12. Consultas de ejemplo (comentadas, documentadas también en la sección 5 de este manual)

### 4.1 Justificación de las reglas principales

- **`afinidad/3`** implementa literalmente el criterio de la sección 4.2 del enunciado:
  puntos acumulados por síntomas coincidentes (ponderados por severidad: leve=1,
  moderado=2, severo=3) sobre el total máximo posible para esa enfermedad. El "máximo
  posible" se definió como todos los síntomas de la enfermedad en su grado más severo —
  ver justificación completa en `docs/decisiones_tecnicas.md` §8.
- **`nivel_urgencia/3`** traduce el porcentaje de afinidad a una de las tres recomendaciones
  textuales que exige el enunciado, con umbrales documentados en `docs/decisiones_tecnicas.md` §9.
- **`medicamento_sugerido/4`** implementa los **dos niveles obligatorios de contraindicación**
  de la sección 4.2: descarta primero el medicamento contraindicado contra la enfermedad que
  se está tratando, y luego contra las alergias/enfermedades crónicas propias del paciente;
  si el primer candidato falla, prueba automáticamente el siguiente medicamento registrado
  para esa enfermedad.
- **`diagnosticar/2`** ordena los diagnósticos de mayor a menor afinidad usando
  `sort(2, @>=, ...)`, eligiendo deliberadamente `@>=` en vez de `@>` para no perder
  enfermedades que empaten en porcentaje (un detalle de corrección que se documenta porque
  `predsort/3`, la alternativa más obvia, sí eliminaría esos empates).

## 5. Consultas de ejemplo y su explicación

Estas son las consultas de referencia definidas en la sección 12 del archivo `.pl`,
verificadas con `swipl` y con `pyswip` (ver `docs/decisiones_tecnicas.md` §10):

1. `afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P).`
   Calcula el % de afinidad con hipertensión para un paciente con dolor de cabeza moderado
   y mareo severo. Resultado: `P = 56` (puntos 2+3=5 sobre un máximo de 9 posibles).

2. `nivel_urgencia(56, Nivel, Recomendacion).`
   Traduce ese 56% a un nivel de urgencia. Resultado: `Nivel = media`,
   `Recomendacion = 'Posible automanejo'`.

3. `medicamento_sugerido(hipertension, [losartan], [], Medicamento).`
   Si el paciente es alérgico a losartán (el medicamento de primera línea), el motor prueba
   el siguiente candidato registrado. Resultado: `Medicamento = enalapril`.

4. `diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], Diagnosticos).`
   Devuelve todas las enfermedades con al menos un síntoma coincidente, ordenadas de mayor a
   menor afinidad. Resultado: `[diagnostico(hipertension, 56), diagnostico(gastroenteritis_aguda, 8)]`.

5. `informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe).`
   Consulta integral: junta afinidad, urgencia y medicamento seguro. Como el paciente es
   alérgico a ibuprofeno (que no es ni siquiera candidato de `medicamento_para` para
   hipertensión), el motor sugiere con normalidad `losartan`.

## 6. Flujo de interacción entre módulos

Ver [docs/diagramas/arquitectura.md](../diagramas/arquitectura.md) — incluye el diagrama de
secuencia del diagnóstico de un paciente y el de la actualización administrativa (con RPA).

## 7. Diseño de interfaz

Ver [docs/mockups/](../mockups/) — wireframes navegables de las 7 pantallas principales
(inicio, formulario de paciente, informe de resultados, login/panel/CRUD de administrador,
pantalla del RPA), con el flujo de navegación documentado en `docs/mockups/README.md`.

## 8. Decisiones técnicas y su justificación

Ver [docs/decisiones_tecnicas.md](../decisiones_tecnicas.md) — bitácora completa de las
decisiones tomadas de forma autónoma durante el desarrollo (framework, librería Prolog, RPA,
generación de PDF, estructura de carpetas, interpretación de fórmulas, umbrales, y validación
del motor lógico).

## 9. Pendiente para la Entrega No. 2

- Implementación funcional de `src/backend/prolog_engine.py` y las rutas Flask (`routes/`).
- Conversión de los mockups estáticos en plantillas Jinja2 reales.
- Implementación funcional del RPA (`src/rpa/admin_rpa.py`) con PyAutoGUI.
- Generación real del informe en PDF (ReportLab) y del historial de sesión.
- Ampliación del catálogo de enfermedades/síntomas/medicamentos.
- Manual de Usuario (con capturas de pantalla del sistema ya funcional).
- Evaluación de coherencia diagnóstica con 3+ casos clínicos y reflexión crítica.
