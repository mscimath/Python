from django.urls import path
from . import views

urlpatterns = [
    path('', views.privacy_report, name='privacy_report'),
]
