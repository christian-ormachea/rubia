from django.db import models
from django.conf import settings


class Nota(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notas',
    )
    titulo = models.TextField(default='Sin titulo')
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='notas/', blank=True, null=True)
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creada']

    def __str__(self):
        return f'Nota de {self.autor} - {self.creada:%d/%m/%Y}'

    @property
    def urls_imagenes(self):
        urls = []
        if self.imagen:
            urls.append(self.imagen.url)
        for extra in self.imagenes_extra.all():
            urls.append(extra.imagen.url)
        return urls


class NotaImagen(models.Model):
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE, related_name='imagenes_extra')
    imagen = models.ImageField(upload_to='notas/')

    class Meta:
        ordering = ['id']