from django.contrib import admin
from admin1.models import Administrator

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
  list_display = ['ano','id','name','nickname','role']
  