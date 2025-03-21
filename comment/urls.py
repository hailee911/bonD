from django.urls import path
from . import views

app_name = "comment"
urlpatterns = [
    path('add_comment/<int:cno>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
