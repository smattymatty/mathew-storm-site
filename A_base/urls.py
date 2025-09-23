from django.urls import path
from . import views

app_name = 'A_base'

urlpatterns = [
    path('', views.index, name='home'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]