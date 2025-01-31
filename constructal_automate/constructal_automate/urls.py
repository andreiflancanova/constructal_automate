from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from csg.views.plate_views import PlateViewSet
from csg.views.stiffened_plate_views import StiffenedPlateViewSet
from cbeb.views.stiffened_plate_analysis_views import StiffenedPlateAnalysisViewSet
from cbeb.views.elastic_buckling_views import ElasticBucklingViewSet
from cbeb.views.elasto_plastic_buckling_views import ElastoPlasticBucklingViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

PLATES_BASE_ROUTE = 'plates'
STIFFENED_PLATES_BASE_ROUTE = 'stiffened-plates'
STIFFENED_PLATE_ANALYSIS_BASE_ROUTE = 'stiffened-plate-analysis'
ELASTIC_BUCKLING_BASE_ROUTE = 'elastic-buckling'
ELASTO_PLASTIC_BUCKLING_BASE_ROUTE = 'elasto-plastic-buckling'

schema_view = get_schema_view(
    openapi.Info(
        title="Constructal Automate",
        default_version='v1',
        description="API REST para automação de fluxos de modelagem computacional utilizando a biblioteca PyMAPDL para integração com o software Ansys Mechanical APDL",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="andreiflancanova@hotmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



router = routers.DefaultRouter()

router.register(rf'{PLATES_BASE_ROUTE}', PlateViewSet, basename=PLATES_BASE_ROUTE)
router.register(rf'{STIFFENED_PLATES_BASE_ROUTE}', StiffenedPlateViewSet, basename=STIFFENED_PLATES_BASE_ROUTE)
router.register(rf'{STIFFENED_PLATE_ANALYSIS_BASE_ROUTE}', StiffenedPlateAnalysisViewSet, basename=STIFFENED_PLATE_ANALYSIS_BASE_ROUTE)
router.register(rf'{ELASTIC_BUCKLING_BASE_ROUTE}', ElasticBucklingViewSet, basename=ELASTIC_BUCKLING_BASE_ROUTE)
router.register(rf'{ELASTO_PLASTIC_BUCKLING_BASE_ROUTE}', ElastoPlasticBucklingViewSet, basename=ELASTO_PLASTIC_BUCKLING_BASE_ROUTE)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI (alternativa ao Swagger UI)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # OpenAPI em JSON ou YAML
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json')
]
