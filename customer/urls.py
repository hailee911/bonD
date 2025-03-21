from django.urls import path,include
from . import views

app_name = "customer"
urlpatterns = [
    path('', views.main, name="main"),
    path('noticeview/<str:bno>/', views.noticeview, name="noticeview"),
    path('noticelist/', views.noticelist, name="noticelist"),
]
