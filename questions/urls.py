# questions/urls.py
from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path(
        'htmx/load-questions/',
        views.htmx_load_questions,
        name='htmx_load_questions'
    ),
    path(
        '',
        views.question_page_view,
        name='question_page'
    ),
    path(
        'htmx/search-tutorial-titles/',
        views.htmx_search_tutorial_titles,
        name='htmx_search_tutorial_titles'
    ),
    path(
        'htmx/search-tag-names/',
        views.htmx_search_tag_names,
        name='htmx_search_tag_names'
    ),

]
