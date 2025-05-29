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
]