# -*- encoding: utf-8 -*-

import webapp2


class MainPage(webapp2.RequestHandler):

  def get(self):
    self.redirect('/catalog/')