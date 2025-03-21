from django.urls import path,include
from . import views

app_name = "emotion"
urlpatterns = [
    path('main/', views.main, name="main"),
    path('main_data1/', views.main_data1, name="main_data1"),
    path('main_data2/', views.main_data2, name="main_data2"),
    path('main_data3/', views.main_data3, name="main_data3"),
    path('main_data4/', views.main_data4, name="main_data4"),
    path('main_data5/', views.main_data5, name="main_data5"),
    path('report/', views.report, name="report"),
    path("run-ai/", views.run_ai_process, name="run_ai_process"),
    path('save_diaries_to_txt/', views.save_diaries_to_txt, name='save_diaries_to_txt'),
]
