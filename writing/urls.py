from django.urls import path
from . import views


urlpatterns = [
    # Book cover / landing page
    path('', views.index, name='index'),

    # Read a specific chapter
    path('read/<slug:chapter_slug>/', views.read_chapter, name='read_chapter'),

    # HTMX endpoint for dynamic page loading
    path('api/get-page/<slug:chapter_slug>/<int:page_num>/', views.get_page_htmx, name='get_page'),
]
