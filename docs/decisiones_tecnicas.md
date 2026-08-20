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

---
*Este documento se irá actualizando conforme surjan nuevas decisiones técnicas durante el
desarrollo del proyecto.*
