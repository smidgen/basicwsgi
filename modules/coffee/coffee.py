#!/usr/bin/python3

def run(environ, urlvars):
    'Returns an HTTP 418 status code with appropriate message.'
    ret = {
        'status': '418 I\'m a teapot',
        'data': {
            'title': '418 I&#39;m a teapot',
            'body': '<h1>I&#39;m a teapot. I don&#39;t make coffee.</h1>',
        },
    }
    return ret
