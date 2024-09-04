from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.session, name="login"),
    path("about-us/", views.aboutus, name="about-us"),
    path("profile/", views.profile, name="perfil"),
    path("signup/", views.signup, name="signup"),
    # path("", views.index, name = "index")
]
