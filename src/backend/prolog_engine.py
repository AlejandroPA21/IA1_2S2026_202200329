"""
Puente entre Python y el motor logico Prolog (SWI-Prolog via pyswip).

Toda la logica de diagnostico vive en `src/prolog/knowledge_base.pl`. Esta
clase es la unica responsable de cargar (`consult/1`) y volver a cargar ese
archivo, y de traducir las consultas Prolog hacia/desde estructuras de datos
de Python, para que el resto del backend nunca tenga que hablar con pyswip
directamente.
"""

from pathlib import Path


class PrologEngine:
    """Envoltorio sobre pyswip.Prolog para consultar la base de conocimiento."""

    def __init__(self, pl_path: str | Path):
        self.pl_path = Path(pl_path)
        # TODO (siguiente entregable): inicializar pyswip.Prolog() y ejecutar
        # consult(self.pl_path) al construir la instancia.

    def reload(self) -> None:
        """Vuelve a consultar el archivo .pl tras una edicion administrativa.

        Este metodo implementa la actualizacion en caliente descrita en la
        seccion 4.2 del enunciado: tras sobrescribir knowledge_base.pl desde
        el panel de administrador, se invoca consult/1 nuevamente para que el
        modulo de pacientes use la base de conocimiento actualizada sin
        reiniciar la aplicacion.
        """
        raise NotImplementedError("Se implementara junto con el motor de inferencia.")
