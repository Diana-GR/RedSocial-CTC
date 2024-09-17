from django.db import models
from django.contrib.auth.models import User  # Django ya lo tiene implementado


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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)  # Campo para contar likes
    reacciones = models.ManyToManyField(User, related_name="reacciones", blank=True)

    def __str__(self):
        return f"Post de {self.usuario.username} - {self.contenido[:20]}"


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"{self.usuario.nombre} es amigo de {self.amigo.nombre}"
