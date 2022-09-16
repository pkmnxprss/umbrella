from django.urls import path

from . import views

urlpatterns = [
    # Path for user registration page.
    # Full address will be auth/signup/ but the auth/ prefix will be handled in the core urls.py
    path("signup/", views.SignUp.as_view(), name="signup")
]
