from django.contrib import admin
from .models import Personnel

# Register your models here.

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "prenom", "matricule", "telephone", "mail", "adresse", "fonction")
    search_fields = ("nom", "prenom", "mail")
