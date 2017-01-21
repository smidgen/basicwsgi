#!/usr/bin/python3

def run(environ, urlvars):
    'Returns an HTTP 418 status code with appropriate message.'
    ret = {
        'status': '418 I\'m a teapot',
        'data': {
            'title': "I'm a teapot",
            'body': "<h1>I'm a teapot. I don't make coffee.</h1>",
        },
    }
    return ret
