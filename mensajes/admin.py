from django import forms
from django.contrib import admin
from django.db import models

from .models import Mensaje, MensajeImagen


class MensajeImagenInline(admin.TabularInline):
    model = MensajeImagen
    extra = 1


class MensajeAdmin(admin.ModelAdmin):
    inlines = [MensajeImagenInline]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 6, 'cols': 80})},
    }


admin.site.register(Mensaje, MensajeAdmin)