from django import forms
from django.forms import ModelForm
from .models import Database, Categorias, Banners, CustomUser

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Database
        fields = ['titulo']
    
    def save(self, commit=True):
        pregunta = super().save(commit=False)
        pregunta.categoria = Categorias.objects.get(categoria="Preguntas")
        if commit:
            pregunta.save()
        return pregunta

class BannersForm(forms.ModelForm):
    class Meta:
        model = Banners
        fields = ['titulo', 'descripcion', 'articulo', 'imagen', 'expiracion']

class CSVUploadForm(forms.Form):
    file = forms.FileField()

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']