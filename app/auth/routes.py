from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.services.auth_service import AuthService

bp = Blueprint("auth", __name__)
auth_service = AuthService()


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Informe email e senha.", "danger")
            return render_template("login.html")

        try:
            auth_data = auth_service.login(email, password)
            session["access_token"] = auth_data["access_token"]
            session["refresh_token"] = auth_data["refresh_token"]
            session["user_email"] = auth_data["email"]
            session["user_id"] = auth_data["user_id"]
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("main.formulario"))
        except Exception as exc:
            error_message = str(exc).lower()
            if any(token in error_message for token in ["network", "conexão", "connection", "timed out", "urlerror"]):
                flash("Falha de conexão com o Supabase. Verifique SUPABASE_URL e SUPABASE_KEY.", "danger")
            elif any(token in error_message for token in ["invalid login credentials", "credenciais", "invalid", "401", "403"]):
                flash("Credenciais inválidas ou sessão expirada.", "danger")
            else:
                flash("Não foi possível autenticar no Supabase.", "danger")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))
