"""Pruebas de las primitivas de conteo del RPA visual (src/rpa/gui_automation.py).

No se prueba la automatizacion en si (mover el mouse/teclado real no es
apto para una suite automatizada); estas pruebas verifican unicamente la
LOGICA determinista que decide cuantas veces presionar Tab/Espacio para
llegar a cada checkbox, sustituyendo pyautogui por un doble de prueba que
solo registra las teclas que se "presionarian".
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import rpa.gui_automation as gui_automation  # noqa: E402


def test_marcar_checkboxes_cuenta_tabs_y_espacios_correctamente(monkeypatch):
    presionadas = []
    monkeypatch.setattr(
        gui_automation.pyautogui, "press", lambda tecla: presionadas.append(tecla)
    )

    catalogo = ["dolor_abdominal", "diarrea", "fiebre_leve", "nauseas"]
    objetivos = ["nauseas", "dolor_abdominal", "diarrea"]  # desordenados a proposito

    posicion_final = gui_automation._marcar_checkboxes(catalogo, objetivos)

    # dolor_abdominal(0), diarrea(1), nauseas(3): 0 + 1 + 2 = 3 tabs, 3 espacios
    assert presionadas.count("tab") == 3
    assert presionadas.count("space") == 3
    assert posicion_final == catalogo.index("nauseas")


def test_marcar_checkboxes_sin_objetivos_no_presiona_nada(monkeypatch):
    presionadas = []
    monkeypatch.setattr(
        gui_automation.pyautogui, "press", lambda tecla: presionadas.append(tecla)
    )

    posicion_final = gui_automation._marcar_checkboxes(["a", "b", "c"], [])

    assert presionadas == []
    assert posicion_final == 0


def test_seleccionar_opcion_presiona_home_y_down_segun_indice(monkeypatch):
    presionadas = []
    monkeypatch.setattr(
        gui_automation.pyautogui, "press", lambda tecla: presionadas.append(tecla)
    )

    gui_automation._seleccionar_opcion(gui_automation.SISTEMAS_CUERPO, "digestivo")

    indice_esperado = gui_automation.SISTEMAS_CUERPO.index("digestivo")
    assert presionadas[0] == "home"
    assert presionadas.count("down") == indice_esperado


def test_escribir_pega_desde_portapapeles(monkeypatch):
    copiado = []
    monkeypatch.setattr(gui_automation.pyperclip, "copy", lambda texto: copiado.append(texto))
    monkeypatch.setattr(gui_automation, "pyautogui", MagicMock())

    cfg = gui_automation.ConfiguracionGUI(espera_pegado=0)
    gui_automation._escribir("Migraña Crónica", cfg)

    assert copiado == ["Migraña Crónica"]
    gui_automation.pyautogui.hotkey.assert_called_once_with("ctrl", "v")
