from django.contrib import admin
from emotion.models import EmotionScore

@admin.register(EmotionScore)
class EmotionScoreAdmin(admin.ModelAdmin):
  list_display = ['member','emotionscore']