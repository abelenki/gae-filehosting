# -*- encoding: utf-8 -*-

import webapp2

from models import Directory, File
from aux import auth, db_uri, split_url

import jinja2
import os


jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


class CatalogPage(webapp2.RequestHandler):

  @auth
  def get(self):
    if self.file_exists():
      self.redirect(self.file_download_link())
      return

    if self.dir_exists():
      template = jinja.get_template('catalog.html')
      params = {
        'path': '/' + self.get_display_path(),
        'parent': self.get_parent_path(),
        'subdirs': self.get_subdirs(),
        'files': self.get_files(),
      }
      self.response.out.write(template.render(params))
    else:
      self.error(404, 'No such directory')


  def file_exists(self):
    path, name = split_url(self.get_current_path())
    result = File.gql('WHERE path = :path AND name = :name', path=path, name=name)
    return result.count() > 0

  def file_download_link(self):
    parts = self.get_current_path().split('/')
    path = '/'.join(parts[1:])
    return '/file/' + path

  def get_current_path(self):
    parts = self.request.path.split('/')
    path = '/'.join(parts[2:])
    return db_uri(path, self.auth['user'])

  def get_display_path(self):
    parts = self.get_current_path().split('/')
    return '/'.join(parts[1:]) + ('/' if len(parts) > 1 else '')

  def get_parent_path(self):
    path = self.get_current_path()
    if '/' not in path:
      return None
    else:
      parts = path.split('/')
      return '/catalog/' + '/'.join(parts[1:-1])

  def get_subdirs(self):
    result = Directory.gql('WHERE path = :1', self.get_current_path())
    return result.fetch(result.count())

  def get_files(self):
    result = File.gql('WHERE path = :1', self.get_current_path())
    return result.fetch(result.count())

  def dir_exists(self):
    path, name = split_url(self.get_current_path())
    result = Directory.gql('WHERE path = :path AND name = :name', path=path, name=name)
    return (path == "") or result.count() != 0

  def error(self, code, message=""):
    """
    Установка кода и вывод текста ошибки
    """
    webapp2.RequestHandler.error(self, code)
    self.response.out.write('Error: ' + message + '\n')