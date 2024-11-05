from django.urls import path
from .views import AnswerQuestion

urlpatterns = [
    path("ask/", AnswerQuestion.as_view(), name="ask-question"),
]
