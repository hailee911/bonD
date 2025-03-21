from django.contrib import admin
from comment.models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'member', 'text', 'created_at', 'updated_at','group_num']