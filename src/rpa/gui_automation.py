"""
RPA con automatizacion visual real (PyAutoGUI) para el alta de enfermedades.

`rpa.admin_rpa.ejecutar_carga` (el "modo rapido", usado por el boton
"Ejecutar RPA" del panel de administrador) llama directamente a
`KnowledgeStore`, sin pasar por la interfaz. Este modulo es el complemento
que SI opera la pagina web como lo haria un administrador humano -moviendo
el teclado real del sistema operativo con PyAutoGUI-, que es lo que exige
el enunciado (seccion 4.2: "RPA que ayude al administrador... llenando cada
campo de forma automatica") y lo que debe quedar grabado en el video de
evidencia (ver seccion "Entregables"). Se agrega como script separado, en
vez de reemplazar `ejecutar_carga`, porque ambos cumplen roles distintos:
el modo rapido es el que un administrador usaria en el dia a dia (confiable
y sin depender de que el navegador tenga foco); este modulo es la prueba de
automatizacion RPA con PyAutoGUI que pide la rubrica.

DISENO -sin coordenadas de pantalla ni reconocimiento de imagenes-:

  1. Los 3 formularios de alta ("Nuevo sintoma", "Nuevo medicamento",
     "Nueva enfermedad") tienen su primer campo con el atributo HTML
     `autofocus` (ver src/backend/templates/admin_*.html): el navegador ya
     dejo el cursor listo apenas la pagina carga, sin necesidad de ningun
     clic (que si dependeria de resolucion/zoom/posicion de la ventana).
  2. La navegacion entre paginas usa el atajo universal Ctrl+L (foco en la
     barra de direcciones) + escribir la URL + Enter, en vez de clics sobre
     enlaces del menu -funciona igual en Chrome, Edge o Firefox, y sin
     importar el tamano de la ventana.
  3. Todo el texto que se escribe en un campo se pega desde el portapapeles
     (Ctrl+V) en vez de simularse tecla por tecla: `pyautogui.write()` no
     soporta de forma confiable acentos/enies del espanol, y el
     portapapeles si preserva cualquier caracter Unicode.
  4. Los <select> (sistema del cuerpo / tipo) se resuelven con Home + Down
     repetido N veces, con N = indice del valor deseado dentro de
     SISTEMAS_CUERPO / TIPOS_ENFERMEDAD (mismo orden que usa la plantilla),
     en vez de "type-ahead", cuyo comportamiento exacto varia por navegador.
  5. Los checkboxes de "Sintomas asociados" y "Medicamentos contraindicados"
     se alcanzan contando cuantas veces hay que presionar Tab desde el
     primero de la lista. Ese conteo se calcula leyendo el catalogo REAL
     (via PrologEngine, en modo solo lectura -nunca escribe nada-) justo
     antes de llenar cada enfermedad, porque la plantilla siempre los
     renderiza en orden alfabetico (ver knowledge_store.py). Es decir: el
     robot sabe donde esta cada casilla porque conoce el estado real de la
     base de conocimiento, no porque tenga memorizada una posicion en
     pixeles -por eso sigue funcionando aunque cambie el catalogo.

Requisitos para ejecutar este script (ver tambien
docs/manual_tecnico/manual_tecnico.md, seccion "Configuracion del robot
RPA"):

  1. El servidor Flask debe estar corriendo (`python src/backend/app.py`)
     en otra terminal, con las credenciales de administrador por defecto
     (o las que se indiquen en `ConfiguracionGUI`).
  2. PyAutoGUI mueve el mouse y el teclado de TODO el sistema operativo, no
     solo del navegador: no toques el mouse/teclado mientras corre, y no
     dejes otras ventanas al frente.
  3. Para abortar de emergencia: lleva el mouse a cualquier esquina de la
     pantalla (PyAutoGUI FAILSAFE, activado) o Ctrl+C en la terminal.
"""

from __future__ import annotations

import json
import sys
import time
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.knowledge_store import (  # noqa: E402
    SISTEMAS_CUERPO,
    TIPOS_ENFERMEDAD,
    slugify,
)
from backend.prolog_engine import PrologEngine  # noqa: E402
from rpa.admin_rpa import (  # noqa: E402
    CAMPOS_REQUERIDOS,
    ReporteRPA,
    ResultadoItem,
    clasificar_tipo,
)

RUTA_PL_POR_DEFECTO = Path(__file__).resolve().parent.parent / "prolog" / "knowledge_base.pl"


@dataclass
class ConfiguracionGUI:
    """Parametros ajustables del robot. Los tiempos de espera son
    generosos a proposito (para que el video quede legible); si tu equipo
    es rapido puedes reducirlos."""

    base_url: str = "http://127.0.0.1:5000"
    usuario: str = "admin"
    contrasena: str = "medilogic2026"
    espera_navegacion: float = 1.5  # segundos tras cada carga/redireccion de pagina
    espera_pegado: float = 0.15  # segundos tras cada Ctrl+V
    pl_path: str | Path = RUTA_PL_POR_DEFECTO


# ---------------------------------------------------------------------
# Primitivas de bajo nivel (unicas funciones que tocan mouse/teclado real)
# ---------------------------------------------------------------------
def _navegar(url: str, cfg: ConfiguracionGUI) -> None:
    """Va a `url` usando Ctrl+L (barra de direcciones) en vez de clics."""
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.2)
    pyautogui.write(url, interval=0.01)  # la URL es siempre ASCII
    pyautogui.press("enter")
    time.sleep(cfg.espera_navegacion)


def _escribir(texto: str, cfg: ConfiguracionGUI) -> None:
    """Escribe `texto` en el campo con foco actual, pegandolo desde el
    portapapeles (ver punto 3 del diseno, arriba)."""
    pyperclip.copy(texto)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(cfg.espera_pegado)


def _tab(n: int = 1) -> None:
    for _ in range(max(n, 0)):
        pyautogui.press("tab")


def _seleccionar_opcion(lista: list[str], valor: str) -> None:
    """Deja un <select> enfocado en `valor`: Home (primera opcion) + Down
    repetido segun el indice de `valor` en `lista` (mismo orden que
    SISTEMAS_CUERPO/TIPOS_ENFERMEDAD, que es como los renderiza la
    plantilla)."""
    indice = lista.index(valor)
    pyautogui.press("home")
    for _ in range(indice):
        pyautogui.press("down")


def _marcar_checkboxes(catalogo: list[str], objetivos: list[str]) -> int:
    """Con el foco ya en la casilla de indice 0 de `catalogo`, avanza con
    Tab hasta cada indice objetivo (en orden ascendente) y presiona Espacio
    para marcarlo. Devuelve el indice en el que quedo el foco al terminar,
    para que el llamador sepa cuantos Tab le faltan para salir de la
    lista."""
    posicion = 0
    for objetivo in sorted(objetivos, key=catalogo.index):
        indice_objetivo = catalogo.index(objetivo)
        _tab(indice_objetivo - posicion)
        pyautogui.press("space")
        posicion = indice_objetivo
    return posicion


# ---------------------------------------------------------------------
# Pasos de alto nivel
# ---------------------------------------------------------------------
def _login(cfg: ConfiguracionGUI) -> None:
    """Asume que la pagina de login YA esta cargada (ver
    `ejecutar_carga_gui`): el campo "usuario" tiene autofocus."""
    _escribir(cfg.usuario, cfg)
    _tab()
    _escribir(cfg.contrasena, cfg)
    pyautogui.press("enter")  # unico boton submit del formulario
    time.sleep(cfg.espera_navegacion)


def _crear_catalogo_faltante(
    nombres: list[str], url_pagina: str, cfg: ConfiguracionGUI, existentes: set[str]
) -> None:
    """Da de alta, vía la interfaz, cada nombre de `nombres` cuyo atomo
    (slugify) no este ya en `existentes` (que se actualiza en el sitio)."""
    for nombre in nombres:
        atomo = slugify(nombre)
        if atomo in existentes:
            continue
        _navegar(url_pagina, cfg)
        _escribir(nombre, cfg)
        pyautogui.press("enter")
        time.sleep(cfg.espera_navegacion)
        existentes.add(atomo)


def _llenar_enfermedad(
    registro: dict,
    tipo: str,
    sistema: str,
    catalogo_sintomas: list[str],
    catalogo_medicamentos: list[str],
    cfg: ConfiguracionGUI,
) -> None:
    """Llena y envia el formulario "Nueva enfermedad" para un registro del
    JSON, ya con los catalogos de sintomas/medicamentos actualizados."""
    objetivo_sintomas = [slugify(s) for s in registro["sintomas_asociados"]]
    objetivo_medicamentos = [slugify(m) for m in registro["medicamentos_contraindicados"]]

    _navegar(f"{cfg.base_url}/admin/enfermedades", cfg)
    _escribir(registro["nombre_enfermedad"], cfg)  # campo "Nombre": autofocus
    _tab()
    _seleccionar_opcion(SISTEMAS_CUERPO, sistema)
    _tab()
    _seleccionar_opcion(TIPOS_ENFERMEDAD, tipo)
    _tab()
    _escribir(registro["descripcion"], cfg)
    _tab()  # entra a la casilla de sintomas en indice 0

    posicion = _marcar_checkboxes(catalogo_sintomas, objetivo_sintomas)
    _tab(len(catalogo_sintomas) - 1 - posicion)  # termina la lista de sintomas
    _tab()  # entra a la casilla de medicamentos en indice 0

    posicion = _marcar_checkboxes(catalogo_medicamentos, objetivo_medicamentos)
    _tab(len(catalogo_medicamentos) - 1 - posicion)  # termina la lista de medicamentos
    _tab()  # boton "Guardar" (unico boton visible en modo creacion)
    pyautogui.press("enter")
    time.sleep(cfg.espera_navegacion)


# ---------------------------------------------------------------------
# Orquestacion
# ---------------------------------------------------------------------
def ejecutar_carga_gui(
    ruta_json: str | Path,
    cfg: ConfiguracionGUI | None = None,
    directorio_reportes: str | Path = "reportes",
    pausa_inicial: float = 5.0,
) -> ReporteRPA:
    """Ejecuta el RPA operando la interfaz web real con PyAutoGUI: abre el
    navegador, inicia sesion, y llena el formulario de "Nueva enfermedad"
    (mas los catalogos de sintomas/medicamentos que hagan falta) para cada
    registro de `ruta_json`. Pensado para grabarse en el video de
    evidencia. Devuelve el mismo tipo de reporte que el modo rapido
    (`rpa.admin_rpa.ejecutar_carga`), con su propia bitacora en texto
    plano.
    """
    cfg = cfg or ConfiguracionGUI()
    ruta_json = Path(ruta_json)
    registros = json.loads(ruta_json.read_text(encoding="utf-8"))
    if isinstance(registros, dict):
        registros = [registros]

    # Motor de SOLO LECTURA: se usa unicamente para saber en que posicion
    # alfabetica va a quedar cada checkbox (ver diseno, punto 5). Nunca
    # escribe: todos los cambios de datos pasan por la interfaz.
    engine = PrologEngine(cfg.pl_path)

    print(f"Iniciando en {pausa_inicial:.0f}s: deja el navegador listo y con foco...")
    time.sleep(pausa_inicial)

    pyautogui.FAILSAFE = True  # mover el mouse a una esquina aborta de inmediato
    inicio = datetime.now()

    webbrowser.open(f"{cfg.base_url}/admin/login")
    time.sleep(cfg.espera_navegacion * 2)  # la primera carga del navegador es mas lenta
    _login(cfg)

    items: list[ResultadoItem] = []
    for registro in registros:
        nombre = registro.get("nombre_enfermedad", "(sin nombre)")
        try:
            faltantes = [c for c in CAMPOS_REQUERIDOS if c not in registro]
            if faltantes:
                raise ValueError(f"Faltan campos requeridos: {', '.join(faltantes)}")

            tipo = clasificar_tipo(registro["descripcion"])
            sistema = slugify(registro["sistema_cuerpo"])
            atomo = slugify(nombre)
            existia = atomo in {e["nombre"] for e in engine.enfermedades()}

            engine.reload()
            existentes_sintomas = set(engine.sintomas())
            _crear_catalogo_faltante(
                registro["sintomas_asociados"],
                f"{cfg.base_url}/admin/sintomas",
                cfg,
                existentes_sintomas,
            )

            engine.reload()
            existentes_medicamentos = set(engine.medicamentos())
            _crear_catalogo_faltante(
                registro["medicamentos_contraindicados"],
                f"{cfg.base_url}/admin/medicamentos",
                cfg,
                existentes_medicamentos,
            )

            engine.reload()
            _llenar_enfermedad(
                registro, tipo, sistema, engine.sintomas(), engine.medicamentos(), cfg
            )

            items.append(
                ResultadoItem(
                    nombre_original=nombre,
                    atomo=atomo,
                    sistema_cuerpo=sistema,
                    tipo=tipo,
                    estado="actualizada" if existia else "creada",
                )
            )
        except Exception as exc:  # noqa: BLE001 - se reporta al administrador
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
    reporte = ReporteRPA(archivo_origen=ruta_json.name, inicio=inicio, fin=fin, items=items)

    destino = Path(directorio_reportes)
    destino.mkdir(parents=True, exist_ok=True)
    ruta_bitacora = destino / f"rpa_gui_carga_{inicio.strftime('%Y%m%d_%H%M%S')}.txt"
    ruta_bitacora.write_text(reporte.texto_bitacora(), encoding="utf-8")
    reporte.ruta_bitacora = ruta_bitacora

    return reporte
