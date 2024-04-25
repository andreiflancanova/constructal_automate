from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from csg.views.plate_views import PlateViewSet

PLATES_BASE_ROUTE = 'plates' 
router = routers.DefaultRouter()

router.register(rf'{PLATES_BASE_ROUTE}', PlateViewSet, basename=PLATES_BASE_ROUTE)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
