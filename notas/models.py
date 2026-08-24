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