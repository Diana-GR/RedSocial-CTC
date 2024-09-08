from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.session, name="login"),
    path("logout/", views.delete_session, name="logout"),
    path("about-us/", views.aboutus, name="about-us"),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("comentarios/<int:post_id>/", views.comentarios_view, name="comentarios_view"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
]
