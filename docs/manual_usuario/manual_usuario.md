# Manual de Usuario — MediLogic

**Curso:** Inteligencia Artificial 1 — Universidad San Carlos de Guatemala
**Proyecto:** MediLogic — Entrega No. 2, Proyecto Final

> Antes de exportar a PDF: reemplaza cada `[CAPTURA: ...]` por una captura real de tu
> pantalla en ese punto del flujo (con `python src/backend/app.py` corriendo).

MediLogic es una herramienta de **apoyo diagnóstico preliminar**. No sustituye la consulta
médica profesional: ante síntomas de urgencia, acude siempre a un servicio de salud.

## 1. Cómo iniciar la aplicación

1. Instala [SWI-Prolog](https://www.swi-prolog.org/) (necesario para `pyswip`).
2. `pip install -r requirements.txt` (idealmente dentro de un entorno virtual `.venv`).
3. `python src/backend/app.py` y abre `http://127.0.0.1:5000/` en tu navegador.

[CAPTURA: pantalla de inicio, con los dos botones "Soy paciente" y "Acceso administrador"]

## 2. Módulo de Paciente

No requiere iniciar sesión. Desde el inicio, presiona **"Soy paciente — Iniciar
diagnóstico"**.

### 2.1 Formulario de ingreso clínico

1. **Síntomas actuales:** marca cada casilla que corresponda; al marcarla se habilita un
   selector de severidad (Leve / Moderado / Severo) — indícala con criterio, porque el
   cálculo de afinidad depende de ella (leve pesa menos que severo).
2. **Alergias a medicamentos:** marca los medicamentos a los que eres alérgico. Este listado
   lo llena el administrador; si no ves un medicamento, es porque aún no está registrado.
3. **Enfermedades crónicas / antecedentes:** marca tus condiciones preexistentes (ej.
   hipertensión, diabetes). El sistema las usa para descartar medicamentos contraindicados
   contra esas condiciones, no solo contra la enfermedad diagnosticada.
4. Presiona **"Solicitar análisis"**.

[CAPTURA: formulario de paciente con algunos síntomas y severidades marcadas]

### 2.2 Cómo interpretar el informe de resultados

Por cada enfermedad compatible con tus síntomas verás una tarjeta con:

- **Nombre de la enfermedad** y **% de afinidad** (barra de progreso): qué tan bien coinciden
  tus síntomas, ponderados por severidad, con el perfil de esa enfermedad.
- **Etiqueta de urgencia** (color): 🔴 alta = "Consulta médica inmediata sugerida" (afinidad
  ≥60%), 🟠 media = "Posible automanejo" (20–59%), 🟢 baja = "Observación recomendada" (<20%).
- **Medicamento sugerido:** el más seguro disponible para esa enfermedad, ya descartando
  cualquiera contraindicado por tus alergias o enfermedades crónicas. Si no hay ninguno
  seguro, verás "Ningún medicamento seguro disponible" — es una respuesta intencional, no un
  error: significa que **ningún** medicamento registrado para esa enfermedad es seguro para
  tu perfil, y debe evaluarlo un médico.
- **Reglas Prolog activadas:** el detalle técnico (afinidad, nivel de urgencia y sustitución
  de medicamento) que el motor lógico evaluó para llegar a esa conclusión.

Los diagnósticos aparecen ordenados de mayor a menor afinidad.

[CAPTURA: informe de resultados con al menos un diagnóstico y sus reglas activadas]

### 2.3 Historial de la sesión

Al final del informe hay una tabla con los diagnósticos anteriores de **esta misma sesión de
navegador** (hora, diagnóstico principal, afinidad). Es temporal: vive en `sessionStorage` del
navegador, nunca se envía al servidor, y se pierde al cerrar la pestaña.

### 2.4 Descargar el informe en PDF

Presiona **"⬇ Descargar informe en PDF"** en la parte superior del informe. El PDF incluye
fecha de generación, los datos ingresados, cada diagnóstico con su afinidad/urgencia/medicamento,
las reglas Prolog activadas y el sello del sistema.

## 3. Módulo de Administrador

Accede desde **"Acceso administrador"** en el inicio. Credenciales por defecto: usuario
`admin`, contraseña `medilogic2026` (configurables con las variables de entorno `ADMIN_USER`
/ `ADMIN_PASSWORD` — ver `README.md`).

[CAPTURA: pantalla de login del administrador]

### 3.1 Panel general

Muestra un resumen (enfermedades, síntomas y medicamentos registrados) y accesos rápidos a
cada sección.

### 3.2 Gestión de enfermedades

En **Enfermedades** puedes crear, editar o eliminar una enfermedad: nombre, sistema del
cuerpo, tipo (crónico/viral/bacteriano/inmunológico/otro), descripción, síntomas asociados y
medicamentos contraindicados. Para editar, presiona "Editar" en la tabla — el formulario se
precarga con los datos existentes.

> **Antes de crear una enfermedad**, registra primero sus síntomas y medicamentos en las
> secciones correspondientes (los checkboxes solo muestran lo que ya existe en el catálogo).

[CAPTURA: formulario "Nueva enfermedad" con síntomas y medicamentos marcados]

### 3.3 Gestión de síntomas y medicamentos

**Síntomas** y **Medicamentos** son catálogos simples: nombre → se registra y queda
disponible de inmediato en el formulario del paciente y en el de enfermedades. Desde
**Medicamentos** también puedes indicar qué enfermedades trata cada uno.

### 3.4 Contraindicaciones

En **Contraindicaciones** defines qué medicamento no debe usarse para tratar cuál enfermedad.
Estas reglas se aplican en dos niveles automáticamente (sin configuración adicional):

1. **Contra la enfermedad que se está diagnosticando** (fármaco–patología).
2. **Contra cualquier enfermedad crónica que el paciente haya marcado como antecedente**
   (condiciones del paciente) — por eso el mismo catálogo de contraindicaciones cubre ambos
   casos: una enfermedad crónica del paciente es, precisamente, una enfermedad de este
   catálogo.

### 3.5 Exportar el archivo `.pl`

**"Exportar archivo .pl"** descarga el `knowledge_base.pl` completo tal cual está en el
servidor en ese momento — útil para revisión o respaldo.

### 3.6 RPA — Carga masiva de enfermedades

En **RPA — Carga masiva** puedes subir un archivo JSON (formato de `EjemploRPA.json`:
`nombre_enfermedad`, `descripcion`, `sintomas_asociados`, `medicamentos_contraindicados`,
`sistema_cuerpo`) y el robot da de alta cada enfermedad automáticamente, clasificando su
"tipo" por palabras clave en la descripción. Al terminar, muestra un resumen
(creadas/actualizadas/errores) y genera una bitácora en texto plano descargable.

[CAPTURA: resultado de una ejecución del RPA con su bitácora]

> **Nota:** este botón es el modo rápido del RPA (ver detalle técnico en el Manual Técnico,
> sección "Configuración del robot RPA"). No requiere instalación adicional ni es necesario
> ejecutarlo manualmente para usar el sistema — es el flujo normal de administración.

#### Ejecutar el RPA con automatización visual (PyAutoGUI)

Existe una segunda forma de correr el mismo RPA, operando la página real con el mouse/teclado
del sistema (usada para grabar el video de evidencia del proyecto). No es necesaria para el
uso normal del sistema, pero así se ejecuta:

1. Deja el servidor Flask corriendo (`python src/backend/app.py`).
2. En otra terminal: `python scripts/ejecutar_rpa_gui.py EjemploRPA.json`.
3. Deja el navegador abierto y al frente: el script da una cuenta regresiva de 5 segundos
   antes de empezar a mover el mouse y el teclado.
4. Para abortar en cualquier momento, lleva el mouse a cualquier esquina de la pantalla.

Ver el Manual Técnico para el detalle completo de cómo funciona y qué revisar antes de grabar.

## 4. Errores comunes y advertencias

| Situación | Causa | Qué hacer |
|---|---|---|
| El formulario de paciente no muestra síntomas/alergias/crónicas | Aún no hay nada registrado en esos catálogos | Pide al administrador que registre síntomas, medicamentos y enfermedades |
| "No se encontraron enfermedades compatibles" | Ningún síntoma marcado coincide con las enfermedades registradas | Revisa que hayas marcado al menos un síntoma existente en el catálogo |
| "Ningún medicamento seguro disponible" en un diagnóstico | Todos los medicamentos registrados para esa enfermedad están contraindicados por tus alergias/enfermedades crónicas | No es un error: consulta a un médico, el sistema no tiene una alternativa segura que ofrecer |
| Al guardar una enfermedad no aparecen los síntomas esperados en las casillas | El síntoma todavía no existe en el catálogo | Regístralo primero en "Síntomas" |
| `pyswip`/`swipl` no encontrado al iniciar `app.py` | SWI-Prolog no está instalado o no está en el `PATH` | Instala SWI-Prolog (swi-prolog.org) y reinicia la terminal |
| El RPA visual (PyAutoGUI) escribe en la ventana equivocada | El navegador perdió el foco durante la cuenta regresiva | Vuelve a ejecutar el script y no toques el mouse/teclado hasta que termine |

## 5. Aviso legal

MediLogic es un proyecto académico. Los diagnósticos, porcentajes de afinidad y sugerencias
de medicamento son orientativos y **no reemplazan una evaluación médica profesional**.
