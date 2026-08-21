"""Pruebas del flujo de diagnostico del modulo paciente (formulario -> informe -> PDF)."""

import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from backend.app import create_app  # noqa: E402

RUTA_PL_ORIGINAL = (
    Path(__file__).resolve().parent.parent / "src" / "prolog" / "knowledge_base.pl"
)


@pytest.fixture
def cliente(tmp_path):
    """App de pruebas contra una COPIA del .pl real, para no mutar el repo."""
    ruta_copia = tmp_path / "knowledge_base.pl"
    shutil.copy(RUTA_PL_ORIGINAL, ruta_copia)
    app = create_app(pl_path=ruta_copia)
    app.testing = True
    return app.test_client()


def test_formulario_carga_catalogos_dinamicos(cliente):
    respuesta = cliente.get("/paciente/")
    assert respuesta.status_code == 200
    assert b"dolor_cabeza" in respuesta.data  # catalogo real de sintomas del .pl


def test_diagnostico_calcula_afinidad_y_excluye_medicamento_por_alergia(cliente):
    respuesta = cliente.post(
        "/paciente/diagnostico",
        data={
            "sintoma": ["dolor_cabeza", "mareo"],
            "severidad_dolor_cabeza": "moderado",
            "severidad_mareo": "severo",
            "alergia": ["ibuprofeno"],
        },
    )
    assert respuesta.status_code == 200
    # Coincide con el caso documentado en decisiones_tecnicas.md / demo_prolog.pl
    assert b"56%" in respuesta.data
    assert b"losartan" in respuesta.data.lower()


def test_diagnostico_sin_sintomas_no_rompe(cliente):
    respuesta = cliente.post("/paciente/diagnostico", data={})
    assert respuesta.status_code == 200
    assert b"No se encontraron enfermedades" in respuesta.data


def test_descarga_pdf_genera_documento(cliente):
    respuesta = cliente.post(
        "/paciente/informe/pdf",
        data={
            "sintoma": ["dolor_cabeza", "mareo"],
            "severidad_dolor_cabeza": "moderado",
            "severidad_mareo": "severo",
            "alergia": ["ibuprofeno"],
        },
    )
    assert respuesta.status_code == 200
    assert respuesta.content_type == "application/pdf"
    assert respuesta.data[:4] == b"%PDF"
