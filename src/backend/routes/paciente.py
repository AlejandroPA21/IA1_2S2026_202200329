"""
Rutas del modulo de paciente (seccion 4.2 del enunciado): formulario de
ingreso clinico sin autenticacion, calculo del informe de diagnostico via el
motor Prolog, y descarga del informe en PDF.
"""

from __future__ import annotations

from flask import Blueprint, Response, current_app, render_template, request

from backend.pdf_report import generar_pdf_informe

paciente_bp = Blueprint("paciente", __name__, url_prefix="/paciente")


def _engine():
    return current_app.prolog_engine


def _leer_sintomas_del_formulario(form) -> list[tuple[str, str]]:
    seleccionados = form.getlist("sintoma")
    sintomas = []
    for s in seleccionados:
        severidad = form.get(f"severidad_{s}", "leve")
        if severidad not in ("leve", "moderado", "severo"):
            severidad = "leve"
        sintomas.append((s, severidad))
    return sintomas


def _diagnosticar_desde_formulario(form):
    engine = _engine()
    sintomas = _leer_sintomas_del_formulario(form)
    alergias = form.getlist("alergia")
    cronicas = form.getlist("cronica")

    resultados = engine.diagnosticar(sintomas, alergias, cronicas)
    reglas_por_enfermedad = {
        r["enfermedad"]: engine.reglas_activadas(
            r["enfermedad"], sintomas, r["afinidad"], r["urgencia"], r["medicamento"]
        )
        for r in resultados
    }
    return sintomas, alergias, cronicas, resultados, reglas_por_enfermedad


@paciente_bp.get("/")
def formulario():
    engine = _engine()
    return render_template(
        "paciente_formulario.html",
        sintomas=engine.sintomas(),
        alergias=engine.alergias_disponibles(),
        cronicas=engine.enfermedades_cronicas(),
    )


@paciente_bp.post("/diagnostico")
def diagnostico():
    sintomas, alergias, cronicas, resultados, reglas = _diagnosticar_desde_formulario(
        request.form
    )
    return render_template(
        "paciente_resultado.html",
        sintomas=sintomas,
        alergias=alergias,
        cronicas=cronicas,
        resultados=resultados,
        reglas_por_enfermedad=reglas,
        principal=resultados[0] if resultados else None,
    )


@paciente_bp.post("/informe/pdf")
def informe_pdf():
    sintomas, alergias, cronicas, resultados, reglas = _diagnosticar_desde_formulario(
        request.form
    )
    pdf_bytes = generar_pdf_informe(resultados, sintomas, alergias, cronicas, reglas)
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=medilogic_informe.pdf"
        },
    )
