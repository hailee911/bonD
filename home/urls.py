from django.urls import path,include
from . import views

app_name = "main"
urlpatterns = [
    path('', views.landing,name="landing"),
    path('index/', views.main,name="main"),
    path('logout/', views.logout,name="logout"),
    path('search/', views.search,name="search"),
    path('get_family_members/', views.get_family_members,name="get_family_members"),
    path('get_emotion_graph/<member_id>/', views.get_emotion_graph,name="get_emotion_graph"),
    path('notification/', views.notification_list, name="notification_list"),
    path('notification_read/<int:notification_id>/', views.notification_read, name="notification_read"),
]
