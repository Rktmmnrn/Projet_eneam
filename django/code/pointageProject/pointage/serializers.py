from rest_framework import serializers
from .models import Pointage
from personnel.serializers import PersonnelSerializer

class PointageSerializer(serializers.ModelSerializer):
    personnel_info = serializers.SerializerMethodField()
    
    def get_personnel_info(self, obj):
        return f"{obj.personnel.nom} {obj.personnel.prenom} ({obj.personnel.matricule})"
    
    class Meta:
        model = Pointage
        fields = [
            'id', 'personnel', 'personnel_info', 'type_pointage', 
            'datetime_pointage', 'notes', 'appareil_id', 'synced_with_odoo'
        ]
        read_only_fields = ['datetime_pointage', 'synced_with_odoo']