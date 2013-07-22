from django.contrib import admin
from projects.models import *

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'year')
	list_filter = ['year']
	
admin.site.register(Category)
admin.site.register(Project, ProjectAdmin)
admin.site.register(List)
admin.site.register(Page)