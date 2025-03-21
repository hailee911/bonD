from django.urls import path
from . import views

app_name="family1"
urlpatterns = [
    path('fam/', views.fam, name='fam'),
    path('delete_member/<str:member_id>/', views.delete_member, name='delete_member'),
    path('add_member/', views.add_member, name='add_member'),  # 멤버 추가 URL
]
