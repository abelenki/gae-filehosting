# -*- encoding: utf-8 -*-

import webapp2

from aux import auth, split_url, db_uri
from models import Directory, File


class FileHandler(webapp2.RequestHandler):
  """
  Класс-обработчик действий с файлами
  """

  @auth
  def get(self):
    """
    Получение содержимого файла в бинарном виде
    """
    if not self.file_exists():
      self.error(404, 'No such file')
    else:
      self.response.headers['Content-Type'] = 'application/octet-stream'
      self.response.out.write(self.get_request_file().contents)

  @auth
  def post(self):
    """
    Создание нового файла в существующей директории
    """
    if self.file_exists():
      self.error(400, 'File already exists')
    else:
      if self.dir_exists():
        path, name = split_url(self.file_url())
        File(
          path=path,
          name = name,
          contents=self.request.body,
        ).put()
      else:
        self.error(404, 'Parent directory doesn\'t exist')

  @auth
  def put(self):
    """
    Изменение содержимого существующего файла
    """
    if not self.file_exists():
      self.error(404, 'No such file')
    else:
      f = self.get_request_file()
      f.contents = self.request.body
      f.put()

  @auth
  def delete(self):
    """
    Удаление существующего файла
    """
    if not self.file_exists():
      self.error(404, 'No such file')
    else:
      self.get_request_file().delete()


  def file_exists(self):
    """
    Провекта существования файла, с которым производится
    """
    path, name = split_url(self.file_url())
    result = File.gql('WHERE path = :path AND name = :name', path=path, name=name)
    return result.count() != 0

  def dir_exists(self):
    """
    Проверка существования рабочей директории
    """
    path, name = split_url(self.file_url())

    parts = path.split('/')
    dirname = parts.pop()
    dirpath = '/'.join(parts)

    dir = Directory.gql('WHERE path = :path AND name = :name', path=dirpath, name=dirname)
    return dir.count() != 0

  def get_request_file(self):
    """
    Получение файла, с которым производится работа
    """
    path, name = split_url(self.file_url())
    result = File.gql('WHERE path = :path AND name = :name', path=path, name=name)
    return result.fetch(1)[0]

  def file_url(self):
    """
    Получение внутреннего пути к файлу
    """
    return db_uri(self.request.path[len('/file/'):], self.auth['user'])

  def error(self, code, message=""):
    """
    Установка кода и вывод текста ошибки
    """
    webapp2.RequestHandler.error(self, code)
    self.response.out.write('Error: ' + message + '\n')