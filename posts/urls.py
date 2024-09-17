from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.session, name="login"),
    path("logout/", views.delete_session, name="logout"),
    path("about-us/", views.aboutus, name="about-us"),
    path("profile/", views.profile, name="profile"),  # Perfil del usuario autenticado
    path(
        "profile/<int:user_id>/", views.profile, name="profile_otros"
    ),  # Perfil de otros usuarios
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("comentarios/<int:post_id>/", views.comentarios_view, name="comentarios_view"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
    path("like_comment/<int:comment_id>/", views.like_comment, name="like_comment"),
    path("buscar/", views.buscarUser, name="buscarUser"),
    path("seguir/<int:user_id>/", views.seguirUser, name="seguirUser"),
]
