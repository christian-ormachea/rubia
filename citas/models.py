from django.db import models

class Cita(models.Model):
    PLAN_CHOICES = [
        ('comida', '🍽️ Comida'),
        ('cine', '🎬 Cine'),
        ('pasear', '🚶 Pasear a Pincho'),
        ('casa', '🏡 Plan en casa'),
        ('sorpresa', '🎁 Sorpresa'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField(blank=True, null=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='sorpresa')

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"