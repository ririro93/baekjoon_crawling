from django.urls import path, include
from rest_framework import routers

from .views import (
    crawl_home,
    refresh_button,
    MemberViewSet,
    SolveViewSet,
)

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'solves', SolveViewSet)

urlpatterns = [
    path('', crawl_home),
    path('refresh/', refresh_button),
    path('router/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]