#!/usr/bin/python3

import os, sys, traceback, html

sys.path.append('/nolan4/srv/python/fileshare')

os.environ['PYTHON_EGG_CACHE'] = '/nolan4/srv/python/fileshare/.python-egg'

def application(environ, start_response):
    try:
        status = '200 OK'
        content_type = 'text/html'
        output = '''<!DOCTYPE html>
<html>
<head>
  <title></title>
  <meta charset="utf-8" />
  <style type="text/css">
    table.env_dump {
      border-collapse: collapse;
    }
    table.env_dump th, table.env_dump td {
      border: 1px solid black;
      padding: 3px;
    }
    table.env_dump th {
      text-align: left;
    }
  </style>
</head>
<body>
<h1>Hello World!</h1>
'''
        output += '<table class="env_dump">\n'
        for key, value in sorted(environ.items(), key=lambda s: str(s).lower()):
            output += ("  <tr><th>%s</th><td>%s</td></tr>\n" % (key, html.escape(str(value))))
        output += '</table>\n'
        output += '''
</body>
</html>
'''
    except Exception as e:
        status = '500 Internal Server Error'
        content_type = 'text/plain'
        output = ''
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        for line in traceback.format_exception(exc_type, exc_obj, exc_traceback):
            output += line + '\n'
    finally:
        response_headers = [('Content-type', content_type + '; charset=utf-8'),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [bytes(output, 'utf8')]
