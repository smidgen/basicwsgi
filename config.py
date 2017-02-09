#!/usr/bin/python3
'This file contains immutable application-wide configuration variables.'

IS_DEV_SERVER = True

index_module = 'index'
modules_allowed = {
    'index':    True,
    'cgi':      IS_DEV_SERVER,
    'coffee':   True,
    'upload':   True,
}
