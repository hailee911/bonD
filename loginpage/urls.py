from django.urls import path,include
from . import views

app_name = "loginpage"
urlpatterns = [
    path('login/', views.login,name="login"),
    path('id/', views.id,name="id"),
    path('id2/<str:user_id>/', views.id2,name="id2"),
    path('pw/', views.pw,name="pw"),
    path('pw2/<str:user_id>', views.pw2,name="pw2"),
    path('pw3/<str:user_id>', views.pw3,name="pw3"),
    path('join01/', views.join01,name="join01"),
    path('join01_1/', views.join01_1,name="join01_1"),
    path('join01_2/', views.join01_2,name="join01_2"),
    path('join01_3/', views.join01_3,name="join01_3"),
    path('join01_4/', views.join01_4,name="join01_4"),
    path('join02/', views.join02,name="join02"),
    path('join03/<str:id>/<str:pw>/<str:mail>/', views.join03,name="join03"),
    path('join04/', views.join04,name="join04"),
]
