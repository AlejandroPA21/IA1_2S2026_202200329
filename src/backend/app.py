"""
MediLogic - Punto de entrada de la aplicacion Flask.

Este modulo expone la fabrica `create_app`, encargada de construir la
aplicacion Flask con sus rutas, plantillas y archivos estaticos. La logica de
negocio (diagnostico, contraindicaciones, calculo de afinidad) vive
exclusivamente en `src/prolog/knowledge_base.pl` y se consulta a traves de
`prolog_engine.py`; este archivo unicamente orquesta la capa web: registra
los blueprints de paciente/administrador y crea una unica instancia del
motor Prolog (y de su capa de persistencia, `KnowledgeStore`) compartida por
toda la aplicacion.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Permite ejecutar este archivo directamente (`python src/backend/app.py`,
# como indica el README) y tambien importarlo como paquete (`backend.app`,
# como hacen los tests) usando siempre imports absolutos "backend.X".
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from flask import Flask, render_template

from backend.knowledge_store import KnowledgeStore
from backend.prolog_engine import PrologEngine
from backend.routes.admin import admin_bp
from backend.routes.paciente import paciente_bp

load_dotenv()

RUTA_PL_POR_DEFECTO = (
    Path(__file__).resolve().parent.parent / "prolog" / "knowledge_base.pl"
)


def _etiqueta(atomo: str) -> str:
    """Filtro Jinja: convierte un atomo Prolog ('dolor_cabeza') en una
    etiqueta legible ('Dolor Cabeza') para mostrar en la interfaz."""
    return atomo.replace("_", " ").strip().title()


def create_app(pl_path: str | Path | None = None) -> Flask:
    """Crea y configura la instancia de la aplicacion Flask."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "medilogic-dev-secret")
    app.config["ADMIN_USER"] = os.environ.get("ADMIN_USER", "admin")
    app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD", "medilogic2026")

    app.jinja_env.filters["etiqueta"] = _etiqueta

    ruta_pl = Path(pl_path) if pl_path else RUTA_PL_POR_DEFECTO
    # El motor y el store se cuelgan de la instancia de la app (no de un
    # global de modulo) para que cada `create_app()` -por ejemplo, cada
    # ejecucion de test- tenga su propia conexion aislada con SWI-Prolog.
    app.prolog_engine = PrologEngine(ruta_pl)
    app.knowledge_store = KnowledgeStore(app.prolog_engine)

    @app.route("/")
    def index():
        # Pantalla de inicio publica (sin autenticacion), segun seccion 4.2
        # del enunciado.
        return render_template("index.html")

    app.register_blueprint(paciente_bp)
    app.register_blueprint(admin_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
