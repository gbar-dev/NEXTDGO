from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework.views import APIView


class EmailVerification(APIView):
    def activate_user(request, uidb64, token):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"success": "Account activated"}, status=200)
        else:
            return Response({"error": "Link expired or invalid"}, status=400)
