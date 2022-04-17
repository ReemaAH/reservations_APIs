
from django.conf.urls import url
from django.urls import include, path

from .views import UserAPIView

urlpatterns = [
    path('registration', UserAPIView.as_view()),

]
