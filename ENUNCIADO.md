# Inteligencia Artificial 1

**Universidad San Carlos de Guatemala**
**Facultad de Ingeniería**
**Ingeniería en Ciencias y Sistemas**

## Título del Proyecto: MediLogic

**PONDERACIÓN:** 30
**Horas Aproximadas:** 50

---

## Índice

### Contenido

1. Resumen Ejecutivo — 3
2. Competencias que desarrollaremos — 3
3. Objetivos del Aprendizaje — 3
   - 3.1 Objetivo General — 3
   - 3.2 Objetivos Específicos — 3
4. Enunciado del Proyecto — 4
   - 4.1 Descripción del problema a resolver — 4
   - 4.2 Alcance del proyecto — 4
   - 4.3 Requerimientos técnicos — 7
   - 4.4 Entregables — 8
5. Metodología — 9
6. Desarrollo de Habilidades Blandas — 10
   - 6.1 Proyectos Individuales — 10
7. Cronograma — 11
8. Rúbrica de Calificación — 12
   - 8.1 Requisitos para optar a la calificación — 12
   - 8.2 Resumen de Puntuaciones — 12
   - 8.3 Detalle de la Calificación — 13
   - 8.4 Valores — 15

---

## 1. Resumen Ejecutivo

Este proyecto consiste en el diseño e implementación de un sistema experto inteligente basado en lógica computacional y automatización robótica de procesos, orientado al diagnóstico médico preliminar. El sistema, denominado MediLogic, permitirá a los usuarios (pacientes) ingresar sus síntomas, enfermedades crónicas y alergias a medicamentos para recibir un informe con posibles enfermedades, porcentaje de afinidad y tratamiento sugerido. Utilizando reglas definidas en prolog, el sistema realizará inferencias que relacionen los datos ingresados con una base de conocimientos médica estructurada. Esta iniciativa busca potenciar el razonamiento computacional de los estudiantes mediante la resolución de problemas del mundo real, y su aplicación podría extenderse a contextos de salud pública o telemedicina.

Este proyecto se fundamenta en el paradigma de sistemas expertos basados en reglas (IA simbólica tradicional). Los estudiantes deberán analizar las limitaciones de este enfoque determinista frente al manejo de incertidumbre y la integración con modelos basados en datos o agentes inteligentes contemporáneos.

## 2. Competencias que desarrollaremos

- Integra fundamentos de lógica y simulación robótica mediante el uso de entornos de desarrollo como Python con pyswip pytholog, PyAutoGUI y TagUI para resolver problemas relacionados a inferencia, interacción digital y simulación de comportamientos autónomos.
- Implementa soluciones de inteligencia artificial empleando técnicas de inferencia lógica y control de robots en distintos escenarios de optimización, clasificación y toma de decisiones.
- Desarrolla hechos, reglas, expresiones y predicados recursivos mediante el uso de cláusulas, ciclos, listas, unificación y cortes en prolog para modelar bases de conocimiento y resolver problemas de inferencia lógica.

## 3. Objetivos del Aprendizaje

### 3.1 Objetivo General

Al finalizar el proyecto, los estudiantes serán capaces de desarrollar una solución tecnológica que resuelva un problema real o simulado por medio de sistemas inteligentes, utilizando Prolog como el lenguaje y principal herramienta para el desarrollo de la lógica e inferencia, integrada con la automatización robótica de procesos. Los estudiantes aplicarán habilidades de programación, diseño de sistemas, trabajo en equipo y metodología de desarrollo, para entregar un prototipo funcional junto con su documentación técnica.

### 3.2 Objetivos Específicos

Al finalizar el proyecto, los estudiantes deberán ser capaces de:

1. **Desarrollar un sistema funcional:** Aplicar los conocimientos adquiridos en el curso para diseñar, implementar y probar un sistema experto capaz de inferir enfermedades y sugerir medicamentos seguros a partir de los datos ingresados por el usuario.

2. **Diseñar interfaces de usuario funcionales y amigables:** Implementar interfaces intuitivas que permitan a los usuarios ingresar información clínica de manera clara, y consultar los diagnósticos generados de forma comprensible y visual.

3. **Documentar correctamente el desarrollo del sistema:** Elaborar la documentación técnica del proyecto, incluyendo manual de usuario, guías de instalación, estructura del archivo Prolog, pruebas realizadas y justificación de reglas activadas en el diagnóstico.

4. **Evaluar críticamente el modelo simbólico:** Analizar las limitaciones de los sistemas expertos basados en reglas frente al manejo de incertidumbre, la escalabilidad y los enfoques modernos de la inteligencia artificial (como machine Learning y agentes), mediante una reflexión comparativa basada en la experimentación con casos clínicos.

## 4. Enunciado del Proyecto

### 4.1 Descripción del problema a resolver

La falta de acceso inmediato a un diagnóstico médico preliminar, combinada con la presencia de enfermedades crónicas y alergias, representa un reto significativo en la atención sanitaria básica. Muchos pacientes no pueden identificar correctamente sus padecimientos ni saben qué tratamientos pueden o no utilizar. Esto puede derivar en complicaciones, automedicación riesgosa o tratamientos inadecuados.

Este proyecto propone el diseño e implementación de un sistema experto que, con base en lógica computacional, pueda analizar los síntomas, alergias y enfermedades preexistentes del usuario para generar un informe con posibles diagnósticos, el grado de afinidad con cada uno, y medicamentos recomendados evitando contraindicaciones.

El sistema será construido sobre un motor lógico desarrollado en Prolog, el cual, mediante reglas lógicas codificadas en un archivo .pl, podrá realizar inferencias sobre los datos ingresados por el usuario. Se busca que el sistema sirva como herramienta de orientación médica y educación, simulando el razonamiento de un especialista de salud a través de programación lógica.

### 4.2 Alcance del proyecto

El sistema inteligente médico por desarrollar, denominado MediLogic, estará compuesto por dos módulos principales: uno destinado a los usuarios pacientes y otro reservado para administradores o personal médico autorizado. Ambos módulos deberán estar integrados en una interfaz funcional, clara e intuitiva, junto con una lógica de inferencia implementada íntegramente en prolog.

#### Inicio

Al ingresar al sistema, los usuarios encontrarán una pantalla principal accesible sin autenticación. En ella se mostrará una descripción general del sistema y su funcionalidad, explicando que se trata de una herramienta de apoyo diagnóstico preliminar que no sustituye la consulta médica profesional. Desde esta pantalla, el usuario podrá elegir entre acceder al módulo de diagnóstico para pacientes o al módulo administrativo para personal médico, este último protegido mediante credenciales.

#### Pacientes

El módulo destinado a los usuarios pacientes permitirá ingresar información clínica básica a través de formularios interactivos. El sistema debe permitir seleccionar síntomas presentes a través de checkboxes, así como registrar alergias a medicamentos y enfermedades crónicas preexistentes como diabetes, hipertensión, enfermedades autoinmunes, entre otras.

Además, para mejorar la precisión del análisis y abordar parcialmente el manejo de incertidumbre en entornos médicos, el sistema deberá permitir que el usuario indique el nivel de severidad de cada síntoma (leve, moderado, severo). Esta severidad deberá influir mediante ponderaciones o factores de certeza dentro de las reglas en Prolog, evitando depender exclusivamente de heurísticas puramente deterministas y reflejando de mejor manera la incertidumbre clínica en el cálculo del porcentaje de afinidad.

**Criterio estándar para el cálculo de afinidad e incertidumbre:**

Para garantizar un criterio de evaluación homogéneo, el motor en Prolog deberá calcular el porcentaje de afinidad ponderando la severidad de los síntomas egresados de la siguiente manera:

- Síntoma leve: Ponderación base de 1 o 10% de peso en la regla.
- Síntoma moderado: Ponderación base de 2 o 20% de peso en la regla.
- Síntoma Severo: Ponderación base de 3 o 30% de peso en la regla.

El porcentaje final de afinidad para cada enfermedad se obtendrá mediante una relación matemática proporción entre los puntos acumulados por los síntomas coincidentes del usuario y el total máximo posible de los síntomas definidos para dicha enfermedad en la base de conocimiento, integrando así un manejo básico de incertidumbre y graduación clínica.

Una vez completado el ingreso de datos, el usuario podrá solicitar un análisis. El sistema, utilizando la base de conocimiento en prolog, realizará un proceso de inferencia lógica para determinar posibles enfermedades asociadas a los síntomas proporcionados. Estas enfermedades deberán ordenarse por porcentaje de coincidencia, expresado como nivel de afinidad entre el perfil del paciente y las características clínicas de cada enfermedad.

Además del diagnóstico, el sistema debe sugerir medicamentos adecuados para tratar cada una de las enfermedades listadas, siempre y cuando no estén contraindicados por las alergias o condiciones crónicas indicadas. En caso de conflictos entre tratamientos posibles y enfermedades coexistentes, el sistema deberá identificar estas incompatibilidades y excluir opciones que puedan representar un riesgo para el paciente, sugiriendo otro posible medicamento con el mismo fin, pero sin repercusiones para su estado de salud general.

Finalmente, el sistema deberá emitir una recomendación de acción para el usuario, indicando el nivel de urgencia con frases como: "Consulta médica inmediata sugerida", "Posible automanejo" u "Observación recomendada".

El informe que se genere debe incluir:

- Una lista de enfermedades sugeridas, ordenadas de mayor a menor probabilidad.
- El porcentaje de afinidad correspondiente a cada diagnóstico.
- El medicamento más seguro y efectivo propuesto, evitando riesgos por alergias o interacciones negativas.
- Una explicación detallada que indique qué reglas Prolog se activaron para llegar a las conclusiones presentadas.
- Un nivel de urgencia estimado para cada diagnóstico, con base en los síntomas y su severidad.
- Visualización clara de los resultados mediante tablas, secciones y gráficos explicativos como barras de afinidad o alertas de advertencia.

Adicionalmente, el sistema deberá mantener un historial local temporal de diagnósticos durante la sesión activa en el navegador, permitiendo que el paciente revise análisis anteriores mientras navega.

También deberá ofrecer la opción de descargar el informe en formato PDF, incluyendo la fecha, un resumen del diagnóstico, las advertencias importantes, los medicamentos sugeridos, las reglas activadas y el sello visual del sistema.

**Formulario de Ingreso Clínico del Paciente (Catálogos Dinámicos):** La interfaz del módulo de pacientes deberá contar con un formulario accesible sin autenticación que solicite y procese la información clínica de la siguiente manera:

1. **Selección de síntomas actuales:** Mediante checkboxes o listas de selección múltiple alimentadas dinámicamente desde el catálogo de síntomas de la base de conocimiento.
2. **Nivel de severidad:** Especificando por cada síntoma seleccionado su grado (Leve, Moderado o Severo) para el cálculo de afinidad.
3. **Registro de Alergias a Medicamentos:** Mediante checkboxes o listas de selección múltiple donde el paciente pueda indicar sus alergias. Este catálogo debe cargarse de forma dinámica consultando los medicamentos registrados previamente por el administrador.
4. **Registro de Enfermedades Crónicas / Antecedentes:** Un apartado para marcar padecimientos preexistentes. Este catálogo también debe poblarse de manera dinámica a partir de las enfermedades registradas en el sistema (por ejemplo, hipertensión, diabetes, etc.), permitiendo que el motor en Prolog ejecute correctamente las reglas cruzadas de contraindicación y filtrado de seguridad.

#### Administrador

El módulo administrativo estará protegido por autenticación y será accesible únicamente para usuarios con credenciales válidas. Este módulo ofrecerá un panel de control completo que permita gestionar la base de conocimientos del sistema en tiempo real, mediante formularios o interfaces estructuradas que no requieran editar manualmente el archivo .pl.

Desde este panel, el administrador podrá realizar las siguientes acciones:

- Crear, editar y eliminar enfermedades registradas en el sistema, incluyendo su nombre, descripción, síntomas asociados y medicamentos contraindicados.
- Registrar nuevos síntomas y asociarlos a enfermedades específicas mediante criterios de compatibilidad.
- Administrar medicamentos disponibles, indicando qué enfermedades pueden tratar y qué contraindicaciones presentan.
- Definir relaciones de contraindicación entre medicamentos, enfermedades crónicas y alergias.
- Clasificar enfermedades por sistema del cuerpo (respiratorio, digestivo, endocrino, etc.) o por tipo (viral, crónico, inmunológico), para facilitar su administración y consulta.
- Visualizar y exportar el archivo .pl actual con toda la base lógica del sistema.

Todos los cambios realizados mediante la interfaz administrativa deben reflejarse automáticamente en el archivo Prolog, asegurando así la persistencia, actualización y validez de las reglas y hechos registrados. Esta integración entre el frontend del sistema y la lógica declarativa debe garantizar que el motor de inferencia pueda utilizar los datos actualizados de forma inmediata.

Para evitar ambigüedades en el desarrollo, las contraindicaciones gestionadas por el administrador y evaluadas por el motor en Prolog deben contemplar **obligatoriamente dos niveles**:

- **Contraindicaciones con condiciones del paciente:** Restricciones cruzadas entre los medicamentos y las enfermedades crónicas o alergias registradas por el paciente (ej. evitar ciertos fármacos si el paciente es hipertenso o alérgico).
- **Contraindicaciones entre fármacos y patologías/tratamientos:** Relaciones de incompatibilidad directa que el administrador configure para asegurar que el motor lógico descarte opciones de riesgo y sugiera alternativas seguras.

**Automatización de funciones de administrador:**

Administrar la relación entre múltiples enfermedades puede ser un trabajo complejo, esto implica en tiempo valioso para el administrador que podría emplear en otras actividades. Por ello se solicita que se cree un RPA que ayude al administrador a crear nuevas enfermedades, llenando cada campo de forma automática por medio de un archivo proporcionado por el administrador, el cual debe contener los campos que se muestran en el json de ejemplo que se proporcionará. Además, se debe clasificar cada una de las enfermedades por sistema del cuerpo (respiratorio, digestivo, endocrino, etc.) o por tipo (viral, crónico, inmunológico), ya que estas tareas suponen la inversión de mucho tiempo para el usuario administrador.

**Actualización dinámica del archivo .pl:** Para simplificar la implementación del módulo administrativo sin que se requiera reiniciar la aplicación ni lidiar con bloqueos avanzados de hilos en pyswip, el mecanismo de actualización en caliente se gestionará de la siguiente manera:

1. Cuando el administrador cree, edite o elimine un registro desde la interfaz, el backend en Python deberá sobrescribir o actualizar directamente el archivo .pl en el disco con la nueva estructura de hechos y reglas.
2. Inmediatamente después de guardar los cambios en el archivo, el sistema ejecutará un comando de recarga en el motor lógico (por ejemplo, volviendo a invocar la consulta de carga o inicialización del archivo "consult/1" a través de pyswip). De esta forma, las siguientes consultas del módulo de pacientes utilizarán la base de conocimientos actualizada de manera inmediata y limpia.

**Generación de informe:** Luego de hacer esta carga, deberá generar un informe (en texto plano) para tener una bitácora de cambios hechos por el robot.

### 4.3 Requerimientos técnicos

Para el desarrollo del proyecto MediLogic, los estudiantes deberán emplear exclusivamente tecnologías permitidas. El objetivo es que los estudiantes comprendan, a profundidad, los fundamentos de la inteligencia artificial simbólica aplicada a través de un sistema web ligero y funcional.

Las herramientas y tecnologías requeridas son:

- **Lenguajes de programación:**
  El sistema debe ser desarrollado utilizando Python, utilizando las librerías Python, pyswip, PyAutoGUI. Esta libertad busca que el estudiante se enfoque en fortalecer los conocimientos en PROLOG y RPA.

- **Motor lógico:**
  Toda la lógica de conocimientos del sistema deberá estar implementada en Prolog utilizando cualquiera de las dos librerías proporcionados en clase (pyswip), ejecutándose sobre el lenguaje python. La base de conocimiento debe estar contenida exclusivamente en un archivo .pl, el cual incluirá hechos, reglas, y estructuras que representen los síntomas, enfermedades, medicamentos y sus relaciones lógicas.

- **Interfaz de Usuario:**
  Se espera una interfaz clara, amigable y accesible que permita a los usuarios interactuar con el sistema sin necesidad de conocimientos técnicos. Esta deberá facilitar el ingreso de información, el análisis automático y la visualización de los resultados generados por el motor lógico.

  La solución debe estar realizada sobre una arquitectura cliente-servidor, tomando siempre en cuenta que **la lógica de Prolog exclusivamente debe ser en Python**.

- **Control de versiones:**
  Todo el código fuente, documentación técnica y recursos del proyecto deberán alojarse en un repositorio de GitHub privado.

- **Licenciamiento:**
  El proyecto deberá tener una **licencia de software MIT**, claramente indicada en el repositorio. Una vez finalizado el semestre, el repositorio deberá hacerse público para fomentar el acceso abierto y la reutilización académica del código.

### 4.4 Entregables

| Tipo | Descripción |
|---|---|
| **Aplicación** | Aplicación funcional web. |
| **RPA** | Un video con el funcionamiento de la carga por medio del RPA, desde el inicio hasta el final del funcionamiento con al menos 3 enfermedades cargadas y categorizadas. Este se debe subir a **GitHub** embebido para que sea fácil de visualizar |
| **Manual Técnico** | Documento en PDF que incluya una explicación completa de la arquitectura del sistema, las herramientas utilizadas, la estructura del archivo .pl, el flujo de interacción entre los módulos, y los procesos lógicos implementados. También debe incluir una descripción detallada de las reglas definidas en prolog y su justificación, así como las decisiones tomadas en la construcción del sistema.<br><br>Agregar una sección en donde se pueda visualizar la configuración del Robot que automatice. No es necesario mostrar el funcionamiento (para eso está el video) pero si de la configuración se realizó para el correcto funcionamiento |
| **Manual de Usuario** | Documento destinado a los usuarios finales del sistema. Debe contener instrucciones paso a paso sobre el uso del módulo de pacientes y el módulo administrativo, incluyendo capturas de pantalla, posibles errores comunes, recomendaciones y advertencias. También debe explicar cómo interpretar los resultados presentados por el sistema y cómo utilizar el informe descargable en PDF.<br><br>*El manual de usuario para el RPA no es obligatorio, ya que es una herramienta automática, pero si agregar la información de como ejecutarlo. |
| **Código Fuente** | Repositorio de GitHub que contenga el código completo del proyecto: archivos fuente, el archivo .pl con la base lógica en prolog. El código debe estar organizado, debidamente comentado, y reflejar buenas prácticas de desarrollo y control de versiones. El repositorio debe mantenerse privado hasta su revisión, y hacerse público después de finalizar el semestre. |
| **Evaluación de coherencia diagnóstica y análisis crítico** | Documento adicional en el que se presenten al menos tres casos clínicos completos con datos de entrada (síntomas, alergias y enfermedades crónicas) y un análisis del resultado obtenido por el sistema. El estudiante deberá explicar si el diagnóstico fue coherente o no, justificando su respuesta. Adicionalmente, el documento debe incluir una sección de reflexión crítica obligatoria que contraste las limitaciones del sistema experto basado en reglas (IA simbólica) frente al manejo de incertidumbre, la escalabilidad y los modelos modernos de inteligencia artificial (como Machine Learning, modelos probabilísticos y agentes de IA). |

**Lineamientos para la Reflexión Crítica (Análisis Comparativo):**

La sección de reflexión crítica dentro del análisis de casos deberá tener una extensión mínima de **1 página** donde el estudiante aborde obligatoriamente los siguientes puntos:

1. **Limitaciones del enfoque simbólico:** Explicar cómo el motor de reglas estricto de Prolog maneja (o deja de manejar) la ambigüedad y los escenarios donde los síntomas no encajan en una regla determinista exacta.

2. **Comparativa con IA basada en datos (Machine Learning / Modelos probabilísticos):** Contrastar cómo un modelo estadístico o probabilístico calcularía una probabilidad de diagnóstico a partir de datos reales frente a las reglas fijas programadas.

3. **Escalabilidad y mantenimiento:** Reflexionar sobre qué ocurriría con el sistema si en lugar de unas cuantas enfermedades y síntomas se tuvieran miles, y cómo los enfoques modernos o agentes autónomos resuelven el crecimiento de la base de conocimiento.

- **Colaborador obligatorio en el repositorio:** *ixchop98* debe ser agregados al repositorio como colaborador con permisos de lectura completa.
- **Nombre del repositorio:** *IA1_2S2026_Carnet*.
- **Medio de entrega:** El enlace al repositorio a través de la plataforma UEDI

## 5. Metodología

El desarrollo del proyecto MediLogic deberá seguir una metodología estructurada que permita a los estudiantes organizar, ejecutar y documentar cada etapa de forma efectiva. Se recomienda la aplicación de metodologías ágiles, como **Personal SCRUM** (lista de tareas, planificación semanal, revisión diaria, revisión semanal), para la gestión del tiempo de forma efectiva y la entrega progresiva de avances.

A continuación, se describen las fases mínimas que los estudiantes deberán seguir durante el ciclo de desarrollo del proyecto:

1. **Investigación preliminar:** Los estudiantes deben realizar una revisión técnica sobre sistemas expertos médicos, lógica declarativa, motores de inferencia como prolog, y ejemplos de diagnóstico automatizado. También deberán estudiar las implicaciones de la sintaxis Prolog, su integración en python y buenas prácticas en el diseño de reglas.

2. **Diseño del sistema:** Se deben elaborar diagramas de flujo, maquetas de interfaz (mockups) y una representación inicial de la estructura del archivo .pl. En esta fase se definirán los síntomas, enfermedades, medicamentos, contraindicaciones y las reglas básicas de inferencia.

3. **Construcción de la interfaz:** Se desarrollará la aplicación según la arquitectura elegida utilizando exclusivamente Python para la lógica. Se implementará la navegación entre módulos, la captura de información del paciente, la comunicación con el motor Prolog y la presentación del informe de diagnóstico.

4. **Implementación del motor lógico:** Los estudiantes deberán desarrollar el archivo .pl que contendrá la base de conocimiento médica (hechos y reglas). Deberán aplicar lógica de predicados para vincular síntomas con enfermedades, validar contraindicaciones, y calcular el porcentaje de afinidad entre perfiles clínicos y diagnósticos.

5. **Integración del sistema:** Se conectará la interfaz desarrollada con el motor lógico, garantizando el flujo correcto de datos desde el ingreso de información hasta la generación del resultado. También se integrará el módulo administrativo, que permitirá modificar la base de conocimientos desde la interfaz sin intervenir directamente el archivo .pl.

6. **Pruebas funcionales y validación:** Se realizarán pruebas sistemáticas utilizando casos clínicos simulados para verificar el funcionamiento del sistema, la coherencia de los resultados y la activación correcta de las reglas. Esta fase también contempla el desarrollo del entregable de evaluación de coherencia diagnóstica, con al menos tres casos completos documentados.

7. **Documentación:** Los estudiantes deberán preparar el manual de usuario, el manual técnico, y el informe general del proyecto, detallando la estructura del sistema, la justificación de sus decisiones lógicas y tecnológicas, así como las dificultades enfrentadas durante el desarrollo.

8. **Presentación final:** Finalmente, los estudiantes presentarán su proyecto, demostrando su funcionamiento, explicando las reglas utilizadas y presentando los entregables requeridos. Se evaluará tanto la calidad técnica como la claridad en la presentación y defensa del trabajo.

## 6. Desarrollo de Habilidades Blandas

Para complementar el desarrollo técnico del sistema *MediLogic*, los estudiantes deberán fortalecer una serie de habilidades blandas que son fundamentales en el ámbito profesional. Estas habilidades permitirán mejorar la comunicación, la colaboración, el liderazgo y la capacidad de resolver problemas en entornos reales o simulados de desarrollo de software.

### 6.1 Proyectos Individuales

El proyecto representa una oportunidad para desarrollar autonomía y autoevaluación. Cada estudiante asumirá la totalidad de las fases del proyecto: investigación, desarrollo, pruebas y documentación.

#### 6.1.1 Autogestión del Tiempo

El estudiante deberá planificar sus tiempos de trabajo, dividir sus actividades por fases y cumplir con las fechas de entrega. Se espera el uso de cronogramas personales y técnicas de gestión de tareas como Pomodoro o Kanban.

#### 6.1.2 Responsabilidad y Compromiso

Al trabajar de forma independiente, el estudiante asume completa responsabilidad por la calidad y completitud del proyecto. Esto fomenta el compromiso con el aprendizaje autónomo, la ética profesional y la entrega de productos funcionales.

#### 6.1.3 Resolución de Problemas

El proyecto individual exige que el estudiante resuelva desafíos técnicos por su cuenta, lo que impulsa la creatividad, la investigación y la toma de decisiones lógica ante errores o problemas emergentes durante el desarrollo.

#### 6.1.4 Reflexión Personal

Al finalizar el proyecto, el estudiante deberá realizar una autoevaluación crítica en la que reflexione sobre lo aprendido, los retos enfrentados y las habilidades que necesita mejorar. Esta práctica promueve la mejora continua y la consolidación del conocimiento adquirido.

## 7. Cronograma

El desarrollo del proyecto MediLogic se organizará en fases clave para asegurar un progreso continuo y bien estructurado. Se realizarán dos entregas: la primera servirá para validar el avance inicial del sistema (estructura base, lógica preliminar y diseño), y la segunda corresponderá al proyecto completo, ya funcional y documentado.

| Tipo | Fecha Inicio | Fecha Fin |
|---|---|---|
| Asignación de Proyecto | 07/08/2026 | 07/08/2026 |
| Entrega No. 1 – Tarea 1 | 21/08/2026 | 21/08/2026 |
| Entrega No. 2 – Proyecto Final | 04/09/2026 | 04/09/2026 |
| Calificación | 05/09/2026 | 05/09/2026 |

**Detalle por entrega**

- **Entrega No. 1 – Tarea 1:** Esta entrega servirá para evaluar el avance inicial del proyecto. Se espera que los estudiantes presenten una versión preliminar del sistema, que incluya el diseño de la interfaz, el archivo .pl con hechos básicos y algunas reglas ya funcionales, así como la estructura del repositorio GitHub y documentación inicial (borrador del manual técnico o de usuario).

- **Entrega No. 2 – Proyecto Final:** Corresponde a la versión final del sistema MediLogic, completamente funcional, con todos los módulos implementados, pruebas realizadas y documentación completa.

## 8. Rúbrica de Calificación

### 8.1 Requisitos para optar a la calificación

Antes de ser evaluado, el proyecto deberá cumplir con los siguientes requisitos mínimos. Si alguno de estos no se cumple, el proyecto no podrá ser calificado y se considerará como no entregado o incompleto:

| Tema | Descripción | Cumple (Sí/No) |
|---|---|---|
| Cumplimiento de la tecnología establecida | El desarrollo debe haberse realizado utilizando únicamente con Prolog y Python como "backend", no se permite otro lenguaje de programación | |
| Uso de herramientas requeridas | El sistema debe estar publicado en GitHub Pages y gestionado mediante un repositorio en GitHub con control de versiones adecuado. | |
| Gestión y entregas del proyecto | Se deben haber entregado ambas fases (avance y entrega final) dentro de las fechas establecidas en el cronograma. Todas las versiones deben estar registradas. | |
| Documentación obligatoria | Se deben entregar el manual de usuario, el manual técnico, todos debidamente elaborados. El informe técnico debe contener diagramas. | |
| Evaluación de coherencia diagnóstica | Debe incluir al menos tres casos clínicos analizados junto con la reflexión crítica comparativa sobre IA simbólica vs. IA moderna, respaldando los resultados generados por el sistema. | |

### 8.2 Resumen de Puntuaciones

| Área | Puntos Totales | Puntos Obtenidos |
|---|---|---|
| **1. Conocimiento** | | |
| Interfaz de Usuario | 5 | |
| Módulo de Paciente | 30 | |
| Modulo del Administrador | 25 | |
| Automatización robótica de procesos (RPA) | 30 | |
| **Sub-Total** | **90** | |
| **2. Habilidades** | | |
| Documentación (Manuales y reflexión crítica comparativa) | 5 | |
| Preguntas | 5 | |
| **Sub-Total** | **10** | |
| **TOTAL** | **100** | |

### 8.3 Detalle de la Calificación

| Descripción de Ponderación | Valor | Observación | Punteo |
|---|---|---|---|
| **1. Conocimiento** | | | |
| **Interfaz de Usuario** | **5** | Interfaz clara, amigable y apegada a los requerimientos | |
| **Módulo del Paciente** | **30** | | |
| Formulario para ingreso de síntomas, enfermedades crónicas y alergias | 4 | Completo, validado y funcional | |
| Registro de severidad de síntomas e impacto en el diagnóstico | 1 | Interfaz implementada correctamente | |
| Hechos en Prolog de enfermedades, síntomas y medicamentos | 2 | Definidos correctamente en el archivo .pl | |
| Reglas en Prolog para diagnóstico basado en afinidad y contraindicaciones | 6 | Precisas, funcionales y bien estructuradas | |
| Presentación lógica y gráfica del informe de diagnóstico | 6 | Resultados claros, ordenados y visuales | |
| Generación de nivel de urgencia según perfil clínico (leve/moderado/severo) | 5 | Diagnóstico incluye recomendación de acción | |
| Sugerencia segura de medicamentos evitando conflictos con alergias/enfermedades | 6 | Valida condiciones correctamente | |
| **Módulo del Administrador** | **25** | | |
| Gestión de enfermedades, síntomas y clasificación por sistemas o tipo | 8 | Crear, editar, eliminar correctamente | |
| Gestión de medicamentos y definición de contraindicaciones | 8 | Interfaz funcional y reglas aplicadas | |
| Gestión del archivo .pl (carga y descarga, integración lógica en tiempo real) | 6 | Sin errores, lectura y escritura funcional | |
| Interfaz de administración funcional y comprensible | 3 | Fluida, ordenada y alineada con requerimientos | |
| **RPA** | **30** | | |
| Carga de archivo TXT con las enfermedades | 5 | Se carga correctamente el archivo txt con las enfermedades | |
| Generación de Texto Plano | 10 | Informe con los detalles de la carga | |
| RPA del lado del backend | 5 | El RPA debe estar desarrollado del lado de backend | |
| Desarrollo de RPA en python | 5 | El RPA debe estar desarrollado en python | |
| Video RPA funcionando | 5 | Se muestra comportamiento funcional de la automatización | |
| **2. Habilidades** | **10** | | |
| **Documentación** | **5** | | |
| Manual Técnico (estructura, reglas, uso de Prolog, decisiones de diseño) | 2 | Completo y detallado | |
| Manual de Usuario (paso a paso, capturas, explicación de resultados) | 1 | Claro y orientado al usuario final | |
| Evaluación de coherencia diagnóstica (3 casos clínicos analizados y justificados y reflexión IA simbólica vs moderna) | 2 | Evaluación técnica, análisis de casos y profundidad en la reflexión crítica comparativa frente a modelos basados en datos y Machine Learning | |
| **Preguntas** | **5** | | |
| Pregunta 1 | 1 | Pregunta teórica o sobre el desarrollo del proyecto | |
| Pregunta 2 | 1 | Pregunta teórica o sobre el desarrollo del proyecto | |
| Pregunta 3 | 1 | Pregunta teórica o sobre el desarrollo del proyecto | |
| Pregunta 4 | 1 | Pregunta teórica o sobre el desarrollo del proyecto | |
| Pregunta 5 | 1 | Pregunta teórica o sobre el desarrollo del proyecto | |
| **Penalizaciones** | | | |
| Entrega fuera del plazo establecido | -20 | Solo si se entrega fuera del plazo oficial (En caso de que la calificación sea mucho tiempo después de la entrega la penalización puede ser mayor). | |
| Impuntualidad en la calificación | -20 | En caso de impuntualidad en la calificación. | |
| **TOTAL** | **100** | | |

### 8.4 Valores

En el desarrollo del proyecto MediLogic, se espera que los estudiantes demuestren un alto nivel de honestidad académica, responsabilidad ética y compromiso profesional. El cumplimiento de los principios que se detallan a continuación será obligatorio y cualquier incumplimiento será sancionado conforme a las normativas vigentes de la Escuela de Ciencias y Sistemas.

1. **Originalidad del Trabajo**
   Cada estudiante o equipo debe desarrollar su propio código, archivo Prolog (.pl), documentación técnica y recursos asociados. Se espera que el trabajo entregado sea producto del conocimiento adquirido en el curso y del esfuerzo auténtico de sus autores.

2. **Prohibición de Copias y Plagio**
   Queda estrictamente prohibido copiar, replicar o adaptar total o parcialmente el código, documentación, lógica en Prolog o cualquier componente del proyecto desde otras fuentes sin el debido análisis, modificación y referencia.

   - La detección de plagio (entre compañeros, de internet o de ciclos anteriores) será penalizada con calificación de 0 puntos.
   - Los responsables serán **reportados formalmente a la Escuela de Ciencias y Sistemas**.
   - Esto incluye el uso de ediciones superficiales de código ajeno, sin comprensión real ni justificación lógica.

3. **Uso Responsable de Recursos Externos**
   Está permitido el uso de bibliotecas de consulta, ejemplos o fragmentos educativos siempre y cuando:

   - Se referencien adecuadamente en el código o en los anexos.
   - Se comprenda completamente su funcionamiento.
   - No se utilicen como sustituto de la lógica propia del proyecto. Cualquier duda deberá ser consultada con el catedrático o auxiliar antes de su uso.

4. **Revisión y Validación del Trabajo**
   El equipo docente podrá utilizar herramientas automáticas y revisiones manuales para comparar entregas y detectar similitudes no justificadas.

   - En caso de sospecha, el estudiante deberá defender su solución, explicar sus decisiones y justificar el funcionamiento de su código y archivo Prolog.
   - Si no logra demostrar la autoría o comprensión del trabajo, se asignará **una calificación de 0 puntos**, sin opción a apelación académica.

5. **Licencia y Transparencia del Proyecto**
   - El proyecto debe ser **OpenSource** bajo licencia **MIT**.
   - Todo el código, archivos .pl, documentación técnica, pruebas y manuales deberán estar alojados en un repositorio de GitHub privado durante el desarrollo.
   - Una vez calificado, el repositorio deberá hacerse público, agregado como colaborador en el repositorio.

6. **Entrega y Fechas Límite**
   - No se permitirá realizar modificaciones al código ni a la documentación después de la fecha de entrega final establecida en el cronograma.
   - Las entregas fuera del plazo establecido pueden considerarse no válidas y se aplicarán las penalizaciones indicadas, a menos que se haya aprobado una prórroga justificada con anterioridad.
