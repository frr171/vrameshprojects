from django.shortcuts import render
from projects.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.cache import cache_page
import rss, globals, re
import django.template
import json

#Set cache_length. Only really necessary if you expect large amounts of traffic.
cache_length = 60

#@cache_page( cache_length )
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
	
	return returnval

#@cache_page( cache_length )
def projects(request):
	context = {}
	context['projects'] = True
	
	context['inprogress'] = split( Project.objects.filter(status=Project.INPROGRESS).order_by('-year') )
	context['completed'] = split( Project.objects.filter(status=Project.COMPLETED).order_by('-year') )
	context['archived'] = split( Project.objects.filter(status=Project.ARCHIVED).order_by('-year') )
	
	return render(request, 'projects.html', context)

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
		context['projects'] = split( Project.objects.filter(tags__name=category_name).order_by('-year') )
		
		return render(request, 'category.html', context)
	else:
		return HttpResponse( "The category named '" + category_name + "' could not be found.")
	
#Import order must be Categories, Projects, then Lists. Pages are independant
def export(request, element):
	if request.user.is_authenticated() and request.user.is_superuser:
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
	else:
		return HttpResponse("You do not have permissions to access this page.")