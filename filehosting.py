# -*- encoding: utf-8 -*-

import webapp2

from directory_handler import DirectoryHandler
from file_handler import FileHandler
from main_page import MainPage
from catalog_page import CatalogPage

urlconf = (
  ('/', MainPage),
  ('/dir/.*', DirectoryHandler),
  ('/file/.*', FileHandler),
  ('/catalog/.*', CatalogPage),
)

app = webapp2.WSGIApplication(urlconf, debug=True)