import json
import os
from datetime import datetime, timedelta, timezone

import jose
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

# Configuration JWE
JWE_SECRET = os.getenv("SECRET_KEY").encode()
JWE_ALG = "dir"
JWE_ENC = "HS512"


def generate_jwe(payload: dict) -> str:
    return jose.encrypt(
        json.dumps(payload).encode(), JWE_SECRET, algorithm=JWE_ALG, encryption=JWE_ENC
    )


def set_cookie(response, token):
    max_age = 60 * 60  # 1 hour
    expires = datetime.now(timezone.utc) + timedelta(seconds=max_age)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=max_age,
        expires=expires,
    )
    return response


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password required"}, status=400)

        user = authenticate(request, username=email, password=password)

        if user is None or not user.is_active:
            return Response(
                {"error": "Invalid credentials or inactive account"}, status=401
            )

        payload = {
            "sub": user.id,
            "email": user.email,
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
        }

        token = generate_jwe(payload)
        response = JsonResponse({"message": "Login successful"})
        return set_cookie(response, token)


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        user = self.user

        payload = {
            "sub": user.id,
            "email": user.email,
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
        }

        token = generate_jwe(payload)
        response = JsonResponse({"message": "Google login successful"})
        return set_cookie(response, token)
