from django.db import models

class Page(models.Model):
	name = models.SlugField()
	title = models.CharField( max_length=300, blank=True )
	html = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.name
		
class Category(models.Model):
	name = models.SlugField()
	title = models.CharField( max_length=300 )
	description = models.CharField( max_length=300 )
	
	def __unicode__(self):
		return self.title


class Project(models.Model):
	name = models.SlugField()
	visible = models.BooleanField()
	title = models.CharField( max_length=300 )
	year = models.IntegerField()
	thumbnail = models.CharField( max_length=300, blank=True )
	
	largeimage = models.CharField( max_length=300, blank=True )
	
	description = models.CharField( max_length=300, blank=True)
	
	SINGLECOLUMN = 'SC'
	TWOCOLUMN = 'TC'
	REDIRECT = 'RD'
	MARKDOWN = 'MD'
	
	TEMPLATE_TYPES = (
    (SINGLECOLUMN, 'Single Column'),
    (TWOCOLUMN, 'Two Column'),
	(REDIRECT, 'Redirect'),
	(MARKDOWN, 'Markdown')
	)
	
	templatetype = models.CharField( max_length=2, choices=TEMPLATE_TYPES )
	
	COMPLETED = "CP"
	INPROGRESS = "IP"
	GRAVEYARD = "GY"
	ARCHIVED = "AR"
	
	STATUS_TYPES = (
    (COMPLETED, 'Completed'),
	(INPROGRESS, 'In-Progress'),
	(GRAVEYARD, 'Graveyard'),
	(ARCHIVED, 'Archived')
	)
	
	status = models.CharField( max_length=2, choices=STATUS_TYPES )
	
	data = models.TextField(blank=True)
	
	tags = models.ManyToManyField(Category)
	
	def __unicode__(self):
		return self.title
		
class List(models.Model):
	name = models.SlugField()
	projects = models.ManyToManyField(Project)
	
	def __unicode__(self):
		return self.name