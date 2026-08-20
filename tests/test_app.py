"""Pruebas basicas de arranque de la aplicacion Flask."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from backend.app import create_app  # noqa: E402


def test_index_route_responde():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
