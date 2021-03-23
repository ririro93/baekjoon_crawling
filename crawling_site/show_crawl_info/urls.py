from django.urls import path, include
from rest_framework import routers

from .views import (
    crawl_home,
    refresh_button,
    refresh_member,
    add_question,
    MemberViewSet,
    SolveViewSet,
)

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'solves', SolveViewSet)

urlpatterns = [
    path('', crawl_home, name='crawl-home'),
    path('refresh/', refresh_button),
    path('refresh/<str:member_id>', refresh_member),
    path('add-question/', add_question),
    path('router/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]