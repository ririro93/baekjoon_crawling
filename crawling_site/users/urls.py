from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('mainPage', views.mainPage_view, name='mainPage'),
    path('signup', views.signup_view, name='signup')
]