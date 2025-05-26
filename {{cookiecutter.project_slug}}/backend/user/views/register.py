import os

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class RegisterUser(APIView):
    def register_user(request):
        data = request.data
        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Email already exists"}, status=400)

        user = User.objects.create(
            username=data["username"],
            email=data["email"],
            password=make_password(data["password"]),
            is_active=False,
        )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_link = f"http://{os.getenv('DOMAIN')}/api/activate/{uid}/{token}/"

        send_mail(
            subject="Confirm your email",
            message=f"Click here to activate your account: {activation_link}",
            from_email=f"no-reply@{os.getenv('DOMAIN')}",
            recipient_list=[user.email],
        )

        return Response(
            {"success": "Check your email to activate your account."}, status=201
        )
