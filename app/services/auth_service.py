from __future__ import annotations

from typing import Any

from app.services.supabase_client import create_supabase_client


class AuthService:
    def login(self, email: str, password: str) -> dict[str, Any]:
        supabase = create_supabase_client()
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {
            "user_id": response.user.id,
            "email": response.user.email,
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }
