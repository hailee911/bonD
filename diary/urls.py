from django.urls import path,include
from . import views
from comment import views as comment_views  # comment 앱의 views 가져오기


app_name = "diary"
urlpatterns = [
    path('diaryHome/', views.diaryHome, name="diaryHome"),
    path('MdiaryList/', views.MdiaryList, name="MdiaryList"),
    path('diaryWrite/', views.diaryWrite, name="diaryWrite"),
    path('diaryMake/', views.diaryMake, name="diaryMake"),
    path('diary_view/<int:cno>/', views.diary_view, name="diary_view"),
    path('Cdiary_view/<int:cno>/', views.Cdiary_view, name="Cdiary_view"),
    path('Jdiary_view/<int:cno>/', views.Jdiary_view, name="Jdiary_view"),
    path('dmodify/<int:cno>/', views.dmodify, name='dmodify'),  # 글 수정
    path('ddelete/<int:cno>/', views.ddelete, name='ddelete'),  # 글 삭제
    path('delete_all/', views.delete_all_posts, name='delete_all_posts'),  # M다이어리 삭제
    path('titleChg/', views.titleChg, name='titleChg'),  # M다이어리 제목 변경
    path('Cdelete_all/', views.Cdelete_all_posts, name='Cdelete_all_posts'),  # C다이어리 삭제
    path('CtitleChg/', views.CtitleChg, name='CtitleChg'),  # C다이어리 제목 변경
    path('CdiaryList/', views.CdiaryList, name="CdiaryList"), # 생성한 다이어리 리스트
    path('JdiaryList/', views.JdiaryList, name="JdiaryList"), # 생성한 다이어리 리스트
    path('add_comment/<int:cno>/', comment_views.add_comment, name="add_comment"),  # 댓글 추가
    path('like/', include('like.urls')),  # like 앱의 URL 포함
]
