from django.urls import path
from .views import AnswerQuestion, AudioUploadView, DalotModel, DalotModelNew
from django.conf import settings
from django.conf.urls.static import static

# AnswerQuestion
urlpatterns = [
    path("dalotgpt/", DalotModel.as_view(), name="dalot-model"),
    path("dalotgptnew/", DalotModelNew.as_view(), name="dalot-model-new"),
    path("ask/", AnswerQuestion.as_view(), name="ask-question"),
    path("upload_audio/", AudioUploadView.as_view(), name="upload_audio"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
