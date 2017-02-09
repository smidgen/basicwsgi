#!/usr/bin/python3
'This file contains immutable application-wide configuration variables.'

IS_DEV_SERVER = True

index_module = 'index'
modules_allowed = {
    'index':     True,
    'cgi':       IS_DEV_SERVER,
    'coffee':    True,
    'mysqltest': True,
    'upload':    True,
}

mysql_config = {
    'host':     'localhost',
    'user':     'test',
    'password': 'mysqltest',
    'db':       'test'
}
