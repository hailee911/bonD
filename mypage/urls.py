from django.urls import path,include
from . import views

app_name = "mypage"
urlpatterns = [
    path('main/', views.main, name="main"),
    path('delaccount/', views.delaccount, name="delaccount"),  # 회원탈퇴
    path('modify/', views.modify, name="modify"),
    path('modify/currpw_chk/', views.currpw_chk, name="currpw_chk"),
    path('modify/pw_chg/', views.pw_chg, name="pw_chg"),
    path('profile_upload', views.profile_upload, name="profile_upload"),
]
