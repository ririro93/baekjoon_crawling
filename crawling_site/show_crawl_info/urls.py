from django.urls import path

from .views import (
    crawl_home
)

urlpatterns = [
    path('', crawl_home),
]