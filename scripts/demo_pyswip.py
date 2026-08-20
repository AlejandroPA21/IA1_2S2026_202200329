"""
MediLogic - Demostracion de knowledge_base.pl consultado desde Python (pyswip).

Uso (desde la raiz del repositorio, con el entorno virtual activado):
    python scripts/demo_pyswip.py

Ejecuta las mismas 5 consultas de referencia que scripts/demo_prolog.pl, pero
a traves de pyswip, para evidenciar que el backend Python puede comunicarse
con el motor logico tal como lo exige el enunciado (seccion 4.3: el motor
logico se ejecuta "sobre el lenguaje python" via pyswip).
"""

from pathlib import Path

from pyswip import Prolog

KB_PATH = Path(__file__).resolve().parent.parent / "src" / "prolog" / "knowledge_base.pl"


def main() -> None:
    prolog = Prolog()
    prolog.consult(str(KB_PATH))

    print("=" * 60)
    print("Consulta 1: afinidad/3 (via pyswip)")
    print("=" * 60)
    resultado = list(prolog.query(
        "afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P)"
    ))
    print("afinidad(hipertension, [dolor_cabeza-moderado, mareo-severo], P) ->", resultado)

    print("\n" + "=" * 60)
    print("Consulta 2: nivel_urgencia/3 (via pyswip)")
    print("=" * 60)
    resultado = list(prolog.query("nivel_urgencia(56, Nivel, Recomendacion)"))
    print("nivel_urgencia(56, Nivel, Recomendacion) ->", resultado)

    print("\n" + "=" * 60)
    print("Consulta 3: medicamento_sugerido/4 (via pyswip)")
    print("=" * 60)
    resultado = list(prolog.query(
        "medicamento_sugerido(hipertension, [losartan], [], Medicamento)"
    ))
    print("medicamento_sugerido(hipertension, [losartan], [], Medicamento) ->", resultado)

    print("\n" + "=" * 60)
    print("Consulta 4: diagnosticar/2 (via pyswip)")
    print("=" * 60)
    resultado = list(prolog.query(
        "diagnosticar([dolor_cabeza-moderado, mareo-severo, dolor_abdominal-leve], D)"
    ))
    print("diagnosticar([...], D) ->", resultado)

    print("\n" + "=" * 60)
    print("Consulta 5: informe/4 (via pyswip)")
    print("=" * 60)
    resultado = list(prolog.query(
        "informe([dolor_cabeza-moderado, mareo-severo], [ibuprofeno], [], Informe)"
    ))
    print("informe([...], [ibuprofeno], [], Informe) ->", resultado)
    print("=" * 60)


if __name__ == "__main__":
    main()
