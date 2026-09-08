from django.db import models
from django.conf import settings

class Mensaje(models.Model):
    texto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='mensajes/', blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'id']

    @property
    def urls_imagenes(self):
        urls = []
        if self.imagen:
            urls.append(self.imagen.url)
        for extra in self.imagenes_extra.all():
            urls.append(extra.imagen.url)
        return urls

    def __str__(self):
        return self.texto[:50]

class MensajeImagen(models.Model):
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name='imagenes_extra')
    imagen = models.ImageField(upload_to='mensajes/')

    class Meta:
        ordering = ['id']

class PreferenciaUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferencias')
    oculto_popup_bienvenida = models.BooleanField(default=False)