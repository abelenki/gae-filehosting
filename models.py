# -*- encoding: utf-8 -*-

from google.appengine.ext import db


class Directory(db.Model):
  """
  Модель директории. Свойства:
    - path: путь к директории,
    - name: название директории
  """
  path = db.StringProperty()
  name = db.StringProperty()

class File(db.Model):
  """
  Модель файла. Свойства:
    - path: путь к файлу,
    - name: имя файла,
    - contents: двоичное содержимое файла
  """
  path = db.StringProperty()
  name = db.StringProperty()
  contents = db.BlobProperty()