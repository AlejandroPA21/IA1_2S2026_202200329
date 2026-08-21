# Bitácora de decisiones técnicas — MediLogic

Este documento registra decisiones técnicas menores tomadas de forma autónoma durante el
desarrollo, junto con su justificación, tal como lo pide la rúbrica en el criterio de
"aplicación de valores" (explicar qué reglas/hechos/decisiones se implementaron y por qué).

## 1. Framework web: Flask

Se eligió **Flask** sobre Django u otras alternativas porque:

- El enunciado pide una "arquitectura cliente-servidor" ligera, no un CMS completo.
- Flask permite exponer rutas simples para los módulos de paciente y administrador,
  dejando toda la lógica de negocio real en Prolog (tal como exige el enunciado: *"la
  lógica de Prolog exclusivamente debe ser en Python"*, es decir, Python solo actúa como
  puente hacia el motor lógico, no como motor de reglas paralelo).
- Es la opción más común enseñada junto con `pyswip` en cursos de sistemas expertos, y
  minimiza dependencias innecesarias.

## 2. Librería de integración con Prolog: pyswip

El enunciado menciona dos opciones (`pyswip` y `pytholog`) pero solo detalla `pyswip`
como la librería vista en clase para conectar con SWI-Prolog. Se eligió **pyswip** porque:

- Se apoya directamente sobre el intérprete real de SWI-Prolog (`consult/1`, `query/1`),
  lo cual es indispensable para el mecanismo de recarga en caliente del archivo `.pl`
  que pide el enunciado (sobrescribir el archivo y volver a hacer `consult`).
- `pytholog` es un motor de inferencia reimplementado en Python puro, lo que se aleja del
  requerimiento explícito de "un archivo .pl" con sintaxis Prolog real.

## 3. RPA: PyAutoGUI (backend)

El enunciado exige que el RPA se ejecute **del lado del backend** y esté **desarrollado en
Python**. Se eligió **PyAutoGUI** (en vez de TagUI, mencionado solo en la sección de
competencias) porque permite automatizar directamente la interfaz web propia del panel de
administrador desde un script Python ejecutado en el servidor/máquina del administrador,
sin depender de un runtime adicional (Node/TagUI). El script leerá el archivo JSON de
enfermedades (ver `EjemploRPA.json`) y completará el formulario de alta de enfermedades de
forma automática, clasificando cada una por sistema del cuerpo/tipo, y al finalizar
generará una bitácora en texto plano.

## 4. Generación de PDF: ReportLab

Para el informe de diagnóstico descargable en PDF (fecha, resumen, advertencias,
medicamentos, reglas activadas, sello visual) se eligió **ReportLab** por ser una librería
Python pura, sin dependencias binarias externas (a diferencia de `weasyprint`, que requiere
GTK en Windows), lo que simplifica la instalación en el entorno de desarrollo.

## 5. Estructura de carpetas

```
src/
  prolog/     -> Único archivo .pl con la base de conocimiento (hechos y reglas).
  backend/    -> Aplicación Flask (rutas, plantillas, integración con pyswip).
  rpa/        -> Script(s) de automatización del módulo administrador.
docs/         -> Manual técnico, manual de usuario, mockups, diagramas, evaluación de
                 coherencia diagnóstica.
tests/        -> Pruebas automatizadas.
```

Se separan `prolog/`, `backend/` y `rpa/` en paquetes independientes dentro de `src/` para
que cada componente pueda documentarse y probarse por separado, reflejando la separación de
responsabilidades que pide el enunciado (interfaz vs. motor lógico vs. automatización).

## 6. Sobre el requisito de "GitHub Pages" (sección 8.1 de la rúbrica)

GitHub Pages solo sirve contenido estático, pero MediLogic requiere un backend Python con
`pyswip` (que a su vez depende del runtime nativo de SWI-Prolog) y no puede ejecutarse como
sitio estático. Se documenta esta limitación aquí para resolverla explícitamente antes de
la entrega: se evaluará publicar en GitHub Pages únicamente material estático (por ejemplo,
documentación o una landing page informativa) mientras la aplicación funcional se ejecuta
localmente o en un servicio de hosting compatible con Python, y se consultará con el
catedrático/auxiliar si es necesario aclarar este punto antes de la entrega final.

## 7. Persistencia de datos administrados

El enunciado indica que los cambios del administrador deben reflejarse "automáticamente en
el archivo Prolog" y que el archivo `.pl` es la única fuente de la base de conocimiento (no
se pide una base de datos relacional aparte). Por lo tanto, el backend reescribirá
directamente `src/prolog/knowledge_base.pl` como mecanismo único de persistencia, sin
introducir una base de datos adicional, evitando duplicar la fuente de verdad.

## 8. Interpretación del "total máximo posible" en el cálculo de afinidad

El enunciado (sección 4.2) pide que la afinidad sea "una proporción entre los puntos
acumulados por los síntomas coincidentes del usuario y el total máximo posible de los
síntomas definidos para dicha enfermedad", sin especificar exactamente qué es ese máximo.
Se definió como: *la cantidad de síntomas asociados a la enfermedad, multiplicada por el
peso del nivel "severo" (3)*, es decir, el escenario en el que el paciente presentara todos
los síntomas de esa enfermedad en su grado más alto. Es la única interpretación que hace que
100% de afinidad sea alcanzable y tenga sentido clínico. Implementado en
`puntos_maximos_enfermedad/2` dentro de `src/prolog/knowledge_base.pl`.

## 9. Umbrales de nivel de urgencia

El enunciado exige un nivel de urgencia con frases como "Consulta médica inmediata
sugerida", "Posible automanejo" u "Observación recomendada", pero no fija los cortes
numéricos. Se definieron los siguientes umbrales sobre el porcentaje de afinidad, por ser
proporcionales y fáciles de justificar ante el catedrático:

| Rango de afinidad | Nivel  | Recomendación |
|---|---|---|
| ≥ 60% | Alta  | Consulta médica inmediata sugerida |
| 20% – 59% | Media | Posible automanejo |
| < 20% | Baja  | Observación recomendada |

Implementado en `nivel_urgencia/3`. Estos umbrales podrán ajustarse en la Entrega No. 2 si,
al probar más casos clínicos, se determina que otro corte refleja mejor la realidad.

## 10. Validación del archivo .pl

El archivo `src/prolog/knowledge_base.pl` fue probado de dos formas antes de darse por
terminado como entregable:

1. Directamente con `swipl` (instalado vía `winget install SWI-Prolog.SWI-Prolog`),
   ejecutando 9 consultas de prueba que cubren cálculo de afinidad, nivel de urgencia,
   sustitución de medicamento por alergia y por enfermedad crónica, orden de diagnósticos,
   catálogos derivados (`alergia/1`, `enfermedad_cronica/1`) y exclusión correcta de
   enfermedades sin síntomas coincidentes. Los 9 casos pasaron.
2. A través de `pyswip` (la librería que usará el backend real), confirmando que
   `Prolog().consult(...)` y las consultas `afinidad/3` e `informe/4` funcionan igual desde
   Python que desde la consola de SWI-Prolog.

## 11. Reescritura segura del `.pl`: marcadores `AUTO:<seccion>`

Para que el panel de administrador pueda "sobrescribir o actualizar directamente el archivo
`.pl` en el disco" (sección 4.2) sin arriesgar las reglas de inferencia, cada una de las 6
secciones de **hechos** de `knowledge_base.pl` (síntomas, medicamentos, enfermedades y las
tres relaciones) quedó delimitada con comentarios `% === AUTO:<seccion> START/END ===`.
`src/backend/knowledge_store.py` es el único módulo que escribe en el archivo: en cada
alta/edición/baja, lee el estado completo vía consultas reales a `PrologEngine` (nunca
reinterpretando el texto), lo modifica en memoria y reemplaza únicamente el contenido entre
esos marcadores con una expresión regular, dejando intactas las reglas (secciones 7 en
adelante) y los comentarios explicativos. Después llama a `PrologEngine.reload()` para que
el `consult/1` en caliente use la base actualizada de inmediato.

## 12. Autenticación del administrador

El enunciado exige que el módulo administrativo esté "protegido por autenticación" sin
detallar el mecanismo. Se implementó autenticación simple basada en sesión de Flask
(`session["admin_autenticado"]`) contra un usuario/contraseña únicos, configurables por
variables de entorno (`ADMIN_USER` / `ADMIN_PASSWORD`, con valores por defecto documentados
en el `README.md`) en vez de una tabla de usuarios en base de datos, coherente con la
decisión de no introducir persistencia adicional fuera del archivo `.pl` (ver punto 7). Es
una solución intencionalmente mínima para un proyecto académico de un solo administrador;
quedaría documentada como limitación de seguridad conocida frente a un entorno de
producción real (contraseña en texto plano en variables de entorno, sin hashing ni límite de
intentos).

## 13. Clasificación automática de "tipo" en el RPA

El JSON de origen (`EjemploRPA.json`) no incluye el campo "tipo" de enfermedad
(crónico/viral/bacteriano/inmunológico) que sí exige `knowledge_base.pl`; el enunciado pide
que el RPA "clasifique cada enfermedad... por sistema del cuerpo o por tipo", precisamente
para ahorrarle ese trabajo repetitivo al administrador. Se implementó una clasificación por
palabras clave sobre la descripción (`clasificar_tipo` en `src/rpa/admin_rpa.py`), con
"crónico" como valor por defecto cuando ninguna palabra clave aplica (en un catálogo de
diagnóstico preliminar, una condición que no se describe explícitamente como
infecciosa/autoinmune/bacteriana suele ser crónica). Es una heurística deliberadamente
simple y **no infalible**: la bitácora en texto plano deja constancia de la clasificación
asignada a cada enfermedad para que el administrador la audite, y puede corregirla en
cualquier momento desde el formulario manual de "Enfermedades" sin perder el resto de la
carga.

**Alcance de esta versión del RPA:** `ejecutar_carga` automatiza el alta completa (lectura
del JSON, clasificación, escritura en `knowledge_base.pl` y generación de bitácora)
invocando la misma capa de persistencia (`KnowledgeStore`) que usa el formulario manual del
administrador, garantizando resultados idénticos a un alta hecha a mano. La automatización
de la interfaz gráfica en sí (PyAutoGUI moviendo el mouse/tecleando sobre la pantalla del
navegador para llenar el formulario campo por campo) queda pendiente para cuando se grabe el
video de evidencia de la Entrega No. 2, ya que requiere una sesión gráfica real no disponible
en el entorno donde se desarrolló y probó esta base.

---
*Este documento se irá actualizando conforme surjan nuevas decisiones técnicas durante el
desarrollo del proyecto.*
