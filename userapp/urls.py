from rest_framework.routers import DefaultRouter
from .views import VacinaViewSet

router = DefaultRouter()
router.register(r'vacinas', VacinaViewSet)
     
urlpatterns = router.urls