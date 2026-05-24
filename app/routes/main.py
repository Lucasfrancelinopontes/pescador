from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from app.services.coleta_service import ColetaService
from app.services.supabase_client import create_supabase_client
from app.utils.auth import login_required

bp = Blueprint("main", __name__)
coleta_service = ColetaService()


def _require_auth():
    if not session.get("access_token"):
        flash("Sua sessão expirou. Faça login novamente.", "warning")
        return redirect(url_for("auth.login"))
    return None


@bp.route("/")
def index():
    if session.get("access_token"):
        return redirect(url_for("main.formulario"))
    return redirect(url_for("auth.login"))


@bp.route("/formulario", methods=["GET", "POST"])
@login_required
def formulario():
    if request.method == "POST":
        client = create_supabase_client(session.get("access_token"))
        try:
            coleta_service.submit_complete(client, request.form, session.get("user_id"))
            flash("Formulário salvo com sucesso.", "success")
            return redirect(url_for("main.formulario"))
        except Exception as exc:
            flash(f"Não foi possível salvar os dados no Supabase: {exc}", "danger")

    return render_template("formulario.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    return jsonify({"status": "ok", "message": "Dashboard protegido disponível."})


@bp.route("/exportacao")
@login_required
def exportacao():
    return jsonify({"status": "ok", "message": "Exportação protegida disponível."})
