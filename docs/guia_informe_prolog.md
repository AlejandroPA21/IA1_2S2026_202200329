# Guía para el informe en PDF (Tarea 1 — código Prolog y queries)

Esta guía es para el PDF que exige la rúbrica de la Tarea 1 (código con **CodeSnap** +
queries explicadas). Tú armas el PDF; aquí tienes exactamente qué correr y qué capturar,
en orden, para que quede completo y ordenado.

## 0. Antes de empezar (una sola vez)

SWI-Prolog ya quedó instalado y agregado a tu PATH de usuario. **Abre una terminal nueva**
(cierra y vuelve a abrir la terminal de VS Code, o abre una PowerShell nueva) para que
reconozca el comando `swipl` — los cambios de PATH no aplican a terminales que ya estaban
abiertas antes de la instalación.

Verifica con:

```powershell
swipl --version
```

Deberías ver `SWI-Prolog version 10.0.2 for x64-win64`.

## 1. Qué capturar con CodeSnap (el código)

Abre `src/prolog/knowledge_base.pl` en VS Code y toma una captura con CodeSnap de cada
bloque (no hace falta el archivo completo en una sola imagen, son 12 secciones cortas y
numeradas — captura sección por sección, o agrupa 2-3 secciones relacionadas por imagen):

1. **Sección 8** (`peso_severidad/2`, `afinidad/3`) — es la regla más importante: el
   cálculo de afinidad ponderado por severidad que pide el enunciado.
2. **Sección 9** (`nivel_urgencia/3`) — traduce el % de afinidad a la recomendación textual.
3. **Sección 10** (`medicamento_seguro/3`, `medicamento_sugerido/4`) — los dos niveles de
   contraindicación (alergia y enfermedad crónica) y la sustitución automática de medicamento.
4. **Sección 11** (`diagnosticar/2`, `informe/4`) — la consulta integral que junta todo.

(Opcional pero recomendable: una captura de las secciones 1-7 con los hechos base, para
mostrar que la base de conocimiento también tiene datos, no solo reglas.)

## 2. Qué correr y capturar (las queries)

### Opción A — directamente en Prolog (recomendada, más simple)

Desde la raíz del repositorio:

```powershell
swipl scripts/demo_prolog.pl
```

Esto imprime, ya formateadas y con una breve explicación arriba de cada una, las 5 queries
de referencia. **Captura la salida completa de la terminal** (o en 2-3 capturas si no cabe
todo en una pantalla) — ya viene lista para pegar en el PDF tal cual, sección por sección:

1. `afinidad/3` — afinidad de un paciente con hipertensión.
2. `nivel_urgencia/3` — nivel de urgencia para ese porcentaje.
3. `medicamento_sugerido/4` — sustitución automática cuando el paciente es alérgico al
   medicamento de primera línea.
4. `diagnosticar/2` — varias enfermedades coincidentes, ordenadas por afinidad.
5. `informe/4` — la consulta integral (afinidad + urgencia + medicamento seguro).

### Opción B — también desde Python/pyswip (evidencia extra de la integración)

```powershell
.venv\Scripts\activate
python scripts\demo_pyswip.py
```

Mismas 5 consultas, pero mostrando que Python (`pyswip`) se comunica correctamente con el
motor Prolog — útil como evidencia de que la arquitectura cliente-servidor descrita en el
Manual Técnico ya funciona de extremo a extremo, no solo en teoría.

### Opción C — consola interactiva de Prolog (si quieres mostrar que tú mismo escribes la query)

```powershell
swipl
?- consult('src/prolog/knowledge_base.pl').
?- afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P).
?- diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], D).
?- informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe).
```

## 3. Explicación breve de cada query (para copiar/parafrasear en el PDF)

| # | Query | Qué demuestra |
|---|---|---|
| 1 | `afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P)` | Calcula el % de afinidad ponderando la severidad de cada síntoma (leve=1, moderado=2, severo=3) sobre el máximo posible para esa enfermedad. Resultado: `P = 56`. |
| 2 | `nivel_urgencia(56, Nivel, Recomendacion)` | Traduce el porcentaje anterior a un nivel de urgencia y su recomendación textual. Resultado: `media` / `'Posible automanejo'`. |
| 3 | `medicamento_sugerido(hipertension, [losartan], [], Medicamento)` | El paciente es alérgico al medicamento de primera línea (losartán); el motor descarta esa opción automáticamente y sugiere el siguiente candidato seguro (`enalapril`), demostrando el nivel de contraindicación "condiciones del paciente". |
| 4 | `diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], D)` | Evalúa todas las enfermedades registradas y devuelve solo las que tienen al menos un síntoma coincidente, ordenadas de mayor a menor afinidad. |
| 5 | `informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe)` | Consulta integral: junta afinidad + urgencia + medicamento seguro en un solo resultado, tal como lo consumirá la interfaz web. |

## 4. Estructura sugerida del PDF (para evitar la penalización de "desordenado")

1. Portada (nombre, carnet, curso, proyecto MediLogic).
2. Breve introducción (1 párrafo: qué es `knowledge_base.pl` y qué resuelve).
3. Código fuente por secciones (capturas CodeSnap del punto 1, con un título antes de cada
   una indicando qué predicado(s) contiene).
4. Queries de prueba (capturas del punto 2), cada una con su explicación breve del punto 3
   justo debajo o al lado de la captura — no todas las capturas juntas al final sin contexto.
5. Conclusión breve (1-2 líneas: qué quedó funcionando y qué falta para la Entrega No. 2).

## 5. Otras verificaciones que puedes correr y mencionar/capturar (opcional)

```powershell
.venv\Scripts\activate
pytest                       # confirma que el esqueleto Flask sigue funcionando
python src\backend\app.py    # levanta el servidor en http://127.0.0.1:5000 (solo pantalla "en construccion" por ahora)
```

Abrir en el navegador `docs/mockups/01_inicio.html` y navegar entre pantallas también es
válido como evidencia visual del diseño de interfaz, si quieres incluir 1-2 capturas de eso
en el manual técnico (no es obligatorio para esta Tarea 1, que es específicamente sobre el
código Prolog).
