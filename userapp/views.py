from rest_framework import viewsets
from .models import Vacina
from .serializers import VacinaSerializer

class VacinaViewSet(viewsets.ModelViewSet):
    queryset = Vacina.objects.all()
    serializer_class = VacinaSerializer