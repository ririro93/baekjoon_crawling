from django.urls import path

from .views import (
    fines_home,
)

urlpatterns = [
    path('', fines_home),
]