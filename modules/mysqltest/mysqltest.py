#!/usr/bin/python3

import os, string, MySQLdb

REQUIRES_DB = True

def run(environ, urlvars, db_con):
    cursor = db_con.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, text FROM test')
    rows = cursor.fetchall()

    htmlvars = {
        'headers': '',
        'rows': '',
    }
    for desc in cursor.description:
        htmlvars['headers'] += '<th>%s</th>' % desc[0]

    for row in rows:
        htmlvars['rows'] += '<tr><td>{id}</td><td>{text}</td></tr>\n'.format_map(row)

    fo = open(os.path.dirname(__file__) + '/template.html', 'r')
    t = string.Template(fo.read())
    body = t.substitute(htmlvars)

    ret = {
        'data': {
            'title': 'MySQL Test',
            'body': body,
        },
    }
    return ret
