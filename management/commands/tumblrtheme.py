from django.core.management.base import BaseCommand, CommandError

import django.template
from django.shortcuts import render
from django.template import RequestContext, loader
from django.template import Context

from django.template.loader import render_to_string
import codecs

class Command(BaseCommand):
  args = '<output_file>'
  help = "Generate the tumblr theme for the blog."

  def handle(self, *args, **options):
    if len(args) < 1:
      self.stdout.write("One argument (the output filename) must be provided.")
      return

    result = render_to_string("tumblr.html", Context({
      "blogtab" : True,
      "root_url" : "http://www.varunramesh.net"
    }) )

    output_file = codecs.open(args[0], 'w', 'utf-8')
    output_file.write(result)
    output_file.close()
