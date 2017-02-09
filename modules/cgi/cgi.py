#!/usr/bin/python3

import html

def run(environ, urlvars):
    body = '<h1>Environment / CGI variable dump</h1>\n<table class="table">\n'
    for key, value in sorted(environ.items(), key=lambda s: str(s).lower()):
        body += ("  <tr><th>%s</th><td>%s</td></tr>\n" % (key, html.escape(str(value))))
    body += '</table>\n'

    ret = {
        'data': {
            'title': 'CGI Dump',
            'body': body,
        },
    }
    return ret
