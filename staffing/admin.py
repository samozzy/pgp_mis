from django.contrib import admin
from .models import *

# Register your models here.

class StaffRoleAdmin(admin.ModelAdmin):
	list_display = ['role_name', 'department', 'is_management']

class QuickLinkAdmin(admin.ModelAdmin):
	list_display = ['title', 'ordering']

admin.site.register(StaffRole, StaffRoleAdmin)
admin.site.register(Application)
admin.site.register(QuickLink, QuickLinkAdmin)