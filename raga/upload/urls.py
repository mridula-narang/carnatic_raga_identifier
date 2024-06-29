# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage, name='upload'),
    path('upload/', views.upload_file, name='upload'),
    # Add other URLs as needed
]
