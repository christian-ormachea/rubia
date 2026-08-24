from django import forms

from .models import Nota


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'contenido', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Título de la nota',
            }),
            'contenido': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribí algo lindo...',
            }),
        }