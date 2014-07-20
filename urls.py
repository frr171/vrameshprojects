from django.conf.urls import patterns, url

from projects import views
from projects import backup

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),

	url(r'^export/(?P<element>[a-zA-Z0-9_.-]+)', backup.export, name='export'),
	url(r'^import/(?P<element>[a-zA-Z0-9_.-]+)', backup.importload, name='import'),

	url(r'^projects/$', views.projects, name='projects'),

	url(r'^projects/(?P<project_name>[a-zA-Z0-9_.-]+)', views.project, name='project'),

	url(r'^archive/$', views.archive, name='archive'),

	url(r'^categories/$', views.categories, name='categories'),
	url(r'^categories/(?P<category_name>[a-zA-Z0-9_.-]+)', views.category, name='category'),

	url(r'^(?P<page_name>[a-zA-Z0-9_.-]+)', views.page, name='page')
)
