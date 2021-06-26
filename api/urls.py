from django.urls import path, include
from rest_framework import routers
from apps.core.views import *

router = routers.SimpleRouter()

router.register('core/users', UserViewSet),
router.register('core/paises', PaisViewSet),
router.register('core/provincias', ProvinciaViewSet),
router.register('core/localidades', LocalidadViewSet),
router.register('core/roles', RolViewSet),

urlpatterns = [
    path('', include(router.urls)),
]
