from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime, parse_date
from .models import Pointage
from personnel.models import Personnel
from .serializers import PointageSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def pointage_list(request):
    """
    GET /api/pointage/?date=2024-01-15&matricule=EMP001
    POST /api/pointage/ - Créer un pointage individuel
    """
    
    # GESTION DES ERREURS pour GET
    if request.method == 'GET':
        try:
            date_str = request.query_params.get('date')
            matricule = request.query_params.get('matricule')
            
            qs = Pointage.objects.all()
            
            if date_str:
                date_obj = parse_date(date_str)
                if not date_obj:
                    return Response(
                        {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                qs = qs.filter(datetime_pointage__date=date_obj)
            
            if matricule:
                qs = qs.filter(personnel__matricule=matricule)
            
            serializer = PointageSerializer(qs, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des pointages: {str(e)}")
            return Response(
                {'error': 'Erreur serveur lors de la récupération des données'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # GESTION DES ERREURS pour POST
    elif request.method == 'POST':
        try:
            data = request.data.copy()
            
            # Validation du matricule
            matricule = data.get('personnel')
            if not matricule:
                return Response(
                    {'error': 'Le matricule est obligatoire'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                personnel = Personnel.objects.get(matricule=matricule)
            except Personnel.DoesNotExist:
                return Response(
                    {'error': f'Personnel avec matricule {matricule} non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            data['personnel'] = personnel.id
            
            serializer = PointageSerializer(data=data)
            if serializer.is_valid():
                pointage = serializer.save()
                return Response(
                    PointageSerializer(pointage).data, 
                    status=status.HTTP_201_CREATED
                )
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du pointage: {str(e)}")
            return Response(
                {'error': 'Erreur serveur lors de la création du pointage'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )