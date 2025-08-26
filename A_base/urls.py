from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]