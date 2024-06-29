from django.urls import path
from .views import IndexView

urlpatterns = [
    path('uploaded/',IndexView.as_view() , name='index'),
]
