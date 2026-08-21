"""
Persistencia de la base de conocimiento administrada desde el panel web.

El enunciado (seccion 4.2) exige que el archivo `.pl` sea la unica fuente de
verdad y que los cambios del administrador se reflejen "automaticamente" en
el, sin editarlo a mano. Este modulo es el unico responsable de:

1. Leer el estado completo de los hechos (via `PrologEngine`, es decir, vía
   consultas reales al motor, nunca reinterpretando el texto del archivo).
2. Aplicar el alta/edicion/baja solicitada por el administrador sobre esa
   representacion en memoria (`Estado`).
3. Regenerar UNICAMENTE las secciones de "hechos" del archivo `.pl` (ver los
   marcadores `% === AUTO:<seccion> START/END ===` en knowledge_base.pl),
   dejando intactas las reglas del motor de inferencia.
4. Pedirle a `PrologEngine.reload()` que vuelva a hacer `consult/1`, para que
   el modulo de paciente use la base actualizada de inmediato (recarga en
   caliente, sin reiniciar la aplicacion).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from backend.prolog_engine import PrologEngine

SISTEMAS_CUERPO = [
    "circulatorio",
    "respiratorio",
    "digestivo",
    "endocrino",
    "inmunologico",
    "neurologico",
    "musculoesqueletico",
    "dermatologico",
]

TIPOS_ENFERMEDAD = ["cronico", "viral", "bacteriano", "inmunologico", "otro"]


class ValidationError(Exception):
    """Error de validacion de datos administrativos (nombre duplicado, etc.)."""


def slugify(texto: str) -> str:
    """Convierte un nombre ingresado por el administrador en un atomo Prolog.

    Quita acentos, pasa a minusculas y reemplaza cualquier caracter que no
    sea alfanumerico por guion bajo, para producir un atomo valido sin
    necesidad de comillas (ej. "Migraña Crónica" -> "migrana_cronica").
    """
    sin_acentos = unicodedata.normalize("NFKD", texto)
    sin_acentos = "".join(c for c in sin_acentos if not unicodedata.combining(c))
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", sin_acentos.strip()).strip("_").lower()
    return slug or "sin_nombre"


def _escapar_atomo(texto: str) -> str:
    """Escapa un string para usarlo como atomo entre comillas simples en Prolog."""
    return texto.replace("'", "\\'")


@dataclass
class Enfermedad:
    nombre: str
    descripcion: str
    sistema_cuerpo: str
    tipo: str


@dataclass
class Estado:
    """Representacion completa y editable de las secciones de hechos del .pl."""

    sintomas: list[str] = field(default_factory=list)
    medicamentos: list[str] = field(default_factory=list)
    enfermedades: list[Enfermedad] = field(default_factory=list)
    enfermedad_sintoma: list[tuple[str, str]] = field(default_factory=list)
    medicamento_para: list[tuple[str, str]] = field(default_factory=list)
    contraindicaciones: list[tuple[str, str]] = field(default_factory=list)

    def nombres_enfermedades(self) -> set[str]:
        return {e.nombre for e in self.enfermedades}


class KnowledgeStore:
    """CRUD sobre la base de conocimiento, con persistencia en el archivo .pl."""

    def __init__(self, engine: PrologEngine):
        self.engine = engine
        self.pl_path: Path = engine.pl_path

    # ------------------------------------------------------------------
    # Lectura del estado completo
    # ------------------------------------------------------------------
    def cargar_estado(self) -> Estado:
        enfermedades = [
            Enfermedad(e["nombre"], e["descripcion"], e["sistema_cuerpo"], e["tipo"])
            for e in self.engine.enfermedades()
        ]
        return Estado(
            sintomas=self.engine.sintomas(),
            medicamentos=self.engine.medicamentos(),
            enfermedades=enfermedades,
            enfermedad_sintoma=self.engine.enfermedad_sintoma_all(),
            medicamento_para=self.engine.medicamento_para_all(),
            contraindicaciones=self.engine.contraindicaciones_all(),
        )

    def snapshot(self) -> dict:
        """Vista de solo lectura, comoda para plantillas (dashboard, listados)."""
        estado = self.cargar_estado()
        por_enfermedad = {
            e.nombre: {
                "sintomas": sorted(
                    s for en, s in estado.enfermedad_sintoma if en == e.nombre
                ),
                "medicamentos_contraindicados": sorted(
                    m for m, en in estado.contraindicaciones if en == e.nombre
                ),
                "medicamentos_tratan": sorted(
                    m for m, en in estado.medicamento_para if en == e.nombre
                ),
            }
            for e in estado.enfermedades
        }
        enfermedades = []
        for e in sorted(estado.enfermedades, key=lambda x: x.nombre):
            detalle = por_enfermedad[e.nombre]
            enfermedades.append(
                {
                    "nombre": e.nombre,
                    "descripcion": e.descripcion,
                    "sistema_cuerpo": e.sistema_cuerpo,
                    "tipo": e.tipo,
                    **detalle,
                }
            )
        return {
            "sintomas": estado.sintomas,
            "medicamentos": estado.medicamentos,
            "enfermedades": enfermedades,
            "contraindicaciones": [
                {"medicamento": m, "enfermedad": en}
                for m, en in estado.contraindicaciones
            ],
        }

    # ------------------------------------------------------------------
    # Sintomas
    # ------------------------------------------------------------------
    def crear_sintoma(self, nombre: str) -> str:
        atomo = slugify(nombre)
        estado = self.cargar_estado()
        if atomo in estado.sintomas:
            raise ValidationError(f"El sintoma '{atomo}' ya existe.")
        estado.sintomas.append(atomo)
        self._guardar(estado)
        return atomo

    def eliminar_sintoma(self, atomo: str) -> None:
        estado = self.cargar_estado()
        estado.sintomas = [s for s in estado.sintomas if s != atomo]
        estado.enfermedad_sintoma = [
            par for par in estado.enfermedad_sintoma if par[1] != atomo
        ]
        self._guardar(estado)

    # ------------------------------------------------------------------
    # Medicamentos
    # ------------------------------------------------------------------
    def crear_medicamento(self, nombre: str) -> str:
        atomo = slugify(nombre)
        estado = self.cargar_estado()
        if atomo in estado.medicamentos:
            raise ValidationError(f"El medicamento '{atomo}' ya existe.")
        estado.medicamentos.append(atomo)
        self._guardar(estado)
        return atomo

    def eliminar_medicamento(self, atomo: str) -> None:
        estado = self.cargar_estado()
        estado.medicamentos = [m for m in estado.medicamentos if m != atomo]
        estado.medicamento_para = [
            par for par in estado.medicamento_para if par[0] != atomo
        ]
        estado.contraindicaciones = [
            par for par in estado.contraindicaciones if par[0] != atomo
        ]
        self._guardar(estado)

    def actualizar_tratamientos(self, medicamento: str, enfermedades: list[str]) -> None:
        """Define para que enfermedades sirve `medicamento` (medicamento_para/2)."""
        estado = self.cargar_estado()
        estado.medicamento_para = [
            par for par in estado.medicamento_para if par[0] != medicamento
        ]
        estado.medicamento_para += [(medicamento, e) for e in enfermedades]
        self._guardar(estado)

    # ------------------------------------------------------------------
    # Enfermedades
    # ------------------------------------------------------------------
    def guardar_enfermedad(
        self,
        nombre: str,
        descripcion: str,
        sistema_cuerpo: str,
        tipo: str,
        sintomas: list[str],
        medicamentos_contraindicados: list[str],
        nombre_original: str | None = None,
    ) -> str:
        """Crea o edita una enfermedad. Si `nombre_original` viene informado,
        se trata de una edicion (permite renombrar, migrando sus relaciones)."""
        atomo = slugify(nombre)
        estado = self.cargar_estado()
        existentes = estado.nombres_enfermedades()

        if nombre_original:
            if nombre_original not in existentes:
                raise ValidationError(f"La enfermedad '{nombre_original}' no existe.")
            if atomo != nombre_original and atomo in existentes:
                raise ValidationError(f"Ya existe una enfermedad llamada '{atomo}'.")
            estado.enfermedades = [
                e for e in estado.enfermedades if e.nombre != nombre_original
            ]
            # Migra relaciones existentes al nuevo nombre (por si se renombro)
            estado.enfermedad_sintoma = [
                (atomo if en == nombre_original else en, s)
                for en, s in estado.enfermedad_sintoma
            ]
            estado.medicamento_para = [
                (m, atomo if en == nombre_original else en)
                for m, en in estado.medicamento_para
            ]
            estado.contraindicaciones = [
                (m, atomo if en == nombre_original else en)
                for m, en in estado.contraindicaciones
            ]
        elif atomo in existentes:
            raise ValidationError(f"Ya existe una enfermedad llamada '{atomo}'.")

        estado.enfermedades.append(
            Enfermedad(atomo, descripcion, slugify(sistema_cuerpo), slugify(tipo))
        )

        # Reemplaza por completo las relaciones sintoma/contraindicacion de
        # esta enfermedad segun lo enviado por el formulario.
        estado.enfermedad_sintoma = [
            par for par in estado.enfermedad_sintoma if par[0] != atomo
        ]
        estado.enfermedad_sintoma += [(atomo, s) for s in sorted(set(sintomas))]

        estado.contraindicaciones = [
            par for par in estado.contraindicaciones if par[1] != atomo
        ]
        estado.contraindicaciones += [
            (m, atomo) for m in sorted(set(medicamentos_contraindicados))
        ]

        # Los sintomas/medicamentos nuevos escritos a mano tambien se dan de
        # alta en el catalogo general, para que queden disponibles en el
        # formulario del paciente.
        estado.sintomas = sorted(set(estado.sintomas) | set(sintomas))
        estado.medicamentos = sorted(
            set(estado.medicamentos) | set(medicamentos_contraindicados)
        )

        self._guardar(estado)
        return atomo

    def eliminar_enfermedad(self, nombre: str) -> None:
        estado = self.cargar_estado()
        estado.enfermedades = [e for e in estado.enfermedades if e.nombre != nombre]
        estado.enfermedad_sintoma = [
            par for par in estado.enfermedad_sintoma if par[0] != nombre
        ]
        estado.medicamento_para = [
            par for par in estado.medicamento_para if par[1] != nombre
        ]
        estado.contraindicaciones = [
            par for par in estado.contraindicaciones if par[1] != nombre
        ]
        self._guardar(estado)

    # ------------------------------------------------------------------
    # Contraindicaciones (gestion directa, ademas de la del formulario de
    # enfermedad) - relacion Medicamento <-> Enfermedad.
    # ------------------------------------------------------------------
    def agregar_contraindicacion(self, medicamento: str, enfermedad: str) -> None:
        estado = self.cargar_estado()
        if (medicamento, enfermedad) not in estado.contraindicaciones:
            estado.contraindicaciones.append((medicamento, enfermedad))
        self._guardar(estado)

    def eliminar_contraindicacion(self, medicamento: str, enfermedad: str) -> None:
        estado = self.cargar_estado()
        estado.contraindicaciones = [
            par
            for par in estado.contraindicaciones
            if par != (medicamento, enfermedad)
        ]
        self._guardar(estado)

    # ------------------------------------------------------------------
    # Carga masiva (usada por el RPA administrativo, ver src/rpa/admin_rpa.py)
    # ------------------------------------------------------------------
    def cargar_enfermedad_rpa(
        self,
        nombre: str,
        descripcion: str,
        sistema_cuerpo: str,
        tipo: str,
        sintomas: list[str],
        medicamentos_contraindicados: list[str],
    ) -> str:
        """Alta de una enfermedad sin exigir unicidad estricta: si ya existe,
        la actualiza (idempotente), tal como conviene a una carga automatica
        que puede reintentarse."""
        atomo = slugify(nombre)
        estado = self.cargar_estado()
        nombre_original = atomo if atomo in estado.nombres_enfermedades() else None
        return self.guardar_enfermedad(
            nombre=nombre,
            descripcion=descripcion,
            sistema_cuerpo=sistema_cuerpo,
            tipo=tipo,
            sintomas=[slugify(s) for s in sintomas],
            medicamentos_contraindicados=[
                slugify(m) for m in medicamentos_contraindicados
            ],
            nombre_original=nombre_original,
        )

    # ------------------------------------------------------------------
    # Regeneracion del archivo .pl (solo secciones de hechos)
    # ------------------------------------------------------------------
    def _guardar(self, estado: Estado) -> None:
        secciones = {
            "SINTOMAS": self._render_sintomas(estado.sintomas),
            "MEDICAMENTOS": self._render_medicamentos(estado.medicamentos),
            "ENFERMEDADES": self._render_enfermedades(estado.enfermedades),
            "ENFERMEDAD_SINTOMA": self._render_pares(
                "enfermedad_sintoma", estado.enfermedad_sintoma
            ),
            "MEDICAMENTO_PARA": self._render_pares(
                "medicamento_para", estado.medicamento_para
            ),
            "CONTRAINDICACIONES": self._render_pares(
                "contraindicacion_enfermedad", estado.contraindicaciones
            ),
        }

        texto = self.pl_path.read_text(encoding="utf-8")
        for nombre, contenido in secciones.items():
            texto = self._reemplazar_seccion(texto, nombre, contenido)

        self.pl_path.write_text(texto, encoding="utf-8")
        self.engine.reload()

    @staticmethod
    def _reemplazar_seccion(texto: str, nombre: str, contenido: str) -> str:
        inicio = f"% === AUTO:{nombre} START ==="
        fin = f"% === AUTO:{nombre} END ==="
        patron = re.compile(re.escape(inicio) + r".*?" + re.escape(fin), re.DOTALL)
        reemplazo = f"{inicio}\n{contenido}{fin}"
        nuevo_texto, n = patron.subn(reemplazo, texto)
        if n == 0:
            raise RuntimeError(
                f"No se encontraron los marcadores AUTO:{nombre} en knowledge_base.pl"
            )
        return nuevo_texto

    @staticmethod
    def _render_sintomas(sintomas: list[str]) -> str:
        return "".join(f"sintoma({s}).\n" for s in sorted(set(sintomas)))

    @staticmethod
    def _render_medicamentos(medicamentos: list[str]) -> str:
        return "".join(f"medicamento({m}).\n" for m in sorted(set(medicamentos)))

    @staticmethod
    def _render_enfermedades(enfermedades: list[Enfermedad]) -> str:
        partes = []
        for e in sorted(enfermedades, key=lambda x: x.nombre):
            desc = _escapar_atomo(e.descripcion)
            partes.append(
                f"enfermedad({e.nombre},\n"
                f"    '{desc}',\n"
                f"    {e.sistema_cuerpo}, {e.tipo}).\n\n"
            )
        return "".join(partes)

    @staticmethod
    def _render_pares(predicado: str, pares: list[tuple[str, str]]) -> str:
        return "".join(
            f"{predicado}({a}, {b}).\n" for a, b in sorted(set(pares))
        )
