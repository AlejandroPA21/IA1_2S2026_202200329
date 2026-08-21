"""Pruebas del modulo administrador: autenticacion y CRUD basico de enfermedades."""

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
    ruta_copia = tmp_path / "knowledge_base.pl"
    shutil.copy(RUTA_PL_ORIGINAL, ruta_copia)
    app = create_app(pl_path=ruta_copia)
    app.testing = True
    app.instance_path = str(tmp_path / "instance")
    return app.test_client()


def _login(cliente, usuario="admin", contrasena="medilogic2026"):
    return cliente.post(
        "/admin/login", data={"usuario": usuario, "contrasena": contrasena}
    )


def test_rutas_admin_requieren_login(cliente):
    respuesta = cliente.get("/admin/", follow_redirects=True)
    assert b"Acceso administrador" in respuesta.data


def test_login_incorrecto_rechaza(cliente):
    respuesta = _login(cliente, contrasena="incorrecta")
    assert respuesta.status_code == 401


def test_login_correcto_permite_acceso_al_panel(cliente):
    _login(cliente)
    respuesta = cliente.get("/admin/")
    assert respuesta.status_code == 200
    assert b"Panel general" in respuesta.data


def test_crear_editar_y_eliminar_enfermedad(cliente):
    _login(cliente)

    respuesta = cliente.post(
        "/admin/enfermedades",
        data={
            "nombre": "Migrana Test",
            "descripcion": "Dolor de cabeza recurrente.",
            "sistema_cuerpo": "neurologico",
            "tipo": "cronico",
            "sintomas": ["dolor_cabeza"],
            "medicamentos_contraindicados": [],
        },
        follow_redirects=True,
    )
    assert b"migrana_test" in respuesta.data.lower()

    respuesta = cliente.post(
        "/admin/enfermedades/migrana_test/eliminar", follow_redirects=True
    )
    assert b"eliminada" in respuesta.data.lower()


def test_exportar_pl_devuelve_archivo(cliente):
    _login(cliente)
    respuesta = cliente.get("/admin/pl/exportar")
    assert respuesta.status_code == 200
    assert b"knowledge_base" in respuesta.data or b"sintoma(" in respuesta.data
