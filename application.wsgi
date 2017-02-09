#!/usr/bin/python3

import os, sys, traceback, importlib, string

sys.path.append('/nolan4/srv/python/fileshare')

from config import *

os.environ['PYTHON_EGG_CACHE'] = '/nolan4/srv/python/fileshare/.python-egg'

def application(environ, start_response):
    try:
        status = '200 OK'
        content_type = 'text/html; charset=utf-8'
        template = 'main.html'
        data = {
            'title': '',
            'base_href': 'http://localhost/fileshare/',
            'add_to_head': '',
            'body': '',
            'add_to_foot': '',
        }

        if len(environ['PATH_INFO']) == 0:
            module_selected = index_module
            path = []
        else:
            path = environ['PATH_INFO'].split('/')
            if path[1] == '':
                module_selected = index_module
            else:
                module_selected = path[1]

        if module_selected not in modules_allowed or modules_allowed[module_selected] == False:
            status = '404 Not Found'
            data['title'] = 'Module Not Found'
            data['body'] = "Error: Cannot find module '" + module_selected + "'"
        else:
            modname = 'modules.' + module_selected + '.' + module_selected
            if modname not in sys.modules:
                module = importlib.import_module(modname)
            else:
                module = sys.modules[modname]
            ret = module.run(environ=environ, urlvars=path[3:])
            status = ret.get('status', status)
            content_type = ret.get('content_type', content_type)
            template = ret.get('template', template)
            data.update(ret['data'])

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
