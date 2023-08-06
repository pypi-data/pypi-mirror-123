"""flask-staticdirs

Import the `staticdirs` module to use:

    >>> from flask import Flask
    >>> from flask_staticdirs import staticdirs
    >>> app = Flask(__name__)
    >>> app.register_blueprint(staticdirs())
    >>> app.run()

See https://github.com/pbatey/flask-staticdirs/ for more information.
"""
import os
from glob import glob
from flask import Blueprint, redirect, request, send_from_directory, abort
from flask.helpers import safe_join

__version__ = "1.0.0"

def staticdirs(static_folder='static', index='index.html', files=[]):
  """Creates a Flask blueprint to serve files and directories (with support for index files) from at static folder.

  :param static_folder: The folder to serve files from. Defaults to 'static'.
  :param index: File or list of files (first found) to serve for a directory. Defaults to 'index.html'.
  :param files: An array of filename globs. Files and directories that match will be routed specifically to avoid conflict with other routes.
  :returns: A flask blueprint. Use with ``app.register_blueprint()``
  """
  static_folder = os.path.join(static_folder, '') # ensure it ends with '/'
  bp = Blueprint(__name__.replace('.','+'), __name__)

  def send_index(static_folder='static', index='index.html'):
    if not isinstance(index, list):
      index = [index]
    for file in index:
      if os.path.isfile(safe_join(static_folder, file)):
        return send_from_directory(static_folder, file)
    abort(404)

  @bp.route('/')
  def route_home_dir():
    """Serve index.html from /"""
    return send_index(static_folder, index)

  @bp.route('/<path:path>')
  def route_dir(path):
    """Serve index.html from subdirs"""
    if os.path.isdir(safe_join(static_folder, path)):
      if not path.endswith('/'):
        path = os.path.join(request.root_path, request.path, '')
        if request.query_string:
          path = f'{path}?{request.query_string}'
        return redirect(path, code=301)
      return send_index(safe_join(static_folder, path), index)
    return send_from_directory(static_folder, path)

  for pattern in files:
    if pattern.startswith('/'):
      pattern = pattern[1:] # ensure it doesn't start with '/'
    for file in glob(safe_join(static_folder, pattern)):
      route = file.removeprefix(static_folder)
      if os.path.isfile(file):
        bp.route(f'/{route}')(lambda: send_from_directory(static_folder, route))
      if os.path.isdir(file):
        bp.route(f'/{route}')(lambda: route_dir(route))

  return bp
