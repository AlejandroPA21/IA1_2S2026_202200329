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

## 14. Cierre para la Entrega No. 2: automatización visual del RPA con PyAutoGUI

La Entrega No. 1 dejó documentado (punto 13) que `admin_rpa.py` automatizaba el alta
llamando directo a `KnowledgeStore`, sin operar la interfaz con PyAutoGUI. Para la entrega
final se agregó `src/rpa/gui_automation.py` (mas el punto de entrada
`scripts/ejecutar_rpa_gui.py`), que sí controla el mouse/teclado real sobre la página web,
que es lo que exige el enunciado y lo que debe quedar grabado en el video de evidencia.

Se descartó el enfoque más común de PyAutoGUI (coordenadas de pantalla fijas o
`locateOnScreen` con capturas de referencia) porque es frágil ante cualquier cambio de
resolución, zoom o tamaño de ventana, y porque habría exigido calibrar coordenadas por
equipo. En su lugar se diseñó una automatización 100% por teclado:

- Se agregó el atributo HTML `autofocus` al primer campo de los formularios "Nuevo síntoma",
  "Nuevo medicamento" y "Nueva enfermedad" (el de login ya lo tenía), así el navegador deja
  el cursor listo apenas carga la página, sin necesidad de ningún clic.
- La navegación entre páginas usa Ctrl+L (barra de direcciones) + URL + Enter en vez de
  clics sobre el menú lateral, y por eso funciona igual en cualquier navegador/resolución.
- Los `<select>` (sistema del cuerpo / tipo) se resuelven con Home + flecha abajo repetida
  N veces (N = índice del valor buscado en `SISTEMAS_CUERPO`/`TIPOS_ENFERMEDAD`), en vez de
  depender del "type-ahead" del navegador, cuyo comportamiento exacto varía entre Chrome,
  Edge y Firefox.
- Los checkboxes de síntomas/medicamentos contraindicados se alcanzan contando cuántas veces
  presionar Tab desde el primero de la lista; ese conteo se calcula leyendo el catálogo real
  (con una instancia de `PrologEngine` **de solo lectura**, nunca escribe nada) justo antes
  de llenar cada enfermedad, aprovechando que la plantilla siempre los renderiza en orden
  alfabético (`knowledge_store.py`). El robot "sabe" dónde está cada casilla porque conoce el
  estado real de la base de conocimiento, no porque tenga memorizada una posición en píxeles.
- Todo el texto que se escribe en un campo se pega desde el portapapeles (`pyperclip` +
  Ctrl+V) en vez de tecla por tecla: `pyautogui.write()` no soporta de forma confiable
  acentos/eñes del español, y el portapapeles preserva cualquier carácter Unicode.

El modo rápido (`rpa/admin_rpa.py::ejecutar_carga`, ligado al botón "Ejecutar RPA" del panel)
se conservó tal cual: sigue siendo el camino confiable para uso diario del administrador
(no depende de que el navegador tenga foco de teclado real), mientras que
`gui_automation.py` es específicamente la prueba de automatización con PyAutoGUI que pide la
rúbrica. Ambos generan bitácoras en texto plano con el mismo formato (`ReporteRPA`).

**Sobre el formato del archivo de carga ("TXT" en la rúbrica vs. JSON en el enunciado):** el
enunciado (sección 4.2) describe el archivo de origen citando expresamente "el json de
ejemplo que se proporcionará" (`EjemploRPA.json`), mientras que la rúbrica (sección 8.3) lo
nombra genéricamente "archivo TXT". Se interpretó JSON como un archivo de texto plano válido
(lo es, y es el único formato de ejemplo que la cátedra entregó) y no se agregó un segundo
parser para un formato TXT no especificado, para no introducir una estructura de datos
inventada sin referencia oficial.

## 15. Se evaluó y se descartó ampliar el catálogo con una quinta enfermedad

Durante la validación final se detectó que, con las 4 enfermedades originales, ningún caso
real llega a activar `contraindicado_por_cronica/2` (nivel "condiciones del paciente" de la
sección 10 del `.pl`): ningún medicamento de `medicamento_para/2` está también en
`contraindicacion_enfermedad/2` contra una enfermedad *distinta* a la que trata. Se probó
agregar una quinta enfermedad ("migraña") vía el CRUD administrativo para forzar un caso real
de ese camino de la regla. Se revirtió esa prueba antes de la entrega por dos motivos:

1. **Reescritura no determinista del orden de los hechos:** cualquier alta/edición desde el
   CRUD reescribe las secciones de hechos del `.pl` en orden alfabético
   (`knowledge_store.py::_render_pares`), sin importar el orden original en que se escribieron
   a mano. Eso reordenó también `medicamento_para(_, hipertension)` (de `losartan, enalapril`
   a `enalapril, losartan`), lo que cambia silenciosamente cuál candidato es "el primero" en
   `medicamento_sugerido/4` para consultas que no dependen de "migraña" en absoluto.
   Confirmarlo así, con una prueba concreta, es en sí mismo un hallazgo útil: **cualquier**
   edición administrativa, no solo esta, puede alterar cuál medicamento se sugiere quede
   como caso base — algo a tener presente si se compara la salida del sistema contra
   evidencia capturada previamente (capturas de pantalla, informes en PDF ya generados, etc.).
2. **Consistencia con la evidencia ya capturada:** las capturas de
   `docs/informe_prolog/imagenes/` y los ejemplos citados en este documento, en el manual
   técnico y en `scripts/demo_prolog.pl` corresponden al catálogo original de 4 enfermedades.
   Agregar una quinta enfermedad que comparte el síntoma "dolor de cabeza" habría cambiado
   permanentemente la salida de las consultas de referencia (`diagnosticar/2`, `informe/4`)
   frente a esas capturas ya tomadas, generando una inconsistencia evitable entre "lo que
   muestra la evidencia" y "lo que hace el código" para un caso que no aportaba tanto como
   para justificar ese riesgo.

Se optó, en cambio, por **documentar el hallazgo honestamente** como parte del entregable de
evaluación de coherencia (`docs/evaluacion_coherencia/evaluacion_coherencia.md`): la regla
`contraindicado_por_cronica/2` está correctamente implementada y es simétrica con
`contraindicado_por_alergia/2`, pero el catálogo que trae el proyecto no genera ningún caso
real que la dispare — una limitación real del sistema tal como se entrega, más valiosa de
reportar que de "maquillar" agregando datos solo para forzar una ejecución positiva. Sí quedó
como remanente útil de este experimento la corrección de un error real que reveló: el JSON de
ejemplo (`EjemploRPA.json`) tenía un typo (`sed_excessiva` en vez de `sed_excesiva`) que, al
volver a cargarse por el RPA, generaba un síntoma duplicado en el catálogo; se corrigió el
JSON para que una futura recarga no reintroduzca ese duplicado.

## 16. Entorno de desarrollo: instalación de SWI-Prolog y `.gitignore`

Para poder validar el proyecto de punta a punta en esta sesión de cierre (pytest, demos y
los casos clínicos con salidas reales) se instaló SWI-Prolog 10.0.2 (vía el instalador
oficial, modo silencioso) y se creó el entorno virtual `.venv` con `pip install -r
requirements.txt`. De paso se detectó que, al correr `python src/backend/app.py` desde la
raíz del repo (tal como indica el README), Flask resuelve la carpeta `instance/` en la raíz
del proyecto y no en `src/backend/instance/` como asumía el `.gitignore` original; se agregó
también `/instance/` al `.gitignore` para cubrir ambos casos.

## 17. Soporte del campo opcional `tratamiento_recomendado` en el RPA

Durante el cierre del proyecto aparecieron en el repositorio dos archivos de referencia
adicionales: `Ejemplo Archivo RPA V2.json` (una variante de `EjemploRPA.json` que agrega un
campo `tratamiento_recomendado` por enfermedad) y `Escenarios Proyecto 1.txt` (una guía de
los escenarios esperados para el módulo de paciente y para el RPA — éxito, conflicto/sustitución,
síntomas insuficientes; y, para el RPA, carga exitosa vs. fallo de formato controlado). El
formato original (`EjemploRPA.json`, y el listado de campos de `Escenarios Proyecto 1.txt`) no
incluye ese campo, así que se agregó como **opcional**, sin romper compatibilidad con el
formato original:

- `KnowledgeStore.cargar_enfermedad_rpa` acepta un parámetro opcional
  `medicamentos_tratamiento`; si se recibe, además de crear/actualizar la enfermedad, registra
  `medicamento_para/2` para cada medicamento indicado (dando de alta en el catálogo general
  cualquier medicamento nuevo) usando el nuevo método `agregar_tratamiento` (análogo a
  `agregar_contraindicacion`, pero para la relación de tratamiento).
- `rpa/admin_rpa.py::ejecutar_carga` (modo rápido) lee `registro.get("tratamiento_recomendado")`
  y lo pasa tal cual — `None` si el campo no existe, que es el comportamiento de siempre.
- **Alcance del RPA visual (`gui_automation.py`):** se decidió **no** automatizar este campo
  opcional en el modo con PyAutoGUI. Asignar tratamientos vía interfaz implica navegar al
  formulario específico de cada medicamento en la página "Medicamentos" (una tarjeta por
  medicamento, con su propia lista de checkboxes de enfermedades) — a diferencia del
  formulario "Nueva enfermedad", esa página no tiene un campo de texto al inicio de cada
  tarjeta para anclar con `autofocus`, y el número de tarjetas/casillas que preceden a la del
  medicamento objetivo varía con el tamaño del catálogo, lo que habría obligado a volver a
  depender de coordenadas de pantalla (justo lo que el diseño del RPA visual evita
  deliberadamente, ver punto 14). El modo visual cubre los campos requeridos según
  `Escenarios Proyecto 1.txt` (nombre, descripción, síntomas, medicamentos contraindicados,
  sistema del cuerpo); el tratamiento recomendado, cuando se usa el formato V2, se completa
  con el modo rápido o manualmente desde "Medicamentos" tras la carga visual.

Se agregó `tests/test_rpa.py` cubriendo los tres escenarios: carga exitosa con el formato
original (actualiza sin duplicar), carga con `tratamiento_recomendado` (verifica
`medicamento_para/2` real), y un archivo con un registro incompleto (falla controlada: se
reporta como error en la bitácora sin detener el resto de la carga).

---
*Este documento se irá actualizando conforme surjan nuevas decisiones técnicas durante el
desarrollo del proyecto.*
