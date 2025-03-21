from django.contrib import admin
from calendar1.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'title', 'location', 'repeat']
    search_fields = ['no', 'name', 'title']  # 검색 필드 추가