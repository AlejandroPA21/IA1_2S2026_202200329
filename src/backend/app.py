"""
MediLogic - Punto de entrada de la aplicacion Flask.

Este modulo expone la fabrica `create_app`, encargada de construir la
aplicacion Flask con sus rutas, plantillas y archivos estaticos. La logica de
negocio (diagnostico, contraindicaciones, calculo de afinidad) vive
exclusivamente en `src/prolog/knowledge_base.pl` y se consulta a traves de
`prolog_engine.py`; este archivo unicamente orquesta la capa web.
"""

from flask import Flask


def create_app() -> Flask:
    """Crea y configura la instancia de la aplicacion Flask."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.route("/")
    def index():
        # Pantalla de inicio publica (sin autenticacion), segun seccion 4.2
        # del enunciado. La version completa (descripcion del sistema y
        # navegacion a los modulos de paciente/administrador) se implementa
        # junto con el entregable de diseno de interfaz.
        return "MediLogic - Sistema experto de diagnostico preliminar (en construccion)"

    # Los blueprints de paciente y administrador se registraran aqui conforme
    # se implementen (ver src/backend/routes/).

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
