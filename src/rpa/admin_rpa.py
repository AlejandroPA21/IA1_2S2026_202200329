"""
RPA de carga de enfermedades para el modulo administrador de MediLogic.

Automatiza el llenado del formulario de alta de enfermedades a partir de un
archivo proporcionado por el administrador (ver `EjemploRPA.json` para el
formato esperado: nombre, descripcion, sintomas asociados, medicamentos
contraindicados y clasificacion por sistema del cuerpo/tipo). Debe ejecutarse
del lado del backend y estar desarrollado en Python (requisito de la seccion
4.2 y de la rubrica).

Al finalizar la carga, genera una bitacora en texto plano con el detalle de
los cambios realizados (enfermedades creadas, clasificacion asignada, errores
si los hubiera).

NOTA: La implementacion funcional (PyAutoGUI, lectura del JSON, generacion de
la bitacora) corresponde al entregable de automatizacion de la Entrega No. 2 -
Proyecto Final. Este archivo se deja como marcador de posicion dentro de la
estructura del repositorio.
"""
