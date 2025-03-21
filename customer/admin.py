from django.contrib import admin
from customer.models import NoticeBoard

@admin.register(NoticeBoard)
class BoardAdmin(admin.ModelAdmin):
  list_display = ['bno','btitle','bdate']