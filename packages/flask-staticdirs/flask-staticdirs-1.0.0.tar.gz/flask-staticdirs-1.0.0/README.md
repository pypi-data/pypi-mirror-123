flask-staticdirs
----------------

The built-in Flask functionality for serving static files from a directory does not serve index
files. _flask-staticdirs_ implements a Flask blueprint that does.

#### Features:

- Redirects paths matching exsting directories so they end with '/'
- Serves the first index file found in the path under a static folder
- Serves paths matching exsiting files in a static folder
- Allows conflicting routes to be superseded with an existing file or directory.

## Usage

Instead of using Flask's **static\_folder**, and **static\_url\_path** parameters, like this:

    from flask import Flask

    app = Flask(__name__, static_folder="public", static_url_path="/")
    if __name__ == '__main__':
        app.run(host="localhost", port=3000, debug=True)

Use the blueprint returned from **flask\_staticdirs.staticdirs()**:

    from flask import Flask
    from flask_staticdirs import staticdirs

    app = Flask(__name__)
    app.register_blueprint(staticdirs("public"), url_prefix="/")
    if __name__ == '__main__':
        app.run(host="localhost", port=3000, debug=True)

***Note***: `url_prefix="/"` is unnecessary since `"/"` is the default value, but the example matches `static_url_path` for clarity.

## Superseding conflicting routes

Flask matches routes to incoming paths based on an algorithm that sorts routes. Because _flask\_staticdirs_ route is '/<path:path', just about any route will take precedence.

This is not normally a problem unless you want to mix programatic responses with the
paths that serve static files.

For example, if you would like to serve static files before files found in a database

    app.register_blueprint(staticdirs("public", files=[ "docs/*" ]))
    @app.route("/docs/<doc>")
    def mysubdir_route(doc):
        return doc_from_db(doc) or f'<p>Could not find {doc}.</p>'
        
I realize this is not _really_ a common use case 😊, but it does illustrate the feature.

## Serving other index files

If you want to serve indexes for directories with files other than 'index.html' you can list them in the **index** parameter:

    app.register_blueprint(staticdirs("public", index=[ "index.html", "index.htm" ]))


## API

### staticdirs(static_folder='static', index='index.html', files=[])

Creates a Flask blueprint to serve files and directories (with support for index files) from at static folder.

- **param static_folder**: The folder to serve files from. Defaults to 'static'.
- **param index**: File or list of files (first found) to serve for a directory. Defaults to 'index.html'.
- **param files**: An array of filename globs. Files and directories that match will be routed specifically to avoid conflict with other routes.
- **returns**: A flask blueprint. Use with ``app.register_blueprint()``
