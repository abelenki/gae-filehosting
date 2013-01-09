# -*- encoding: utf-8 -*-

import base64


def auth(target):
  """
  Декоратор для действий, требующих предварительной авторизации
  """

  def check_auth(user, passwd):
    """
    Вспомогательная функция для проверки пользователя
    """
    allowed_users = {
      'admin': 'admin',
      'scott': 'tiger',
    }
    return (allowed_users.get(user) == passwd)

  def wrapper(self, *args, **kargs):
    """
    Функциональная обёртка, отвечающая за авторизацию
    """
    if 'Authorization' in self.request.headers:

      auth_str = self.request.headers['Authorization'].split()[1]
      user, passwd = base64.decodestring(auth_str).split(':')
      if check_auth(user, passwd):
        self.auth = {
          'user': user,
          'passwd': passwd
        }
        target(self, *args, **kargs)

      else:
        self.response.headers['WWW-Authenticate'] = 'Basic realm="restricted section"'
        self.error(401)
        return

    else:
      self.response.headers['WWW-Authenticate'] = 'Basic realm="restricted section"'
      self.error(401)
      return

  return wrapper

def db_uri(path, user):
  """
  Транслирует URI из запроса во внутренний URI базы данных
  """
  uri = '{user}/{path}'.format(
    user=user,
    path=path
  )
  if uri.endswith('/'):
    uri = uri[:-1]
  return uri

def split_url(url):
  """
  Отделяет имя файла от пути
  """
  parts = url.split('/')
  name = parts.pop()
  return '/'.join(parts), name