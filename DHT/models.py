
# Create your models here.
from django.db import models
class Dht11(models.Model):
  temp = models.FloatField(null=True)
  hum = models.FloatField(null=True)
  dt = models.DateTimeField(auto_now_add=True,null=True)
from django.db import models

class Incident(models.Model):
    date_debut = models.DateTimeField(auto_now_add=True, verbose_name="Date de début")
    date_fin = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    iterations = models.IntegerField(default=0, verbose_name="Compteur d'itérations")
    est_ouvert = models.BooleanField(default=True, verbose_name="Incident ouvert")

    def __str__(self):
        return f"Incident du {self.date_debut}"

    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"

class Alerte(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='alertes', verbose_name="Incident associé")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    message = models.TextField(verbose_name="Message d'alerte")
    utilisateurs_avertis = models.CharField(max_length=255, verbose_name="Utilisateurs avertis")

    def __str__(self):
        return f"Alerte du {self.date_envoi}"

    class Meta:
        verbose_name = "Alerte"
        verbose_name_plural = "Alertes"