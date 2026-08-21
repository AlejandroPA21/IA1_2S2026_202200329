<!--
  INSTRUCCIONES PARA TI (borra este bloque de comentario antes de exportar el PDF):

  1. Sigue docs/guia_informe_prolog.md para saber EXACTAMENTE qué correr y qué capturar.
  2. Guarda cada captura en docs/informe_prolog/imagenes/ con el nombre de archivo que ya
     está escrito en cada ![...](imagenes/nombre.png) de abajo. Si usas otro nombre, solo
     edita la ruta entre paréntesis — no toques nada más.
  3. Los bloques marcados [OPCIONAL] puedes borrarlos si no vas a incluir esa captura.
  4. Los campos entre corchetes [ASI] los reemplazas por tu dato real (nombre, carné, fecha).
  5. Cuando termines de pegar las imágenes, exporta a PDF (ver "Cómo exportar a PDF" al
     final de este archivo, o en el mensaje de instrucciones que acompaña esta plantilla).
-->

# MediLogic — Evidencia del motor lógico en Prolog

**Curso:** Inteligencia Artificial 1 — Universidad San Carlos de Guatemala

**Estudiante:** Adler Alejandro Pérez Asensio

**Carné:** 202200329

**Proyecto:** MediLogic — Entrega No. 1, Tarea 1

**Fecha:** [21/08/2026]

---

## 1. Introducción

`src/prolog/knowledge_base.pl` es la base de conocimiento del sistema experto MediLogic:
contiene, íntegramente en Prolog, los hechos (síntomas, medicamentos, enfermedades y sus
relaciones) y las reglas de inferencia que calculan el porcentaje de afinidad de cada
enfermedad, su nivel de urgencia y el medicamento más seguro para el paciente, evitando
contraindicaciones por alergias o enfermedades crónicas. Este documento presenta el código
fuente de las reglas principales y la evidencia de su ejecución mediante consultas de
prueba, tanto directamente en `swipl` como a través de `pyswip` desde Python.

---

## 2. Código fuente en Prolog

### 2.1 Hechos base — catálogos y relaciones (secciones 1–7) 

Muestra que la base de conocimiento también tiene datos, no solo reglas: catálogo de
síntomas, medicamentos, enfermedades y las relaciones enfermedad–síntoma,
medicamento–enfermedad y contraindicación fármaco–patología.

![Hechos base: síntomas, medicamentos, enfermedades y relaciones](imagenes/01_hechos_base.png)

### 2.2 Ponderación de severidad y cálculo de afinidad (sección 8)

Regla más importante del sistema: pondera cada síntoma por su severidad (leve=1,
moderado=2, severo=3) y calcula el porcentaje de afinidad como la proporción entre los
puntos acumulados y el máximo posible para esa enfermedad, tal como exige la sección 4.2
del enunciado.

![peso_severidad/2 y afinidad/3](imagenes/02_afinidad.png)

### 2.3 Nivel de urgencia (sección 9)

Traduce el porcentaje de afinidad a una recomendación textual ("Consulta médica inmediata
sugerida", "Posible automanejo" u "Observación recomendada"), según los umbrales
justificados en `docs/decisiones_tecnicas.md`.

![nivel_urgencia/3](imagenes/03_urgencia.png)

### 2.4 Seguridad de medicamentos (sección 10)

Implementa los dos niveles obligatorios de contraindicación: contra la enfermedad que se
está tratando y contra las alergias/enfermedades crónicas del paciente, sustituyendo
automáticamente el medicamento cuando el primer candidato no es seguro.

![medicamento_seguro/3 y medicamento_sugerido/4](imagenes/04_medicamento_seguro.png)

### 2.5 Diagnóstico e informe completo (sección 11)

Consulta integral que junta afinidad, urgencia y medicamento seguro para cada enfermedad
coincidente, ordenadas de mayor a menor afinidad — es la que consumirá la interfaz web.

![diagnosticar/2 e informe/4](imagenes/05_informe.png)

---

## 3. Ejecución de las queries de referencia

Consultas verificadas con `swipl scripts/demo_prolog.pl` (y también con `pyswip` mediante
`python scripts/demo_pyswip.py`, como evidencia de que Python se comunica correctamente con
el motor lógico):

![Salida de las 5 queries de referencia — parte 1](imagenes/06_queries_1.png)


<!-- Si toda la salida cupo en una sola captura, borra el bloque de "parte 2" de arriba. -->

| # | Query | Qué demuestra | Resultado |
|---|---|---|---|
| 1 | `afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P)` | Calcula el % de afinidad ponderando la severidad de cada síntoma sobre el máximo posible para esa enfermedad. | `P = 56` |
| 2 | `nivel_urgencia(56, Nivel, Recomendacion)` | Traduce el porcentaje anterior a un nivel de urgencia y su recomendación textual. | `media` / `'Posible automanejo'` |
| 3 | `medicamento_sugerido(hipertension, [losartan], [], Medicamento)` | El paciente es alérgico al medicamento de primera línea; el motor descarta esa opción y sugiere el siguiente candidato seguro, demostrando el nivel de contraindicación "condiciones del paciente". | `Medicamento = enalapril` |
| 4 | `diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], D)` | Evalúa todas las enfermedades registradas y devuelve solo las que tienen al menos un síntoma coincidente, ordenadas de mayor a menor afinidad. | `[diagnostico(hipertension, 56), diagnostico(gastroenteritis_aguda, 8)]` |
| 5 | `informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe)` | Consulta integral: junta afinidad + urgencia + medicamento seguro en un solo resultado. | Sugiere `losartan` (el paciente no es alérgico a él) |
---
## 5. Evidencia de Server Corriendo

---

## 5. Conclusión

Las reglas de `knowledge_base.pl` quedaron validadas de forma independiente al motor logico
(`swipl`) y a través de la integración real con Python (`pyswip`), confirmando que el cálculo
de afinidad, el nivel de urgencia y la sugerencia segura de medicamentos funcionan según lo
especificado en el enunciado. 

