from django.core.management.base import BaseCommand, CommandError

import urllib2
from optparse import make_option
import json

class Command(BaseCommand):
  option_list = BaseCommand.option_list + (
    make_option('-p', '--pages', action='store_true', default=False, help="Import pages."),
    make_option('-r', '--projects', action='store_true', default=False, help="Import projects."),
    make_option('-c', '--categories', action='store_true', default=False, help="Import categories."),
    make_option('-l', '--lists', action='store_true', default=False, help="Import lists."),

    make_option('-u', '--url', help="Import data from a remote url."),
    make_option('-f', '--folder', help="Import data from a files in a local folder.")
  )

  def handle(self, *args, **options):
    if not options['folder'] and not options['url']:
      self.stdout.write("Need to specify either a file or URL.\n");
      return

    def get_resource(name):
      json_string = ""
      if options['folder']:
        return json.loads( open( options['folder'] + name + ".json" ).read() )
      if options['url']:
        return json.loads( urllib2.urlopen(options['url'] + name).read() )


    if options['pages']:
      for page in get_resource("pages"):
        model = Page()
        model.name = page['name']
        model.title = page['title']
        model.html = page['html']

        model.save()
      self.stdout.write("Imported pages.\n");

    if options["categories"]:
      for category in get_resource("categories"):
        model = Category()
        model.name = category['name']
        model.title = category['title']
        model.description = category['description']

        model.save()

      self.stdout.write("Imported categories.\n");

    if options["projects"]:
      for project in get_resource("projects"):
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

      self.stdout.write("Imported projects.\n");

    if options["lists"]:
      for list in get_resource("lists"):
        model = List()

        model.name = list['name']

        model.save()

        for project in list['projects']:
          query = Project.objects.filter(name = project)

          if len(query) > 0:
            model.projects.add( query[0] )

        model.save()

      self.stdout.write("Imported lists.\n");
