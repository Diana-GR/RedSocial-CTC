from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Utilizamos el modelo integrado User
from django.contrib.auth import login, authenticate, logout
from .models import Profile, Post, Comentario
from .forms import ProfileForm


def index(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "inicio.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        print(request.POST)
        try:
            if request.POST["password1"] == request.POST["password2"]:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("home")
            else:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Las contraseñas no coinciden"},
                )
        except:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "error": "El usuario ya existe"},
            )


def session(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm,
                    "error": "El username o password es incorrecto",
                },
            )
        login(request, user)
        return redirect("home")


def delete_session(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("index")
    else:
        return redirect("login")


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    # Si se está creando un nuevo post
    if request.method == "POST":
        if "contenido" in request.POST:
            contenido = request.POST.get("contenido")
            if contenido:
                nuevo_post = Post.objects.create(
                    usuario=request.user, contenido=contenido
                )
                nuevo_post.save()
                return redirect("home")
        # Si se está creando un comentario
        elif "contenido_comentario" in request.POST:
            contenido_comentario = request.POST.get("contenido_comentario")
            post_id = request.POST.get("post_id")
            post = get_object_or_404(Post, id=post_id)
            if contenido_comentario:
                nuevo_comentario = Comentario.objects.create(
                    usuario=request.user, post=post, contenido=contenido_comentario
                )
                nuevo_comentario.save()
                return redirect("home")
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})


def comentarios_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all()
    return render(
        request, "comentarios_view.html", {"post": post, "comentarios": comentarios}
    )


def profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    return render(request, "profile.html", {"profile": profile})


def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request._files, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
        return render(request, "edit_profile.html", {"form": form})


def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("login")

    post = get_object_or_404(Post, id=post_id)

    # Verificar si el usuario ya ha dado like a esta publicación
    if request.user in post.reacciones.all():
        post.reacciones.remove(request.user)
        post.likes -= 1
    else:
        post.reacciones.add(request.user)
        post.likes += 1

    post.save()
    return redirect("home")


def aboutus(request):
    return render(request, "about-us.html")
