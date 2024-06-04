from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from csg.views.plate_views import PlateViewSet
from csg.views.stiffened_plate_views import StiffenedPlateViewSet


PLATES_BASE_ROUTE = 'plates'
STIFFENED_PLATES_BASE_ROUTE = 'stiffened-plates'

router = routers.DefaultRouter()

router.register(rf'{PLATES_BASE_ROUTE}', PlateViewSet, basename=PLATES_BASE_ROUTE)
router.register(rf'{STIFFENED_PLATES_BASE_ROUTE}', StiffenedPlateViewSet, basename=STIFFENED_PLATES_BASE_ROUTE)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
