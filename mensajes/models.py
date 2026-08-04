from django.db import models

class Mensaje(models.Model):
    texto = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=250, blank=True)
    imagen = models.ImageField(upload_to='mensajes/', blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return self.texto[:50]
