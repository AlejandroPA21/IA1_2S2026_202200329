"""
MediLogic - Punto de entrada del RPA con automatizacion visual (PyAutoGUI).

Este es el script que se debe grabar para el video de evidencia (ver
seccion "Entregables" del enunciado). A diferencia del boton "Ejecutar RPA"
del panel de administrador (que llama directo a KnowledgeStore), este
script opera la pagina web real con el mouse/teclado del sistema, tal como
lo haria un administrador humano llenando el formulario "Nueva enfermedad"
campo por campo.

Uso (desde la raiz del repositorio, con el entorno virtual activado):
    1. En una terminal: python src/backend/app.py
    2. En OTRA terminal: python scripts/ejecutar_rpa_gui.py [ruta_al_json]
       (si se omite la ruta, usa EjemploRPA.json)

Ver docs/manual_tecnico/manual_tecnico.md, seccion "Configuracion del
robot RPA", para el detalle de como funciona (sin coordenadas de pantalla)
y que revisar antes de grabar.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from rpa.gui_automation import ejecutar_carga_gui  # noqa: E402


def main() -> None:
    ruta_json = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "EjemploRPA.json"
    if not ruta_json.exists():
        print(f"No se encontro el archivo: {ruta_json}")
        sys.exit(1)

    print("=" * 70)
    print("MediLogic - RPA con automatizacion visual (PyAutoGUI)")
    print("=" * 70)
    print(f"Archivo de origen : {ruta_json}")
    print("Verifica que el servidor Flask ya este corriendo y abre/enfoca")
    print("el navegador ahora: el robot empezara a mover el mouse y el")
    print("teclado del sistema en unos segundos.")
    print("Para abortar: lleva el mouse a cualquier esquina de la pantalla")
    print("(FAILSAFE) o presiona Ctrl+C en esta terminal.")
    print("=" * 70)

    reporte = ejecutar_carga_gui(
        ruta_json, directorio_reportes=str(RAIZ / "instance" / "reportes")
    )

    print()
    print(
        f"Creadas: {reporte.creadas}  Actualizadas: {reporte.actualizadas}  "
        f"Errores: {reporte.errores}"
    )
    print(f"Bitacora: {reporte.ruta_bitacora}")


if __name__ == "__main__":
    main()
