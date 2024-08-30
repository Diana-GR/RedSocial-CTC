from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.session, name="login"),
    path("about-us/", views.aboutUs, name="about-us"),
    path("perfil/", views.perfil, name="perfil"),
    # path("", views.index, name = "index")
]
