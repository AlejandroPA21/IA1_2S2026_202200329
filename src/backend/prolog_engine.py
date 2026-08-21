"""
Puente entre Python y el motor logico Prolog (SWI-Prolog via pyswip).

Toda la logica de diagnostico vive en `src/prolog/knowledge_base.pl`. Esta
clase es la unica responsable de cargar (`consult/1`) y volver a cargar ese
archivo, y de traducir las consultas Prolog hacia/desde estructuras de datos
de Python, para que el resto del backend nunca tenga que hablar con pyswip
directamente.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from pyswip import Prolog


class PrologEngine:
    """Envoltorio sobre pyswip.Prolog para consultar la base de conocimiento."""

    def __init__(self, pl_path: str | Path):
        self.pl_path = Path(pl_path)
        self.prolog = Prolog()
        # pyswip/SWI-Prolog no es seguro para llamadas concurrentes desde
        # varios hilos del servidor de desarrollo de Flask; un lock simple
        # evita condiciones de carrera al hacer consult/query desde distintas
        # requests (ver decisiones_tecnicas.md).
        self._lock = threading.RLock()
        self.reload()

    # ------------------------------------------------------------------
    # Carga / recarga del archivo .pl
    # ------------------------------------------------------------------
    def reload(self) -> None:
        """Vuelve a consultar el archivo .pl tras una edicion administrativa.

        Este metodo implementa la actualizacion en caliente descrita en la
        seccion 4.2 del enunciado: tras sobrescribir knowledge_base.pl desde
        el panel de administrador, se invoca consult/1 nuevamente para que el
        modulo de pacientes use la base de conocimiento actualizada sin
        reiniciar la aplicacion.
        """
        with self._lock:
            # Prolog usa "/" como separador de rutas incluso en Windows; y
            # consult/1 espera una ruta entre comillas simples si contiene
            # espacios o backslashes.
            ruta = str(self.pl_path.resolve()).replace("\\", "/")
            list(self.prolog.query(f"consult('{ruta}')"))

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------
    def _query(self, texto: str) -> list[dict[str, Any]]:
        with self._lock:
            return list(self.prolog.query(texto))

    @staticmethod
    def _atom(valor: Any) -> str:
        """Convierte un resultado de pyswip (bytes/atom) a str de Python."""
        if isinstance(valor, bytes):
            return valor.decode("utf-8")
        return str(valor)

    # ------------------------------------------------------------------
    # Catalogos (usados por el formulario del paciente y el admin)
    # ------------------------------------------------------------------
    def sintomas(self) -> list[str]:
        filas = self._query("sintoma(S)")
        return sorted(self._atom(f["S"]) for f in filas)

    def medicamentos(self) -> list[str]:
        filas = self._query("medicamento(M)")
        return sorted(self._atom(f["M"]) for f in filas)

    def alergias_disponibles(self) -> list[str]:
        """Catalogo de alergias = catalogo de medicamentos (regla alergia/1)."""
        filas = self._query("alergia(M)")
        return sorted(self._atom(f["M"]) for f in filas)

    def enfermedades(self) -> list[dict[str, str]]:
        filas = self._query("enfermedad(N, D, S, T)")
        resultado = []
        for f in filas:
            resultado.append(
                {
                    "nombre": self._atom(f["N"]),
                    "descripcion": self._atom(f["D"]),
                    "sistema_cuerpo": self._atom(f["S"]),
                    "tipo": self._atom(f["T"]),
                }
            )
        return sorted(resultado, key=lambda e: e["nombre"])

    def enfermedades_cronicas(self) -> list[str]:
        filas = self._query("enfermedad_cronica(N)")
        return sorted(self._atom(f["N"]) for f in filas)

    def sintomas_de(self, enfermedad: str) -> list[str]:
        filas = self._query(f"enfermedad_sintoma({enfermedad}, S)")
        return sorted(self._atom(f["S"]) for f in filas)

    def medicamentos_para(self, enfermedad: str) -> list[str]:
        filas = self._query(f"medicamento_para(M, {enfermedad})")
        return [self._atom(f["M"]) for f in filas]

    def contraindicaciones_de(self, enfermedad: str) -> list[str]:
        filas = self._query(f"contraindicacion_enfermedad(M, {enfermedad})")
        return sorted(self._atom(f["M"]) for f in filas)

    def todas_las_contraindicaciones(self) -> list[dict[str, str]]:
        filas = self._query("contraindicacion_enfermedad(M, E)")
        return sorted(
            (
                {"medicamento": self._atom(f["M"]), "enfermedad": self._atom(f["E"])}
                for f in filas
            ),
            key=lambda c: (c["enfermedad"], c["medicamento"]),
        )

    def enfermedad_sintoma_all(self) -> list[tuple[str, str]]:
        filas = self._query("enfermedad_sintoma(E, S)")
        return [(self._atom(f["E"]), self._atom(f["S"])) for f in filas]

    def medicamento_para_all(self) -> list[tuple[str, str]]:
        filas = self._query("medicamento_para(M, E)")
        return [(self._atom(f["M"]), self._atom(f["E"])) for f in filas]

    def contraindicaciones_all(self) -> list[tuple[str, str]]:
        filas = self._query("contraindicacion_enfermedad(M, E)")
        return [(self._atom(f["M"]), self._atom(f["E"])) for f in filas]

    # ------------------------------------------------------------------
    # Diagnostico (modulo paciente)
    # ------------------------------------------------------------------
    def diagnosticar(
        self,
        sintomas: list[tuple[str, str]],
        alergias: list[str],
        cronicas: list[str],
    ) -> list[dict[str, Any]]:
        """Ejecuta informe/4 y devuelve una lista de diagnosticos ordenada.

        `sintomas` es una lista de tuplas (sintoma, severidad), tal como las
        arma el formulario del paciente.
        """
        lista_sintomas = "[" + ",".join(f"{s}-{sev}" for s, sev in sintomas) + "]"
        lista_alergias = "[" + ",".join(alergias) + "]"
        lista_cronicas = "[" + ",".join(cronicas) + "]"

        # informe/4 devuelve una LISTA de terminos compuestos resultado/5.
        # pyswip no reconstruye terminos compuestos anidados dentro de listas
        # como objetos Python navegables (los serializa como texto), asi que
        # se recorren uno a uno con member/2: cada backtracking de la
        # consulta entrega una fila con variables escalares (atomos/numeros)
        # que pyswip si convierte de forma nativa, preservando el orden por
        # afinidad que ya calculo diagnosticar/2 dentro del propio .pl.
        consulta = (
            f"informe({lista_sintomas}, {lista_alergias}, {lista_cronicas}, Informe), "
            "member(resultado(Enf, Pct, Urg, Rec, Med), Informe)"
        )
        filas = self._query(consulta)
        return [
            {
                "enfermedad": self._atom(f["Enf"]),
                "afinidad": int(f["Pct"]),
                "urgencia": self._atom(f["Urg"]),
                "recomendacion": self._atom(f["Rec"]),
                "medicamento": self._atom(f["Med"]),
            }
            for f in filas
        ]

    def reglas_activadas(
        self,
        enfermedad: str,
        sintomas: list[tuple[str, str]],
        afinidad: int,
        urgencia: str,
        medicamento: str,
    ) -> list[str]:
        """Arma una traza legible de las reglas Prolog que explican un resultado.

        Cumple el requisito de la seccion 4.2 ("explicacion detallada que
        indique que reglas Prolog se activaron"). No re-implementa la logica:
        solo describe, con los datos ya calculados por informe/4, cuales
        clausulas del archivo .pl participaron.
        """
        coincidentes = [
            f"{s}-{sev}" for s, sev in sintomas if s in self.sintomas_de(enfermedad)
        ]
        lista = ", ".join(coincidentes) if coincidentes else "(ninguno)"
        return [
            f"afinidad({enfermedad}, [{lista}], {afinidad}).",
            f"nivel_urgencia({afinidad}, {urgencia}, '...').",
            f"medicamento_sugerido({enfermedad}, Alergias, Cronicas, {medicamento}).",
        ]
