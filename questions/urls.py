# questions/urls.py
from django.urls import path
from . import views

app_name = "questions"

urlpatterns = [
    path("", views.questions_page_view, name="questions_page"),
    path("quiz/", views.quiz_view, name="quiz"),
    path(
        "htmx/load-questions/",
        views.htmx_load_questions,
        name="htmx_load_questions",
    ),
    path(
        "htmx/search-tutorial-titles/",
        views.htmx_search_tutorial_titles,
        name="htmx_search_tutorial_titles",
    ),
    path(
        "htmx/search-tag-names/",
        views.htmx_search_tag_names,
        name="htmx_search_tag_names",
    ),
    path(
        "htmx/check-answer/<int:question_pk>/",
        views.htmx_check_answer,
        name="htmx_check_answer",
    ),
    path(
        "htmx/load-single-question/<int:question_pk>/",
        views.htmx_load_single_question,
        name="htmx_load_single_question",
    ),
    path(
        "htmx/skip-question/<int:question_pk>/",
        views.htmx_skip_question,
        name="htmx_skip_question",
    ),
]
