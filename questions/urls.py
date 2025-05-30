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
]
