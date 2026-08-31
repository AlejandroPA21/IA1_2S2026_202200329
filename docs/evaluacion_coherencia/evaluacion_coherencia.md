# Evaluación de coherencia diagnóstica y análisis crítico — MediLogic

**Curso:** Inteligencia Artificial 1 — Universidad San Carlos de Guatemala
**Proyecto:** MediLogic — Entrega No. 2, Proyecto Final

Los tres casos siguientes se ejecutaron contra la aplicación real (`python src/backend/app.py`
+ `swipl` + `pyswip`, sin datos inventados), enviando peticiones HTTP directamente a
`/paciente/diagnostico` tal como lo haría el navegador, contra el catálogo tal cual viene en
el repositorio (`src/prolog/knowledge_base.pl`): hipertensión, asma bronquial, diabetes tipo 2
y gastroenteritis aguda.

Los tres casos cubren los escenarios de diagnóstico descritos en `Escenarios Proyecto 1.txt`:
el Caso 1 combina un **Escenario A** (coincidencia alta, sin contraindicaciones) con la
diabetes como diagnóstico secundario de baja afinidad; el Caso 2 es un **Escenario B**
(conflicto detectado, sin alternativa segura); el Caso 3 es un **Escenario A** simple, de
control. El **Escenario C** (síntomas insuficientes o no concluyentes) no se documenta aquí
como caso clínico narrado porque no aporta un diagnóstico que analizar — pero sí está cubierto
como prueba automatizada (`tests/test_diagnostico.py::test_diagnostico_sin_sintomas_no_rompe`),
que verifica que el sistema responde con claridad ("No se encontraron enfermedades") en vez de
fallar o inventar un resultado.

## Caso 1 — Múltiples diagnósticos y sustitución por alergia

**Entrada:** dolor de cabeza (severo), mareo (moderado), visión borrosa (leve) · alergia:
losartán · antecedente crónico: diabetes tipo 2.

| # | Enfermedad | Afinidad | Urgencia | Medicamento sugerido |
|---|---|---|---|---|
| 1 | Hipertensión | **67%** | Alta — *"Consulta médica inmediata sugerida"* | Enalapril |
| 2 | Diabetes tipo 2 | 11% | Baja — *"Observación recomendada"* | Metformina |

**Análisis de coherencia:** dolor de cabeza + mareo + visión borrosa es la tríada clásica de
crisis hipertensiva, así que es clínicamente coherente que el sistema la coloque primero, con
urgencia alta. La sustitución de medicamento es correcta: losartán era el primer candidato
registrado para hipertensión, pero el paciente es alérgico, y el motor prueba
automáticamente el siguiente (enalapril) en vez de forzar la primera opción o dejar el campo
vacío. **Observación:** diabetes tipo 2 aparece como segundo diagnóstico con 11% pese a que el
paciente ya la declaró como antecedente crónico (no como síntoma nuevo); el motor no excluye
del universo de diagnósticos posibles a las enfermedades que el paciente ya dijo tener, porque
`diagnosticar/2` evalúa todas las `enfermedad/4` registradas sin comparar contra
`EnfermedadesCronicas`. No es necesariamente un error — un antecedente crónico también puede
estar reagudizándose — pero sí es una limitación a tener presente: el sistema no distingue
"posible enfermedad nueva" de "reaparición de una condición ya conocida por el paciente".

## Caso 2 — Sin alternativa segura disponible

**Entrada:** dificultad respiratoria (severo), silbido en el pecho (moderado), tos seca (leve)
· alergia: salbutamol · sin antecedentes crónicos.

| # | Enfermedad | Afinidad | Urgencia | Medicamento sugerido |
|---|---|---|---|---|
| 1 | Asma bronquial | **67%** | Alta — *"Consulta médica inmediata sugerida"* | *Ningún medicamento seguro disponible* |

**Análisis de coherencia:** la tríada dificultad respiratoria + silbido + tos seca es
coherente con un cuadro de asma, y la urgencia alta con 67% de afinidad es razonable dada la
severidad reportada. Lo relevante de este caso es la respuesta ante la alergia: salbutamol es
el **único** medicamento registrado como tratamiento para asma bronquial
(`medicamento_para(salbutamol, asma_bronquial)` es la única cláusula), y el paciente es
alérgico precisamente a él. El motor no "fuerza" salbutamol ni inventa una alternativa que no
esté en la base de conocimiento: `medicamento_sugerido/4` falla limpiamente y
`informe/4` lo traduce a `ninguno_disponible`, que la interfaz muestra como una advertencia
explícita en vez de dejar el campo vacío o mostrar un error. Es el comportamiento
correcto y más seguro que puede tener un sistema de reglas ante un vacío real de su base de
conocimiento: reconocer el límite en vez de improvisar una recomendación médica sin respaldo.

## Caso 3 — Caso simple sin complicaciones (control)

**Entrada:** dolor abdominal (moderado), diarrea (leve) · sin alergias ni antecedentes.

| # | Enfermedad | Afinidad | Urgencia | Medicamento sugerido |
|---|---|---|---|---|
| 1 | Gastroenteritis aguda | **25%** | Media — *"Posible automanejo"* | Suero oral |

**Análisis de coherencia:** único diagnóstico compatible, con síntomas leves/moderados y sin
alergias ni antecedentes que compliquen la sugerencia de medicamento. El resultado es
coherente y sirve como caso de control: sin factores de riesgo, el sistema no genera alertas
innecesarias ni recomienda urgencia alta por síntomas menores — evidencia de que no hay sesgo
hacia sobre-alertar cuando el cuadro clínico es leve.

## Un camino de la regla de contraindicación que el catálogo actual no ejercita

La sección 4.2 del enunciado exige **dos niveles** de contraindicación: contra la enfermedad
que se está tratando (`contraindicacion_enfermedad/2`, verificado directamente en
`medicamento_sugerido/4`) y contra las enfermedades crónicas/alergias del paciente
(`medicamento_seguro/3`, con `contraindicado_por_alergia/2` y `contraindicado_por_cronica/2`).
El nivel de alergia queda demostrado con datos reales en el Caso 1 y en el Caso 2. Al intentar
construir un caso real para el nivel de **enfermedad crónica** (`contraindicado_por_cronica/2`)
se encontró que, con las 4 enfermedades que trae el catálogo, **ninguna combinación posible lo
activa**: cada medicamento de `medicamento_para/2` solo trata una enfermedad, y ninguno de
esos medicamentos está también en `contraindicacion_enfermedad/2` contra una enfermedad
*distinta* a la que trata — que es justamente el escenario que `contraindicado_por_cronica/2`
necesita para dispararse (ej. un medicamento para migraña que esté contraindicado en pacientes
hipertensos). La regla está correctamente implementada y unificada de forma consistente con
`contraindicado_por_alergia/2` (se puede confirmar leyéndola y ejecutándola manualmente con
hechos de prueba en `swipl`), pero **no hay evidencia end-to-end de que se dispare en un
diagnóstico real** con los datos que trae el proyecto. Se documenta como hallazgo honesto de
esta evaluación en vez de forzar una enfermedad nueva solo para "maquillar" una ejecución
positiva: es información real y útil para quien administre el sistema — agregar, desde el
panel de administrador, una segunda enfermedad que comparta un medicamento contraindicado con
alguna de las cuatro existentes (ej. un segundo tratamiento para dolor de cabeza contraindicado
en hipertensión) haría que este camino de la regla quede probado con un caso real.

## Reflexión crítica: IA simbólica vs. enfoques modernos

### 1. Limitaciones del enfoque simbólico ante la ambigüedad

El motor de MediLogic es determinista: `afinidad/3` calcula un porcentaje exacto a partir de
una suma de pesos fijos (leve=1, moderado=2, severo=3) sobre un máximo también fijo por
enfermedad, y `nivel_urgencia/3` traza un corte numérico duro (≥60% = alta, si no ≥20% =
media, si no baja). Esto trae problemas observables incluso en los tres casos anteriores:

- **Frontera artificial:** un paciente con 59% de afinidad recibe "posible automanejo" y uno
  con 60% recibe "consulta médica inmediata", pese a que la diferencia real entre ambos
  perfiles clínicos es mínima. Prolog no tiene noción de "casi alcanza el umbral"; solo evalúa
  si la comparación aritmética es verdadera o falsa.
- **Escala de afinidad no comparable entre enfermedades:** el máximo posible de cada
  enfermedad depende de cuántos síntomas tiene catalogados (`puntos_maximos_enfermedad/2`).
  Hipertensión y asma bronquial tienen ambas 3 síntomas catalogados y, con perfiles de
  severidad equivalentes en los casos 1 y 2, coinciden en 67% — pero esa coincidencia es
  producto del tamaño igual de sus catálogos, no de una probabilidad clínica comparable de
  forma absoluta entre enfermedades distintas. Si el administrador amplía el catálogo de una
  enfermedad más que el de otra, sus porcentajes de afinidad dejan de ser comparables entre sí
  aunque ambos sigan siendo correctos *dentro* de su propia enfermedad.
- **Síntomas no contemplados:** si un paciente presenta un síntoma real pero no catalogado (o
  una combinación atípica), el motor simplemente no lo considera — no hay margen para "esto se
  parece a X aunque no encaje exactamente", porque cada regla exige que el hecho coincida
  literalmente (`enfermedad_sintoma(Enfermedad, Sintoma)`, `member/2`).
- **Reglas correctas pero no ejercitadas:** como se documentó arriba, `contraindicado_por_cronica/2`
  es una regla bien definida que, sin embargo, el catálogo actual nunca llega a activar en la
  práctica — un recordatorio de que "la regla está bien escrita" y "la regla se ha visto
  funcionar con datos reales" son afirmaciones distintas en un sistema simbólico: la cobertura
  de las reglas depende enteramente de que los datos cargados generen los casos que las
  disparan.

### 2. Comparación con IA basada en datos (Machine Learning / modelos probabilísticos)

Un modelo estadístico entrenado con historiales clínicos reales (por ejemplo, una regresión
logística o un árbol de decisión sobre miles de casos) no calcularía la afinidad como una
proporción de puntos fijos, sino como una probabilidad condicional aprendida de la covarianza
real entre síntomas y diagnósticos confirmados — capturando, por ejemplo, que "dolor de
cabeza + mareo" predice hipertensión con más fuerza en pacientes mayores de cierta edad, algo
que MediLogic no puede expresar porque no tiene la variable "edad" ni una noción de fuerza de
asociación aprendida, solo pesos fijos definidos a mano por el administrador. Un modelo
probabilístico también manejaría naturalmente el problema de la "frontera artificial" descrito
arriba: en vez de un corte duro en 60%, produciría una distribución de probabilidad continua
(y podría reportar su propia incertidumbre, algo que un sistema de reglas fijas no sabe
expresar: Prolog siempre está "seguro" del resultado de su propia aritmética, incluso cuando el
resultado clínico real es ambiguo). El costo de ese enfoque es la necesidad de datos reales
etiquetados (historiales clínicos), el riesgo de aprender sesgos presentes en esos datos, y la
pérdida de explicabilidad directa: un sistema de reglas como MediLogic puede señalar exactamente
qué regla y qué hechos se activaron (ver "Reglas Prolog activadas" en cada informe, y el Caso 2
de esta evaluación, donde el sistema explica *por qué* no hay medicamento seguro en vez de solo
fallar); un modelo de ML complejo (red neuronal, ensamble de árboles) típicamente no ofrece esa
trazabilidad sin técnicas adicionales de explicabilidad (SHAP, LIME, etc.).

### 3. Escalabilidad y mantenimiento

Con 4 enfermedades el catálogo de MediLogic es completamente manejable a mano desde el panel
administrativo — y aun así, como muestra el hallazgo de la sección anterior, ya es fácil que
una combinación de reglas quede sin ejercitar con datos reales. Si el catálogo creciera a
miles de enfermedades y síntomas, ese problema se agravaría:

- **Costo de curaduría manual:** cada enfermedad nueva requiere que un humano defina a mano
  sus síntomas, medicamentos y contraindicaciones; con miles de enfermedades, mantener esa
  base consistente (sin duplicados, sin contradicciones, con pesos de severidad razonables, y
  con cobertura de prueba real de cada camino lógico) se vuelve un trabajo de equipo completo,
  no de un solo administrador — el RPA de este proyecto automatiza la *carga* de datos ya
  curados, pero no la curaduría clínica en sí.
- **Costo computacional de `diagnosticar/2`:** hoy evalúa **todas** las enfermedades
  registradas contra los síntomas del paciente en cada consulta (`findall/3` sobre
  `enfermedad/4`). Con miles de enfermedades esto sigue siendo viable (Prolog resuelve esto en
  milisegundos incluso con catálogos grandes), pero el verdadero cuello de botella sería
  humano: revisar y validar clínicamente miles de reglas de contraindicación cruzada crece de
  forma combinatoria (medicamentos × enfermedades), no lineal.
- **Enfoques modernos frente a este problema:** un sistema de agentes de IA o un pipeline
  híbrido resolvería la escala de datos entrenando un modelo sobre la evidencia disponible en
  vez de listar cada relación a mano, y usaría técnicas como *retrieval-augmented generation*
  (RAG) sobre literatura médica actualizada para sugerir relaciones candidatas que un experto
  humano solo tendría que validar (no escribir desde cero) — desplazando el trabajo de "crear
  cada regla" a "supervisar candidatos generados", que escala mucho mejor. La contraparte es
  que estos sistemas introducen una capa de incertidumbre y de posible alucinación que un
  motor de reglas exactas como Prolog, por diseño, no tiene: MediLogic nunca va a "inventar"
  una relación medicamento-enfermedad que no esté explícitamente en `knowledge_base.pl`.

### Conclusión de la reflexión

El enfoque simbólico de MediLogic es apropiado para su alcance actual: un catálogo pequeño,
curado, con trazabilidad total de cada decisión (requisito explícito del enunciado: mostrar
qué reglas Prolog se activaron) y sin necesidad de datos de entrenamiento. Su fortaleza —
reglas exactas y explicables— es también su límite: no generaliza a casos fuera de lo
catalogado, no expresa incertidumbre real, y su cobertura de pruebas depende enteramente de
que los datos cargados generen los casos que ejercitan cada regla, como quedó documentado
arriba. Un sistema en producción real, a mayor escala, probablemente combinaría ambos mundos:
un modelo estadístico o de agentes para sugerir y priorizar candidatos a partir de datos
reales, y una capa de reglas simbólicas (como esta) para aplicar restricciones de seguridad
*duras* (una contraindicación medicamentosa no debería depender de "la probabilidad más alta";
debería ser un veto categórico, que es exactamente lo que Prolog hace bien, y que el Caso 2 de
esta evaluación demuestra con un ejemplo real).
