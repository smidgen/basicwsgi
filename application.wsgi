#!/usr/bin/python3

import os, sys, traceback, importlib, string
import pprint

sys.path.append('/nolan4/srv/python/fileshare')

os.environ['PYTHON_EGG_CACHE'] = '/nolan4/srv/python/fileshare/.python-egg'

IS_DEV_SERVER = True

modules_allowed = {
    'cgi': IS_DEV_SERVER,
    'coffee': True,
}

def application(environ, start_response):
    try:
        status = '200 OK'
        content_type = 'text/html; charset=utf-8'
        template = 'main.html'
        data = {
            'title': '',
            'add_to_head': '',
            'body': '',
            'add_to_foot': '',
        }

        path = environ['PATH_INFO'].split('/')
        if path[1] in modules_allowed and modules_allowed[path[1]]:
            modname = 'modules.' + path[1] + '.' + path[1]
            if modname not in sys.modules:
                module = importlib.import_module(modname)
            else:
                module = sys.modules[modname]
            ret = module.run(environ, path[3:])
            status = ret.get('status', status)
            content_type = ret.get('content_type', content_type)
            template = ret.get('template', template)
            data.update(ret['data'])

        else:
            status = '404 Not Found'
            data['title'] = 'Module Not Found'
            data['body'] = "Error: Cannot find module '" + path[1] + "'"

        fo = open(os.path.dirname(__file__) + '/templates/' + template, 'r')
        t = string.Template(fo.read())
        output = t.substitute(data)

    except Exception as e:
        status = '500 Internal Server Error'
        content_type = 'text/plain; charset=utf-8'
        output = ''
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        for line in traceback.format_exception(exc_type, exc_obj, exc_traceback):
            output += line + '\n'
    finally:
        response_headers = [('Content-type', content_type),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [bytes(output, 'utf8')]
