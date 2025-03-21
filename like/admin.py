# like/admin.py
from django.contrib import admin
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['member', 'liked_at']  # 좋아요를 누른 사용자, 콘텐츠, 좋아요 시간
    ordering = ['-liked_at']  # 최신 순으로 정렬