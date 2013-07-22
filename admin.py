from django.contrib import admin
from projects.models import *

from django.forms import CheckboxSelectMultiple

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'year')
	list_filter = ['year']
	
	#Set the tags field to be checkboxes
	formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

#Register all of the models to be editable from the admin console
admin.site.register(Category)
admin.site.register(Project, ProjectAdmin)
admin.site.register(List)
admin.site.register(Page)