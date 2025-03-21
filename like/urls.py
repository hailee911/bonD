from django.urls import path
from . import views

urlpatterns = [
    path('<int:cno>/', views.like, name='like'),
]
