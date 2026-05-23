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
        except Exception:
            flash("Credenciais inválidas ou sessão expirada.", "danger")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))
