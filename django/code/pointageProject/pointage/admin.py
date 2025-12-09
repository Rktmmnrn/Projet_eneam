from django.contrib import admin
from .models import Pointage

@admin.register(Pointage)
class PointageAdmin(admin.ModelAdmin):
    list_display = ("id", "personnel", "type_pointage", "datetime_pointage", "notes", "synced_with_odoo")
    list_filter = ("type_pointage", "datetime_pointage", "synced_with_odoo")
    search_fields = ("personnel__nom", "personnel__prenom", "personnel__matricule")
    date_hierarchy = "datetime_pointage"
    list_per_page = 50

    def get_personnel_info(self, obj):
        return f"{obj.personnel.nom} {obj.personnel.prenom} ({obj.personnel.matricule})"
    get_personnel_info.short_description = "Personnel"