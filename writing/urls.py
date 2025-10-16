from django.urls import path
from . import views


urlpatterns = [
    # Writing dashboard (main landing page)
    path('', views.index, name='index'),

    # The Labyrinth of Sisyphus book cover
    path('labyrinth-of-sisyphus/', views.book_cover, name='book_cover'),

    # Read a specific chapter
    path('read/<slug:chapter_slug>/', views.read_chapter, name='read_chapter'),

    # HTMX endpoint for dynamic page loading
    path('api/get-page/<slug:chapter_slug>/<int:page_num>/', views.get_page_htmx, name='get_page'),

    # Short Stories
    path('red-shoes/', views.red_shoes, name='red_shoes'),
    path('minimum-viable-apocalypse/', views.minimum_viable_apocalypse, name='minimum_viable_apocalypse'),
]
