from django.shortcuts import render
from projects.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.cache import cache_page
import rss, globals, re
import django.template
import json
import markdown

#Set cache_length. Only really necessary if you expect large amounts of traffic.
cache_length = 60

@cache_page( cache_length )
def home(request):
	context = {}
	context['home'] = True

	#Load Featured Projects
	try:
		context['featured'] = List.objects.filter(name="featured")[0]
	except:
		pass

	#Get Carousel
	results = Page.objects.filter(name="carousel")
	if len(results) > 0:
		context['carousel'] = results[0].html
	else:
		context['carousel'] = loader.get_template('carousel.html').render( RequestContext(request, {} ) )

	#Get Blog Entries
	try:
		context['blog'] = rss.getEntries( )
	except:
		pass

	return render(request, 'homepage.html', context)

#@cache_page( cache_length )
def project(request, project_name):
	context = {}
	context['projects'] = True

	#Tell template if this is a superuser
	context['superuser'] = request.user.is_authenticated() and request.user.is_superuser

	results = Project.objects.filter(name=project_name)

	if len(results) > 0:
		project = results[0]
		context['project'] = project

		#Get blog entries with the same tag as the project name
		try:
			context['blog'] = rss.getEntries( label=project.name)
		except:
			pass

		#Single Column Template
		if project.templatetype == Project.SINGLECOLUMN:
			context['column1'] = project.data
			return render(request, 'singlecolumn.html', context)

		#Markdown Single Column
		if project.templatetype == Project.MARKDOWN:
			context['column1'] = markdown.markdown(project.data)
			return render(request, 'singlecolumn.html', context)

		#Two Column Template
		if project.templatetype == Project.TWOCOLUMN:

			match = re.search( "<column1>(.*)</column1>" , project.data, re.MULTILINE | re.DOTALL )
			if match:
				context['column1'] = match.group(1)

			match = re.search( "<column2>(.*)</column2>" , project.data, re.MULTILINE | re.DOTALL )
			if match:
				context['column2'] = match.group(1)

			return render(request, 'twocolumn.html', context)

		#Simple redirect to an external site
		if project.templatetype == Project.REDIRECT:
			context['url'] = project.data

			return render(request, 'redirect.html', context)
	else:
		return render(request, 'project.html', context)

#@cache_page( cache_length )
def page(request, page_name):

	results = Page.objects.filter(name=page_name)

	if len(results) > 0:
		template = django.template.Template( results[0].html )
		context = RequestContext(request, {} )

		return HttpResponse(template.render(context))
	else:
		return HttpResponse( "The page named '" + page_name + "' could not be found.")

def split(list, n = 3):
	returnval = []

	currentset = []
	for item in list:
		if len(currentset) >= n:
			returnval.append(currentset)
			currentset = []

		currentset.append(item)

	returnval.append(currentset)

	if len(list) > 0:
		return returnval
	else:
		return None

@cache_page( cache_length )
def projects(request):
	return render(request, 'projects.html', {
		'projects' : True,
		'inprogress' : split( Project.objects.filter(status=Project.INPROGRESS, visible=True).order_by('-year') ),
		'completed' : split( Project.objects.filter(status=Project.COMPLETED, visible=True).order_by('-year') ),
		'graveyard' : split( Project.objects.filter(status=Project.GRAVEYARD, visible=True).order_by('-year') )
	})

@cache_page( cache_length )
def archive(request):
	projects_by_year = {}
	years = []

	for project in Project.objects.filter(status=Project.ARCHIVED, visible=True):
		if project.year not in years:
			years.append(project.year)
			projects_by_year[project.year] = []
		projects_by_year[project.year].append(project)
	years.sort(reverse=True)


	return render(request, 'archive.html', {
		'projects' : True,
		'years' : map(lambda x: {
			"year" : x,
			"projects" : split( projects_by_year[x] )
		}, years)
	})

#@cache_page( cache_length )
def categories(request):
	context = {}
	context['projects'] = True

	context['categories'] = Category.objects.all()
	return render(request, 'categories.html', context)

#@cache_page( cache_length )
def category(request, category_name):
	results = Category.objects.filter(name=category_name)

	context = {}
	context['projects'] = True

	if len(results) > 0:
		category = results[0]
		context['category'] = category
		context['projects'] = split( Project.objects.filter(tags__name=category_name, visible=True).order_by('-year') )

		return render(request, 'category.html', context)
	else:
		return HttpResponse( "The category named '" + category_name + "' could not be found.")
