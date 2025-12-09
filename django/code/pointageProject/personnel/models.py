from django.db import models

# Create your models here.

class Personnel(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    fonction = models.CharField(max_length=100)
    mail = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.matricule}"