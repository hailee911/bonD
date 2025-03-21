from django.urls import path
from . import views

app_name="calendar1"
urlpatterns = [
    path('son/', views.son, name='son'),
    path('cal/', views.cal, name='cal'),
    path('delete_event/', views.delete_event, name='delete_event'),
    path('update_event/', views.update_event, name='update_event'),  # 수정 URL 추가
]
