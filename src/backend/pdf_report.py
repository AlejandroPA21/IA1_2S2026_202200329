"""
Generacion del informe de diagnostico descargable en PDF (seccion 4.2 del
enunciado: "descargar el informe en formato PDF, incluyendo la fecha, un
resumen del diagnostico, las advertencias importantes, los medicamentos
sugeridos, las reglas activadas y el sello visual del sistema").

Se usa ReportLab (ver justificacion en docs/decisiones_tecnicas.md) por ser
Python puro, sin dependencias binarias externas.
"""

from __future__ import annotations

import io
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

URGENCIA_COLOR = {
    "alta": colors.HexColor("#e03131"),
    "media": colors.HexColor("#f08c00"),
    "baja": colors.HexColor("#2f9e44"),
}


def generar_pdf_informe(
    resultados: list[dict[str, Any]],
    sintomas: list[tuple[str, str]],
    alergias: list[str],
    cronicas: list[str],
    reglas_por_enfermedad: dict[str, list[str]] | None = None,
) -> bytes:
    """Construye el PDF del informe y devuelve los bytes listos para enviar."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle(
        "TituloMedilogic",
        parent=estilos["Title"],
        textColor=colors.HexColor("#12514e"),
    )
    subtitulo = ParagraphStyle(
        "SubtituloMedilogic", parent=estilos["Normal"], textColor=colors.HexColor("#5b6472")
    )
    seccion = ParagraphStyle(
        "SeccionMedilogic",
        parent=estilos["Heading2"],
        textColor=colors.HexColor("#12514e"),
        spaceBefore=14,
    )
    reglas_estilo = ParagraphStyle(
        "ReglasMedilogic",
        parent=estilos["Code"],
        fontSize=8,
        textColor=colors.HexColor("#333333"),
        backColor=colors.HexColor("#f4f6f8"),
    )

    reglas_por_enfermedad = reglas_por_enfermedad or {}
    elementos = []

    elementos.append(Paragraph("MediLogic — Informe de diagnóstico preliminar", titulo))
    elementos.append(
        Paragraph(
            f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitulo
        )
    )
    elementos.append(
        Paragraph(
            "⚠ Esta herramienta ofrece orientación preliminar y no sustituye "
            "la consulta médica profesional.",
            subtitulo,
        )
    )
    elementos.append(Spacer(1, 10))
    elementos.append(HRFlowable(width="100%", color=colors.HexColor("#e2e8f0")))

    elementos.append(Paragraph("Datos ingresados", seccion))
    sintomas_txt = ", ".join(f"{s} ({sev})" for s, sev in sintomas) or "Ninguno"
    alergias_txt = ", ".join(alergias) or "Ninguna"
    cronicas_txt = ", ".join(cronicas) or "Ninguna"
    elementos.append(Paragraph(f"<b>Síntomas:</b> {sintomas_txt}", estilos["Normal"]))
    elementos.append(Paragraph(f"<b>Alergias:</b> {alergias_txt}", estilos["Normal"]))
    elementos.append(
        Paragraph(f"<b>Enfermedades crónicas:</b> {cronicas_txt}", estilos["Normal"])
    )

    elementos.append(Paragraph("Diagnósticos sugeridos", seccion))

    if not resultados:
        elementos.append(
            Paragraph(
                "No se encontraron enfermedades compatibles con los síntomas "
                "seleccionados.",
                estilos["Normal"],
            )
        )
    for i, r in enumerate(resultados, start=1):
        color = URGENCIA_COLOR.get(r["urgencia"], colors.grey)
        elementos.append(Spacer(1, 8))
        tabla = Table(
            [
                [
                    Paragraph(
                        f"<b>{i}. {r['enfermedad'].replace('_', ' ').title()}</b>",
                        estilos["Normal"],
                    ),
                    Paragraph(f"<b>{r['afinidad']}%</b>", estilos["Normal"]),
                ],
                [
                    Paragraph(r["recomendacion"], ParagraphStyle("rec", textColor=color)),
                    "",
                ],
                [
                    Paragraph(
                        f"<b>Medicamento sugerido:</b> "
                        f"{r['medicamento'].replace('_', ' ').title()}",
                        estilos["Normal"],
                    ),
                    "",
                ],
            ],
            colWidths=[13 * cm, 3 * cm],
        )
        tabla.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 1), (1, 1)),
                    ("SPAN", (0, 2), (1, 2)),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f7f9fa")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        elementos.append(tabla)

        reglas = reglas_por_enfermedad.get(r["enfermedad"], [])
        if reglas:
            texto_reglas = "<br/>".join(regla for regla in reglas)
            elementos.append(Spacer(1, 4))
            elementos.append(
                Paragraph(f"Reglas Prolog activadas:<br/>{texto_reglas}", reglas_estilo)
            )

    elementos.append(Spacer(1, 20))
    elementos.append(HRFlowable(width="100%", color=colors.HexColor("#e2e8f0")))
    elementos.append(
        Paragraph(
            "MediLogic — Sistema experto de diagnóstico preliminar · Proyecto "
            "académico Inteligencia Artificial 1 · USAC",
            subtitulo,
        )
    )

    doc.build(elementos)
    return buffer.getvalue()
