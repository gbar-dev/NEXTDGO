from django.urls import path

from .views.login import GoogleLoginView, LoginView
from .views.register import RegisterUser

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("login/google/", GoogleLoginView.as_view(), name="google_login"),
]
