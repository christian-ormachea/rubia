from django.db import models

class Mensaje(models.Model):
    texto = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.texto[:50]
