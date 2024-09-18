from django.db import models
from django.contrib.auth.models import User  # Django ya lo tiene implementado

User.add_to_class(
    "seguir",
    models.ManyToManyField(
        "self", symmetrical=False, related_name="seguidores", blank=True
    ),
)


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)
    datecompleted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=255, default=" ")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    contenido = models.TextField()
    image = models.ImageField(upload_to="media/posts_images/", blank=True, null=True)
    likes = models.IntegerField(default=0)
    # reacciones = models.ManyToManyField(User, related_name="reacciones", blank=True) - {self.contenido[:20]}
    likes = models.ManyToManyField(User, related_name="likes_publicaciones", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="comentarios_likes", blank=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.post.id}"


# Modelo de Compartido
class Compartido(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compartido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} compartió {self.post}"


# Modelo de Amistad
class Amistad(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="amistades"
    )
    amigo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="amigos")
    fecha_amistad = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "amigo")  # Asegura que la relación sea única
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "amigo"], name="unique_friendship"
            ),
        ]

    def __str__(self):
        return f"{self.usuario.username} es amigo de {self.amigo.username}"
