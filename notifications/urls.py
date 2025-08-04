# notifications/urls.py
from django.urls import path
from .views import SendNotificationView

urlpatterns = [
    path("notifications/send/", SendNotificationView.as_view()),
]
