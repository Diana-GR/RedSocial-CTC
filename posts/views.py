# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Utilizamos el modelo integrado User
from django.contrib.auth import login, authenticate, logout
from .models import Profile, Post, Comentario, Amistad
from .forms import ProfileForm
from django.db.models import Q


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
    form = ProfileForm
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
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    post.save()
    return redirect("home")


def like_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect("login")

    comentario = get_object_or_404(Comentario, id=comment_id)
    post_id = comentario.post.id

    # Verificar si el usuario ya ha dado like a este comentario
    if request.user in comentario.likes.all():
        comentario.likes.remove(request.user)
    else:
        comentario.likes.add(request.user)

    comentario.save()
    return redirect("comentarios_view", post_id=post_id)


def aboutus(request):
    return render(request, "about-us.html")


def seguirUser(request, user_id):
    if not request.user.is_authenticated:
        return redirect("login")

    usuario_a_seguir = get_object_or_404(User, id=user_id)

    # Verifica si el usuario ya está siguiendo a este usuario
    if request.user != usuario_a_seguir:
        amistad, created = Amistad.objects.get_or_create(
            usuario=request.user, amigo=usuario_a_seguir
        )
        # En caso de que la amistad ya exista, no se crea una nueva
        if not created:
            amistad.delete()  # Si ya existe, se elimina la relación

    return redirect("home")  # modificar a donde redirigir


def buscarUser(request):
    query = request.GET.get("q")
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(profile__biography__icontains=query)
        )
    else:
        users = User.objects.none()

    return render(request, "buscador.html", {"users": users})
