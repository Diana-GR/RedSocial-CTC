from django import forms
from django.forms import ModelForm
from .models import Task, Profile, Comentario, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["contenido"]

    contenido = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Escribe tu publicación aquí..."}),
        label="",
    )


# Servira para editar algún usuario
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["biography", "avatar"]
