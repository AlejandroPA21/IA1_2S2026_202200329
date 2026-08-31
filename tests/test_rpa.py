"""Pruebas del RPA modo rapido (src/rpa/admin_rpa.py::ejecutar_carga).

Cubre los escenarios descritos para el RPA: carga exitosa con el formato
original de EjemploRPA.json, carga con el campo opcional
"tratamiento_recomendado" (ver "Ejemplo Archivo RPA V2.json"), y manejo
controlado de un archivo con campos faltantes (sin que el proceso se
rompa por completo).
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from backend.app import create_app  # noqa: E402
from rpa.admin_rpa import ejecutar_carga  # noqa: E402

RUTA_PL_ORIGINAL = (
    Path(__file__).resolve().parent.parent / "src" / "prolog" / "knowledge_base.pl"
)


@pytest.fixture
def store(tmp_path):
    """KnowledgeStore contra una COPIA del .pl real, para no mutar el repo."""
    ruta_copia = tmp_path / "knowledge_base.pl"
    shutil.copy(RUTA_PL_ORIGINAL, ruta_copia)
    app = create_app(pl_path=ruta_copia)
    return app.knowledge_store


def test_ejecutar_carga_formato_original_actualiza_enfermedades_existentes(store, tmp_path):
    """EjemploRPA.json describe las mismas 4 enfermedades que ya trae el
    .pl: debe actualizarlas (no crear duplicados) y no reportar errores."""
    ruta_json = (
        Path(__file__).resolve().parent.parent / "EjemploRPA.json"
    )
    reporte = ejecutar_carga(ruta_json, store, directorio_reportes=tmp_path / "reportes")

    assert reporte.errores == 0
    assert reporte.actualizadas == 4
    assert reporte.ruta_bitacora.exists()
    assert "MediLogic - Bitacora" in reporte.ruta_bitacora.read_text(encoding="utf-8")


def test_ejecutar_carga_registra_tratamiento_recomendado(store, tmp_path):
    """Con el campo opcional "tratamiento_recomendado" (formato V2), el RPA
    debe registrar tambien medicamento_para/2 para cada medicamento listado,
    dando de alta el medicamento en el catalogo si todavia no existia."""
    registro = [
        {
            "nombre_enfermedad": "Enfermedad_Rpa_Test",
            "descripcion": "Descripcion de prueba para el RPA.",
            "sintomas_asociados": ["dolor_cabeza"],
            "tratamiento_recomendado": ["Nuevo_Medicamento_Rpa"],
            "medicamentos_contraindicados": [],
            "sistema_cuerpo": "neurologico",
        }
    ]
    ruta_json = tmp_path / "carga_v2.json"
    ruta_json.write_text(json.dumps(registro), encoding="utf-8")

    reporte = ejecutar_carga(ruta_json, store, directorio_reportes=tmp_path / "reportes")

    assert reporte.errores == 0
    assert reporte.creadas == 1
    assert "nuevo_medicamento_rpa" in store.engine.medicamentos()
    assert (
        "nuevo_medicamento_rpa",
        "enfermedad_rpa_test",
    ) in store.engine.medicamento_para_all()


def test_ejecutar_carga_con_campos_faltantes_reporta_error_sin_romper(store, tmp_path):
    """Escenario de fallo de formato: un registro sin campos requeridos se
    reporta como error en la bitacora, sin detener el resto de la carga."""
    registros = [
        {"nombre_enfermedad": "Incompleta"},  # faltan campos requeridos
        {
            "nombre_enfermedad": "Completa_Rpa_Test",
            "descripcion": "Enfermedad valida en el mismo archivo.",
            "sintomas_asociados": ["mareo"],
            "medicamentos_contraindicados": [],
            "sistema_cuerpo": "neurologico",
        },
    ]
    ruta_json = tmp_path / "carga_con_error.json"
    ruta_json.write_text(json.dumps(registros), encoding="utf-8")

    reporte = ejecutar_carga(ruta_json, store, directorio_reportes=tmp_path / "reportes")

    assert reporte.errores == 1
    assert reporte.creadas == 1  # la segunda enfermedad, valida, si se crea
    assert "completa_rpa_test" in store.cargar_estado().nombres_enfermedades()
