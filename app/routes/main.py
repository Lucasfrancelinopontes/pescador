from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.services.supabase_client import create_supabase_client

bp = Blueprint("main", __name__)


def _login_required():
    if not session.get("access_token"):
        flash("Faça login para acessar o formulário.", "warning")
        return redirect(url_for("main.login"))
    return None


@bp.route("/")
def index():
    if session.get("access_token"):
        return redirect(url_for("main.formulario"))
    return redirect(url_for("main.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Informe email e senha.", "danger")
            return render_template("login.html")

        try:
            supabase = create_supabase_client()
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            session["access_token"] = auth_response.session.access_token
            session["refresh_token"] = auth_response.session.refresh_token
            session["user_email"] = auth_response.user.email
            session["user_id"] = auth_response.user.id

            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("main.formulario"))
        except Exception:
            flash("Falha no login. Verifique suas credenciais.", "danger")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("main.login"))


@bp.route("/formulario", methods=["GET", "POST"])
def formulario():
    guard = _login_required()
    if guard:
        return guard

    if request.method == "POST":
        # Futuras validações de schema e normalização dos campos podem entrar aqui.
        client = create_supabase_client(session.get("access_token"))
        dados = request.form.to_dict(flat=True)
        dados["entrega_atravessador"] = request.form.get("entrega_atravessador") == "on"
        dados["created_by"] = session.get("user_id")
        dados["created_by_email"] = session.get("user_email")

        try:
            client.table("coletas").insert(dados).execute()
            flash("Formulário salvo com sucesso.", "success")
            return redirect(url_for("main.formulario"))
        except Exception:
            flash("Não foi possível salvar os dados no Supabase.", "danger")

    return render_template("formulario.html")
