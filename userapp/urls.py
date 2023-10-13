from rest_framework import routers
from .views import ProfissionalViewSet, VacinaViewSet

router = routers.DefaultRouter()
router.register(r'profissional', ProfissionalViewSet)
router.register(r'vacina', VacinaViewSet) 
     
urlpatterns = router.urls