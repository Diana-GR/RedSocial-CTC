from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Utilizamos el modelo integrado User
from django.contrib.auth import login, authenticate, logout
from .models import Profile, Post, Comentario, Amistad
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .forms import PostForm
from django.contrib import messages


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
        print(request.POST)
        if "contenido" in request.POST:
            contenido = request.POST.get("contenido")
            print(contenido)
            imagen = request.FILES.get("image")
            print(imagen)
            if contenido or imagen:
                nuevo_post = Post.objects.create(
                    usuario=request.user, contenido=contenido, image=imagen
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
    posts = Post.objects.all().order_by("-fecha_publicacion")
    return render(request, "home.html", {"posts": posts})


def comentarios_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all()
    return render(
        request, "comentarios_view.html", {"post": post, "comentarios": comentarios}
    )


@login_required
def profile(request, user_id=None):
    if user_id:
        # Si se proporciona un user_id, obtenemos el perfil del otro usuario
        user = get_object_or_404(User, id=user_id)
        template = "profile2.html"
    else:
        # Si no hay id, usamos nuestro perfil
        user = request.user
        template = "profile.html"

    profile, created = Profile.objects.get_or_create(user=user)
    posts = Post.objects.filter(usuario=user).order_by("-fecha_publicacion")
    sigue_al_usuario = request.user.seguir.filter(id=user.id).exists()
    print(sigue_al_usuario)
    return render(
        request,
        template,
        {
            "profile": profile,
            "user": user,
            "posts": posts,
            "sigue_al_usuario": sigue_al_usuario,
        },
    )


@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
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


@login_required
def seguirUsers(request, user_id):
    perfil_a_seguir = get_object_or_404(User, id=user_id)

    if request.user == perfil_a_seguir:
        print("Estás intentando seguirte a tí mismo.")
        return redirect("profile")  # No permite que un usuario se siga a sí mismo

    amistad, created = Amistad.objects.get_or_create(
        usuario=request.user, amigo=perfil_a_seguir
    )

    if created:
        print(f"{request.user.username} empezó a seguir a {perfil_a_seguir.username}.")
    else:
        amistad.delete()  # dejar de seguir
        print(f"{request.user.username} dejó de seguir a {perfil_a_seguir.username}.")

    return redirect("profile_otros", user_id=user_id)


@login_required
def seguirUser(request, user_id):
    perfil_a_seguir = get_object_or_404(User, id=user_id)

    if request.user == perfil_a_seguir:
        # No permitir que un usuario se siga a sí mismo
        print("Estás intentando seguirte a ti mismo.")
        return redirect("profile", user_id=user_id)

    # Verificar si ya sigue al usuario
    if perfil_a_seguir in request.user.seguir.all():
        # Si ya lo sigue, eliminar la relación (dejar de seguir)
        request.user.seguir.remove(perfil_a_seguir)
        print(f"{request.user.username} dejó de seguir a {perfil_a_seguir.username}.")
    else:
        # Si no lo sigue, añadir la relación (empezar a seguir)
        request.user.seguir.add(perfil_a_seguir)
        print(f"{request.user.username} empezó a seguir a {perfil_a_seguir.username}.")

    return redirect("profile_otros", user_id=user_id)


def buscar(request):
    query = request.GET.get("q")
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(profile__biography__icontains=query)
        )
    else:
        users = User.objects.none()

    return render(request, "buscador.html", {"users": users})


def buscarUser(request):
    query = request.GET.get("q", "")
    users = User.objects.filter(
        Q(username__icontains=query) | Q(profile__biography__icontains=query)
    ).values("id", "username")
    return JsonResponse({"results": list(users)})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(
            request.POST, request.FILES, instance=post
        )  # Asigna la instancia del post
        if form.is_valid():
            post = form.save(commit=False)  # No lo guarda aún
            post.usuario = request.user  # Asigna el usuario
            post.save()  # Ahora lo guarda
            return redirect("profile")
    else:
        form = PostForm(instance=post)  # Cargar el post existente en el formulario

    return render(request, "edit_post.html", {"form": form})


def deletepost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Publicación eliminada con éxito.")
    return redirect("profile")  # Cambia a la URL que desees
