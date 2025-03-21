from django.urls import path,include
from . import views

app_name = "admin1"
urlpatterns = [
	# 관리자1 로그인
    path('login/', views.admin_login, name="admin_login"),
	# 어드민 로그아웃
    path('logout/', views.admin_logout, name="admin_logout"),
	# 유저리스트
    path('admin_memList/', views.admin_memList, name="admin_memList"),
	# 관리자리스트
    path('admin_adminList/', views.admin_adminList, name="admin_adminList"),
	# 관리자추가
    path('admin_adminAdd/', views.admin_adminAdd, name="admin_adminAdd"),
	# 관리자상세정보페이지
    path('admin_adminView/<str:id>/', views.admin_adminView, name="admin_adminView"),
	# 관리자정보수정페이지
    path('admin_adminUpdate/<str:id>/', views.admin_adminUpdate, name="admin_adminUpdate"),
	# 관리자삭제
    path('admin_adminDelete/<str:id>/', views.admin_adminDelete, name="admin_adminDelete"),
	# 관리자삭제(여러명 동시 삭제)
    path('admin_adminsDelete/', views.admin_adminsDelete, name="admin_adminsDelete"),


	# 공지사항리스트
    path('admin_noticeList/', views.admin_noticeList, name="admin_noticeList"),
    # 공지사항 상태 변경
    path('admin_noticeList/status_chg/', views.admin_noticeList2, name="admin_noticeList2"),
	# 공지사항쓰기
    path('admin_notiWrite/', views.admin_notiWrite, name="admin_notiWrite"),
	# 공지사항 보기
    path('admin_notiView/<int:bno>/', views.admin_notiView, name="admin_notiView"),
	# 공지사항 삭제
    path('admin_notiDelete/<int:bno>/', views.admin_notiDelete, name="admin_notiDelete"),
	# 공지사항 삭제(여러개 동시 삭제)
    path('admin_notisDelete/', views.admin_notisDelete, name="admin_notiDelete"),


	# 포스트리스트
    path('admin_postList/', views.admin_postList, name="admin_postList"),
    # 공지사항 상태 변경
    path('admin_postList/status_chg/', views.admin_postList2, name="admin_postList2"),
	# 포스트쓰기
    path('admin_postWrite/', views.admin_postWrite, name="admin_postWrite"),
	# 포스트 보기
    path('admin_postView/<int:bno>/', views.admin_postView, name="admin_notiView"),
	# 포스트 삭제
    path('admin_postDelete/<int:bno>/', views.admin_postDelete, name="admin_notiDelete"),
	# 포스트 삭제(여러개 동시 삭제)
    # path('admin_postsDelete/', views.admin_postsDelete, name="admin_notiDelete"),

    # 1:1 문의리스트
    path('admin_qList/', views.admin_qList, name="admin_qList"),
    path('admin_qList/<int:bno>/', views.admin_qListView, name="admin_qListView"),
    path('admin_qList/<int:bno>/chgText/', views.admin_qListchg, name="admin_qListchg"),
    path('admin_qList/chgText/', views.admin_qListchg2, name="admin_qListchg2"),
    path('admin_qList/chgText2/', views.admin_qListchg3, name="admin_qListchg3"),

	# 유저상세정보페이지
    path('admin_memView/<str:id>/', views.admin_memView, name="admin_memView"),
	# 유저정보수정페이지
    path('admin_memUpdate/<str:id>/', views.admin_memUpdate, name="admin_memUpdate"),
	# 유저삭제
    path('admin_memDelete/<str:id>/', views.admin_memDelete, name="admin_memDelete"),
	# 유저삭제(여러명 동시 삭제)
    path('admin_memsDelete/', views.admin_memsDelete, name="admin_memsDelete"),
	# 유저추가페이지
    path('admin_memAdd/', views.admin_memAdd, name="admin_memAdd"),


]
