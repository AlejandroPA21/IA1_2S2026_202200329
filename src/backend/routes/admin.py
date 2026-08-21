"""
Rutas del modulo administrador (seccion 4.2 del enunciado): autenticacion,
panel general, CRUD de enfermedades / sintomas / medicamentos /
contraindicaciones, exportacion del archivo .pl y ejecucion del RPA de carga
masiva de enfermedades.
"""

from __future__ import annotations

import functools
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from backend.knowledge_store import ValidationError, SISTEMAS_CUERPO, TIPOS_ENFERMEDAD

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _store():
    return current_app.knowledge_store


def _engine():
    return current_app.prolog_engine


def login_required(vista):
    @functools.wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("admin_autenticado"):
            flash("Inicia sesión para acceder al panel administrativo.", "warning")
            return redirect(url_for("admin.login", siguiente=request.path))
        return vista(*args, **kwargs)

    return envoltura


# ----------------------------------------------------------------------
# Autenticacion
# ----------------------------------------------------------------------
@admin_bp.get("/login")
def login():
    if session.get("admin_autenticado"):
        return redirect(url_for("admin.dashboard"))
    return render_template("admin_login.html")


@admin_bp.post("/login")
def login_post():
    usuario = request.form.get("usuario", "")
    contrasena = request.form.get("contrasena", "")
    if (
        usuario == current_app.config["ADMIN_USER"]
        and contrasena == current_app.config["ADMIN_PASSWORD"]
    ):
        session["admin_autenticado"] = True
        session["admin_usuario"] = usuario
        siguiente = request.form.get("siguiente") or url_for("admin.dashboard")
        return redirect(siguiente)
    flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("admin_login.html"), 401


@admin_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ----------------------------------------------------------------------
# Panel general
# ----------------------------------------------------------------------
@admin_bp.get("/")
@login_required
def dashboard():
    estado = _store().snapshot()
    resumen = {
        "enfermedades": len(estado["enfermedades"]),
        "sintomas": len(estado["sintomas"]),
        "medicamentos": len(estado["medicamentos"]),
    }
    return render_template(
        "admin_dashboard.html", resumen=resumen, seccion_activa="dashboard"
    )


# ----------------------------------------------------------------------
# Enfermedades
# ----------------------------------------------------------------------
@admin_bp.get("/enfermedades")
@login_required
def enfermedades():
    estado = _store().snapshot()
    editar = request.args.get("editar")
    enfermedad_editar = None
    if editar:
        enfermedad_editar = next(
            (e for e in estado["enfermedades"] if e["nombre"] == editar), None
        )
    return render_template(
        "admin_enfermedades.html",
        enfermedades=estado["enfermedades"],
        sintomas=estado["sintomas"],
        medicamentos=estado["medicamentos"],
        sistemas=SISTEMAS_CUERPO,
        tipos=TIPOS_ENFERMEDAD,
        enfermedad_editar=enfermedad_editar,
        seccion_activa="enfermedades",
    )


@admin_bp.post("/enfermedades")
@login_required
def enfermedades_guardar():
    form = request.form
    try:
        atomo = _store().guardar_enfermedad(
            nombre=form["nombre"],
            descripcion=form.get("descripcion", ""),
            sistema_cuerpo=form.get("sistema_cuerpo", "otro"),
            tipo=form.get("tipo", "otro"),
            sintomas=form.getlist("sintomas"),
            medicamentos_contraindicados=form.getlist("medicamentos_contraindicados"),
            nombre_original=form.get("nombre_original") or None,
        )
        flash(f"Enfermedad '{atomo}' guardada correctamente.", "success")
    except ValidationError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("admin.enfermedades"))


@admin_bp.post("/enfermedades/<nombre>/eliminar")
@login_required
def enfermedades_eliminar(nombre):
    _store().eliminar_enfermedad(nombre)
    flash(f"Enfermedad '{nombre}' eliminada.", "success")
    return redirect(url_for("admin.enfermedades"))


# ----------------------------------------------------------------------
# Sintomas
# ----------------------------------------------------------------------
@admin_bp.get("/sintomas")
@login_required
def sintomas():
    estado = _store().snapshot()
    return render_template(
        "admin_sintomas.html", sintomas=estado["sintomas"], seccion_activa="sintomas"
    )


@admin_bp.post("/sintomas")
@login_required
def sintomas_crear():
    try:
        atomo = _store().crear_sintoma(request.form.get("nombre", ""))
        flash(f"Síntoma '{atomo}' registrado.", "success")
    except ValidationError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("admin.sintomas"))


@admin_bp.post("/sintomas/<atomo>/eliminar")
@login_required
def sintomas_eliminar(atomo):
    _store().eliminar_sintoma(atomo)
    flash(f"Síntoma '{atomo}' eliminado.", "success")
    return redirect(url_for("admin.sintomas"))


# ----------------------------------------------------------------------
# Medicamentos
# ----------------------------------------------------------------------
@admin_bp.get("/medicamentos")
@login_required
def medicamentos():
    estado = _store().snapshot()
    nombres_enfermedades = [e["nombre"] for e in estado["enfermedades"]]
    tratamientos = {m: [] for m in estado["medicamentos"]}
    for e in estado["enfermedades"]:
        for m in e["medicamentos_tratan"]:
            tratamientos.setdefault(m, []).append(e["nombre"])
    return render_template(
        "admin_medicamentos.html",
        medicamentos=estado["medicamentos"],
        enfermedades=nombres_enfermedades,
        tratamientos=tratamientos,
        seccion_activa="medicamentos",
    )


@admin_bp.post("/medicamentos")
@login_required
def medicamentos_crear():
    try:
        atomo = _store().crear_medicamento(request.form.get("nombre", ""))
        flash(f"Medicamento '{atomo}' registrado.", "success")
    except ValidationError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("admin.medicamentos"))


@admin_bp.post("/medicamentos/<atomo>/tratamientos")
@login_required
def medicamentos_tratamientos(atomo):
    enfermedades_tratadas = request.form.getlist("enfermedades")
    _store().actualizar_tratamientos(atomo, enfermedades_tratadas)
    flash(f"Enfermedades tratadas por '{atomo}' actualizadas.", "success")
    return redirect(url_for("admin.medicamentos"))


@admin_bp.post("/medicamentos/<atomo>/eliminar")
@login_required
def medicamentos_eliminar(atomo):
    _store().eliminar_medicamento(atomo)
    flash(f"Medicamento '{atomo}' eliminado.", "success")
    return redirect(url_for("admin.medicamentos"))


# ----------------------------------------------------------------------
# Contraindicaciones
# ----------------------------------------------------------------------
@admin_bp.get("/contraindicaciones")
@login_required
def contraindicaciones():
    estado = _store().snapshot()
    return render_template(
        "admin_contraindicaciones.html",
        contraindicaciones=estado["contraindicaciones"],
        medicamentos=estado["medicamentos"],
        enfermedades=[e["nombre"] for e in estado["enfermedades"]],
        seccion_activa="contraindicaciones",
    )


@admin_bp.post("/contraindicaciones")
@login_required
def contraindicaciones_crear():
    medicamento = request.form.get("medicamento", "")
    enfermedad = request.form.get("enfermedad", "")
    if medicamento and enfermedad:
        _store().agregar_contraindicacion(medicamento, enfermedad)
        flash(f"'{medicamento}' marcado como contraindicado en '{enfermedad}'.", "success")
    return redirect(url_for("admin.contraindicaciones"))


@admin_bp.post("/contraindicaciones/eliminar")
@login_required
def contraindicaciones_eliminar():
    medicamento = request.form.get("medicamento", "")
    enfermedad = request.form.get("enfermedad", "")
    _store().eliminar_contraindicacion(medicamento, enfermedad)
    flash("Contraindicación eliminada.", "success")
    return redirect(url_for("admin.contraindicaciones"))


# ----------------------------------------------------------------------
# Archivo .pl
# ----------------------------------------------------------------------
@admin_bp.get("/pl/exportar")
@login_required
def exportar_pl():
    ruta = _engine().pl_path
    return send_file(
        ruta, as_attachment=True, download_name="knowledge_base.pl", mimetype="text/plain"
    )


# ----------------------------------------------------------------------
# RPA - carga masiva de enfermedades
# ----------------------------------------------------------------------
@admin_bp.get("/rpa")
@login_required
def rpa():
    return render_template("admin_rpa.html", reporte=None, seccion_activa="rpa")


@admin_bp.post("/rpa/ejecutar")
@login_required
def rpa_ejecutar():
    from rpa.admin_rpa import ejecutar_carga  # import local: evita ciclo en el arranque

    archivo = request.files.get("archivo")
    if not archivo or not archivo.filename:
        flash("Selecciona un archivo JSON con las enfermedades a cargar.", "danger")
        return redirect(url_for("admin.rpa"))

    subida = Path(current_app.instance_path) / "rpa_uploads"
    subida.mkdir(parents=True, exist_ok=True)
    ruta_temporal = subida / secure_filename(archivo.filename)
    archivo.save(ruta_temporal)

    try:
        reporte = ejecutar_carga(
            ruta_temporal,
            _store(),
            directorio_reportes=Path(current_app.instance_path) / "reportes",
        )
        flash(
            f"RPA finalizado: {reporte.creadas} creadas, {reporte.actualizadas} "
            f"actualizadas, {reporte.errores} errores.",
            "success" if reporte.errores == 0 else "warning",
        )
    except Exception as exc:  # noqa: BLE001 - se reporta al administrador
        flash(f"El RPA no pudo procesar el archivo: {exc}", "danger")
        return redirect(url_for("admin.rpa"))

    return render_template("admin_rpa.html", reporte=reporte, seccion_activa="rpa")


@admin_bp.get("/rpa/bitacora/<nombre_archivo>")
@login_required
def rpa_bitacora(nombre_archivo):
    ruta = Path(current_app.instance_path) / "reportes" / secure_filename(nombre_archivo)
    return send_file(ruta, as_attachment=True, mimetype="text/plain")
