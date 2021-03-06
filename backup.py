from django.shortcuts import render
from projects.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.cache import cache_page
import rss, globals, re
import django.template
import json

import urllib2

#Import order must be Categories, Projects, then Lists. Pages are independant
def export(request, element):
	result = []

	if element == "pages":
		for page in Page.objects.all():
			value = {}

			for key in ['name', 'title', 'html']:
				value[key] = getattr(page, key)

			result.append(value)

	if element == "categories":
		for cat in Category.objects.all():
			value = {}

			for key in ['name', 'title', 'description']:
				value[key] = getattr(cat, key)

			result.append(value)

	if element == "projects":
		for project in Project.objects.all():
			value = {}

			for key in ['name', 'visible', 'title', 'year', 'thumbnail', 'largeimage', 'description', 'templatetype', 'status', 'data']:
				value[key] = getattr(project, key)

			value['tags'] = []
			for tag in project.tags.all():
				value['tags'].append( tag.name )

			result.append(value)

	if element == "lists":
		for list in List.objects.all():
			value = {}
			value['name'] = list.name

			value['projects'] = []
			for project in list.projects.all():
				value['projects'].append( project.name )

			result.append(value)

	return HttpResponse( json.dumps(result, indent=True), content_type='application/json; charset=utf-8' )

#Import order must be Categories, Projects, then Lists. Pages are independant
def importload(request, element):
	if request.user.is_authenticated() and request.user.is_superuser:
		result = []

		dom = None

		if "url" in request.REQUEST:
			url = request.REQUEST.get("url")
			print "Url import from ", url

			urlrequest = urllib2.Request( url )
			dom = json.loads( urllib2.urlopen(urlrequest).read() )

		elif "file" in request.REQUEST:
			file = request.REQUEST.get("file")

			print "File import from ", file
			dom = json.loads( open(file).read() )


		if element == "pages":
			for page in dom:
				model = Page()
				model.name = page['name']
				model.title = page['title']
				model.html = page['html']

				model.save()

		if element == "categories":
			for category in dom:
				model = Category()
				model.name = category['name']
				model.title = category['title']
				model.description = category['description']

				model.save()

		if element == "projects":
			for project in dom:
				model = Project()
				model.name = project['name']
				model.visible = project['visible']
				model.title = project['title']
				model.year = project['year']

				model.thumbnail = project['thumbnail']
				model.largeimage = project['largeimage']
				model.description = project['description']

				model.templatetype = project['templatetype']
				model.status = project['status']

				model.data = project['data']

				model.save()

				for tag in project['tags']:
					query = Category.objects.filter(name = tag)
					if len(query) > 0:
						model.tags.add( query[0] )

				model.save()

		if element == "lists":
			for list in dom:
				model = List()

				model.name = list['name']

				model.save()

				for project in list['projects']:
					query = Project.objects.filter(name = project)

					if len(query) > 0:
						model.projects.add( query[0] )

				model.save()


		return HttpResponse( "Successfully imported." )
	else:
		return HttpResponse("You do not have permissions to access this page.")
