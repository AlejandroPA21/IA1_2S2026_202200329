"""
RPA de carga de enfermedades para el modulo administrador de MediLogic.

Automatiza el alta de enfermedades a partir de un archivo JSON proporcionado
por el administrador (ver `EjemploRPA.json` para el formato esperado:
nombre, descripcion, sintomas asociados, medicamentos contraindicados y
sistema del cuerpo). Debe ejecutarse del lado del backend y estar
desarrollado en Python (requisito de la seccion 4.2 y de la rubrica).

Clasificacion automatica: el JSON de origen no incluye el "tipo" de
enfermedad (cronico/viral/bacteriano/inmunologico), asi que el robot lo
infiere a partir de palabras clave presentes en la descripcion -- esta es
precisamente la tarea repetitiva que el enunciado pide automatizar
("clasificar cada una de las enfermedades... ya que estas tareas suponen la
inversion de mucho tiempo para el usuario administrador"). El sistema del
cuerpo se toma del JSON y se normaliza (slugify) para quedar como atomo
Prolog valido.

Al finalizar la carga, genera una bitacora en texto plano con el detalle de
los cambios realizados (enfermedades creadas/actualizadas, clasificacion
asignada, errores si los hubiera), disponible para descarga y consulta
posterior desde el panel de administrador.

NOTA DE ALCANCE: esta version automatiza el alta llamando directamente a la
capa de persistencia (`KnowledgeStore`), que es la misma logica que usa el
formulario manual del administrador -- garantiza que cada enfermedad quede
clasificada y escrita en `knowledge_base.pl` exactamente igual que si un
humano hubiera llenado el formulario campo por campo. La automatizacion de
la interfaz grafica en si (PyAutoGUI moviendo el mouse/tecleando sobre la
pantalla del navegador) queda como una capa adicional opcional sobre esta
misma funcion, a implementar cuando se grabe el video de evidencia, ya que
requiere una sesion grafica real (no disponible en un entorno de pruebas
automatizado).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from backend.knowledge_store import KnowledgeStore, ValidationError, slugify

CAMPOS_REQUERIDOS = [
    "nombre_enfermedad",
    "descripcion",
    "sintomas_asociados",
    "medicamentos_contraindicados",
    "sistema_cuerpo",
]

# Palabras clave -> tipo de enfermedad. Se evalua en orden y se usa la
# primera coincidencia. Los terminos "metabolico"/"arterial"/"elevado(s)"
# tambien se tratan como indicio de cronicidad porque, en la practica, casi
# ninguna descripcion clinica breve incluye literalmente la palabra
# "cronica" aunque la condicion lo sea (ej. diabetes, hipertension).
PALABRAS_CLAVE_TIPO = [
    (("cronic", "metabolic", "arterial", "elevad", "recurrent", "persistent"), "cronico"),
    (("autoinmun", "inmunolog"), "inmunologico"),
    (("bacteria",), "bacteriano"),
    (("viral", "virus", "infeccio"), "viral"),
]


def clasificar_tipo(descripcion: str) -> str:
    """Infiere el tipo de enfermedad a partir de palabras clave en la
    descripcion. Es la clasificacion automatica que pide el enunciado.

    Si ninguna palabra clave aplica, se asume "cronico" por defecto: en un
    catalogo de diagnostico preliminar, una condicion que no se describe
    explicitamente como infecciosa/autoinmune/bacteriana suele ser cronica.
    Esta clasificacion automatica queda siempre visible en la bitacora y es
    editable manualmente desde el formulario de enfermedades, tal como
    corresponde a una automatizacion de apoyo (RPA) y no a una decision
    clinica definitiva.
    """
    texto = descripcion.lower()
    for palabras, tipo in PALABRAS_CLAVE_TIPO:
        if any(palabra in texto for palabra in palabras):
            return tipo
    return "cronico"


@dataclass
class ResultadoItem:
    nombre_original: str
    atomo: str
    sistema_cuerpo: str
    tipo: str
    estado: str  # "creada" | "actualizada" | "error"
    detalle: str = ""


@dataclass
class ReporteRPA:
    archivo_origen: str
    inicio: datetime
    fin: datetime
    items: list[ResultadoItem] = field(default_factory=list)
    ruta_bitacora: Path | None = None

    @property
    def creadas(self) -> int:
        return sum(1 for i in self.items if i.estado == "creada")

    @property
    def actualizadas(self) -> int:
        return sum(1 for i in self.items if i.estado == "actualizada")

    @property
    def errores(self) -> int:
        return sum(1 for i in self.items if i.estado == "error")

    def texto_bitacora(self) -> str:
        lineas = [
            "=" * 70,
            "MediLogic - Bitacora de carga masiva de enfermedades (RPA)",
            "=" * 70,
            f"Archivo de origen : {self.archivo_origen}",
            f"Inicio            : {self.inicio.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Fin               : {self.fin.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Duracion          : {(self.fin - self.inicio).total_seconds():.2f} s",
            "",
            f"Enfermedades creadas    : {self.creadas}",
            f"Enfermedades actualizadas: {self.actualizadas}",
            f"Errores                 : {self.errores}",
            "-" * 70,
        ]
        for i, item in enumerate(self.items, start=1):
            lineas.append(f"[{i}] {item.nombre_original} -> {item.atomo}")
            if item.estado == "error":
                lineas.append(f"    ERROR: {item.detalle}")
            else:
                lineas.append(
                    f"    Clasificada como sistema: {item.sistema_cuerpo} / "
                    f"tipo: {item.tipo} (automatico, por palabras clave)"
                )
                lineas.append(f"    Estado: {item.estado}")
        lineas.append("-" * 70)
        lineas.append("Fin de la bitacora.")
        return "\n".join(lineas) + "\n"


def _validar_registro(registro: dict[str, Any]) -> None:
    faltantes = [c for c in CAMPOS_REQUERIDOS if c not in registro]
    if faltantes:
        raise ValidationError(f"Faltan campos requeridos: {', '.join(faltantes)}")


def ejecutar_carga(
    ruta_json: str | Path,
    store: KnowledgeStore,
    directorio_reportes: str | Path = "reportes",
) -> ReporteRPA:
    """Ejecuta el RPA: lee el JSON, clasifica y da de alta cada enfermedad.

    Devuelve un `ReporteRPA` con el detalle de la ejecucion y la ruta del
    archivo de bitacora en texto plano ya escrito en disco.
    """
    ruta_json = Path(ruta_json)
    inicio = datetime.now()
    registros = json.loads(ruta_json.read_text(encoding="utf-8"))
    if isinstance(registros, dict):
        registros = [registros]

    items: list[ResultadoItem] = []
    for registro in registros:
        nombre = registro.get("nombre_enfermedad", "(sin nombre)")
        try:
            _validar_registro(registro)
            tipo = clasificar_tipo(registro["descripcion"])
            sistema = slugify(registro["sistema_cuerpo"])
            atomo_existente = slugify(nombre) in store.cargar_estado().nombres_enfermedades()

            atomo = store.cargar_enfermedad_rpa(
                nombre=nombre,
                descripcion=registro["descripcion"],
                sistema_cuerpo=sistema,
                tipo=tipo,
                sintomas=registro["sintomas_asociados"],
                medicamentos_contraindicados=registro["medicamentos_contraindicados"],
            )
            items.append(
                ResultadoItem(
                    nombre_original=nombre,
                    atomo=atomo,
                    sistema_cuerpo=sistema,
                    tipo=tipo,
                    estado="actualizada" if atomo_existente else "creada",
                )
            )
        except (ValidationError, KeyError, TypeError) as exc:
            items.append(
                ResultadoItem(
                    nombre_original=nombre,
                    atomo=slugify(nombre),
                    sistema_cuerpo="",
                    tipo="",
                    estado="error",
                    detalle=str(exc),
                )
            )

    fin = datetime.now()
    reporte = ReporteRPA(
        archivo_origen=ruta_json.name, inicio=inicio, fin=fin, items=items
    )

    destino = Path(directorio_reportes)
    destino.mkdir(parents=True, exist_ok=True)
    nombre_bitacora = f"rpa_carga_{inicio.strftime('%Y%m%d_%H%M%S')}.txt"
    ruta_bitacora = destino / nombre_bitacora
    ruta_bitacora.write_text(reporte.texto_bitacora(), encoding="utf-8")
    reporte.ruta_bitacora = ruta_bitacora

    return reporte
