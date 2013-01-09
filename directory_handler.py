# -*- encoding: utf-8 -*-

import webapp2

from aux import auth, db_uri
from models import Directory, File


class DirectoryHandler(webapp2.RequestHandler):
  """
  Класс-обработчик действий с директориями
  """
  
  @auth
  def get(self):
    """
    Получение содержимого директории
    """
    if self.dir_exists():
      self.response.headers['Content-Type'] = 'text/xml; charset=utf-8'
      self.response.out.write('<?xml version="1.0"?>\n')
      self.response.out.write('<directory>')

      dirs = self.get_request_dir_subdirs()
      if len(dirs) > 0:
        for d in dirs:
          self.response.out.write('<subdir>{}</subdir>'.format(d.name))

      files = self.get_request_dir_files()
      if len(files) > 0:
        for f in files:
          self.response.out.write('<file>{}</file>'.format(f.name))
      
      self.response.out.write('</directory>')

    else:
      self.error(404, 'No such directory')
  
  @auth
  def post(self):
    """
    Создание новой директории внутри существующей директории
    """
    if self.dir_exists():
      self.error(400, 'Directory already exists')
    else:
      if self.parent_exists():
        parent, name = self.split_parent_dir()
        Directory(path=parent, name=name).put()
      else:
        self.error(404, 'Parent directory doesn\'t exist')


  def dir_exists(self):
    """
    Проверка существования директории, с которой производится работа
    """
    parent, name = self.split_parent_dir()
    return (name == "") or (self.get_request_dir().count() > 0)

  def parent_exists(self):
    """
    Проверка существования родительской директории
    """
    parent, name = self.split_parent_dir()
    return ('/' not in parent) or (
        Directory.gql('WHERE path = :1', self.split_parent_dir()[0]).count() > 0)

  def get_request_dir(self):
    """
    Получение директории, с которой производится работа
    """
    parent, name = self.split_parent_dir()
    return Directory.gql('WHERE path = :1 AND name = :2', parent, name)

  def get_request_dir_files(self):
    """
    Получение файлов в директории, с которой производится работа
    """
    files = File.gql('WHERE path = :1', self.dir_url())
    return files.fetch(files.count())

  def get_request_dir_subdirs(self):
    """
    Получение поддиректорий директории, с которой производится работа
    """
    dirs = Directory.gql('WHERE path = :1', self.dir_url())
    return dirs.fetch(dirs.count())

  def dir_url(self):
    """
    Получение внутреннего пути к директории
    """
    url = self.request.path[len('/dir/'):]
    return db_uri(url, self.auth['user'])

  def split_parent_dir(self):
    """
    Отделение родительской директории от названия текущей директории
    """
    parts = self.dir_url().split('/')
    if len(parts) < 2:
      return self.dir_url(), ''
    else:
      return '/'.join(parts[:-1]), parts[-1]

  def error(self, code, message=""):
    """
    Установка кода и вывод текста ошибки
    """
    webapp2.RequestHandler.error(self, code)
    self.response.out.write('Error: ' + message + '\n')