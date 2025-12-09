from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Personnel
from .serializers import PersonnelSerializer

@api_view(['GET','POST'])
def personnel_list(request):
    """
    GET /api/personnel/  → liste complète
    """
    if request.method == 'GET':
        qs = Personnel.objects.all()
        serializer = PersonnelSerializer(qs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)