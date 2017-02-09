#!/usr/bin/python3

import os, sys, traceback, importlib, string, MySQLdb

sys.path.append('/nolan4/srv/python/basicwsgi')

from config import *

os.environ['PYTHON_EGG_CACHE'] = '/nolan4/srv/python/basicwsgi/.python-egg'

template_cache = {}

def application(environ, start_response):
    try:
        status = '200 OK'
        content_type = 'text/html; charset=utf-8'
        template = 'main.html'
        data = {
            'title': '',
            'base_href': 'http://localhost/basicwsgi/',
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
            if getattr(module, 'REQUIRES_DB', False):
                db_con = MySQLdb.connect(mysql_config['host'], mysql_config['user'], mysql_config['password'], mysql_config['db'])
                ret = module.run(environ=environ, urlvars=path[3:], db_con=db_con)
            else:
                ret = module.run(environ=environ, urlvars=path[3:])
            status = ret.get('status', status)
            content_type = ret.get('content_type', content_type)
            template = ret.get('template', template)
            data.update(ret['data'])

        if not hasattr(template_cache, template):
            fo = open(os.path.dirname(__file__) + '/templates/' + template, 'r')
            template_cache[template] = string.Template(fo.read())
            fo.close()
        output = template_cache[template].substitute(data)

    except Exception as e:
        status = '500 Internal Server Error'
        content_type = 'text/plain; charset=utf-8'
        output = ''
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        for line in traceback.format_exception(exc_type, exc_obj, exc_traceback):
            output += line + '\n'
    finally:
        if 'db_con' in locals(): db_con.close()

        response_headers = [('Content-type', content_type),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [bytes(output, 'utf8')]
