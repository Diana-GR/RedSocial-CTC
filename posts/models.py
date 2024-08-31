from django.db import models
from django.contrib.auth.models import User  # Django ya lo tiene implementado


# Modelo de Usuario
class Usuario(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Relaciona con el modelo User de Django
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    biografia = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


# Modelo de Publicación
class Post(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post de {self.usuario.nombre} - {self.fecha_publicacion}"


# Modelo de Comentario
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.nombre} en {self.post}"


# Modelo de Compartido
class Compartido(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_compartido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} compartió {self.post}"


# Modelo de Amistad
class Amistad(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="amistades"
    )
    amigo = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="amigos")
    fecha_amistad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} es amigo de {self.amigo.nombre}"


# Modelo de Reacción
class Reaccion(models.Model):
    TIPOS_REACCION = [
        ("me encanta", "Me encanta"),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPOS_REACCION)
    fecha_reaccion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} reaccionó '{self.tipo}' a {self.post}"
