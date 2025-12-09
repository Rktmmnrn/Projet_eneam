from django.db import models
from personnel.models import Personnel

class Pointage(models.Model):
    TYPE_POINTAGE = [
        ('arrivee', 'Arrivée'),
        ('depart', 'Départ'),
        ('pause_debut', 'Début Pause'),
        ('pause_fin', 'Fin Pause'),
    ]
    
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name="pointages")
    type_pointage = models.CharField(max_length=20, choices=TYPE_POINTAGE)
    datetime_pointage = models.DateTimeField(auto_now_add=True)  # Date + heure automatique
    notes = models.TextField(blank=True, null=True)
    appareil_id = models.CharField(max_length=100, blank=True)  # Pour identifier la source
    
    # Pour la synchronisation
    synced_with_odoo = models.BooleanField(default=False)
    # odoo_pointage_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.personnel.matricule} - {self.get_type_pointage_display()} - {self.datetime_pointage}"

    class Meta:
        ordering = ['-datetime_pointage']

        indexes = [
            models.Index(fields=['personnel', 'datetime_pointage']),
        ]