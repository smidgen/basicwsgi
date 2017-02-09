#!/usr/bin/python3

from config import modules_allowed, index_module

def run(environ, urlvars):
    '''The index page for this application.
    This particular version actually is an index of the available modules.
    '''

    body = '''<h1>Welcome</h1>
    <p>This is a basic Python web application without Django or any other web framework.</p>
    <ul>
    '''
    for module, is_allowed in sorted(modules_allowed.items(), key=lambda s: str(s).lower()):
        if is_allowed and module != index_module:
            body += '<li><a href="{0:s}">{0:s}</a></li>'.format(module)
    body += '</ul>'

    ret = {
        'data': {
            'title': 'Index',
            'body': body,
        },
    }
    return ret
