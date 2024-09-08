from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile
from django.contrib.auth.models import User


# Permite que los campos se muestren de manera apilada
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


# Hereda de la administracion base del usuario y permitira editar o crear en la misma vista
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Para quitar el registro de usuario predeterminado
admin.site.unregister(User)
# Para registrar el usuario de manera personalizada
admin.site.register(User, UserAdmin)
