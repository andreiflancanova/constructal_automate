from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from csg.views.plate_views import PlateViewSet
from csg.views.stiffened_plate_views import StiffenedPlateViewSet
from cbeb.views.stiffened_plate_analysis_views import StiffenedPlateAnalysisViewSet
from cbeb.views.biaxial_elastic_buckling_views import BiaxialElasticBucklingViewSet


PLATES_BASE_ROUTE = 'plates'
STIFFENED_PLATES_BASE_ROUTE = 'stiffened-plates'
STIFFENED_PLATE_ANALYSIS_BASE_ROUTE = 'stiffened-plate-analysis'
BIAXIAL_ELASTIC_BUCKLING_BASE_ROUTE = 'biaxial-elastic-buckling'

router = routers.DefaultRouter()

router.register(rf'{PLATES_BASE_ROUTE}', PlateViewSet, basename=PLATES_BASE_ROUTE)
router.register(rf'{STIFFENED_PLATES_BASE_ROUTE}', StiffenedPlateViewSet, basename=STIFFENED_PLATES_BASE_ROUTE)
router.register(rf'{STIFFENED_PLATE_ANALYSIS_BASE_ROUTE}', StiffenedPlateAnalysisViewSet, basename=STIFFENED_PLATE_ANALYSIS_BASE_ROUTE)
router.register(rf'{BIAXIAL_ELASTIC_BUCKLING_BASE_ROUTE}', BiaxialElasticBucklingViewSet, basename=BIAXIAL_ELASTIC_BUCKLING_BASE_ROUTE)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
