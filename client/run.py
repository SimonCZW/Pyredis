#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import argparse

def arg_parse():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        '-d', '--debug',
        action = 'store_true',
        default = False,
        help = 'print debug infomation'
        )

    parser = argparse.ArgumentParser(
        prog = 'kv_client',
        parents = [parent_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = 'pyredis client.')
    parser.add_argument(
        '--host',
        action = 'store',
        type = str,
        dest = 'HOST',
        default = '127.0.0.1',
        help = 'host',
        metavar = '127.0.0.1')
    parser.add_argument(
        '--port','-p',
        action = 'store',
        type = int,
        dest = 'PORT',
        default = '5678',
        help = 'host to bind to',
        metavar = '5678')

    subparsers = parser.add_subparsers(
        title = 'Subcommands CMD',
        description = """
    SHELL                   Open a shell.
    SET key value           Set value.
    GET key
    AUTH username password
    URL name url""")

    parser_set = subparsers.add_parser(
        'SET',
        parents = [parent_parser],
        usage = '%(prog)s [-h] key value',
        help = 'SET key value')
    parser_set.add_argument(
        action = 'store',
        dest = 'kvset',
        nargs = 2,
        help = 'SET key value')

    parser_get = subparsers.add_parser(
        'GET',
        parents = [parent_parser],
        usage = '%(prog)s [-h] key',
        help = 'GET key')
    parser_get.add_argument(
        action = 'store',
        dest = 'kget',
        nargs = 1,
        help = 'GET key')

    parser_get = subparsers.add_parser(
        'AUTH',
        parents = [parent_parser],
        usage = '%(prog)s [-h] username password',
        help = 'AUTH username password')
    parser_get.add_argument(
        action = 'store',
        dest = 'auth',
        nargs = 2,
        help = 'AUTH username password')

    parser_get = subparsers.add_parser(
        'URL',
        parents = [parent_parser],
        usage = '%(prog)s [-h] name url',
        help = 'URL name url')
    parser_get.add_argument(
        action = 'store',
        dest = 'url',
        nargs = 2,
        help = 'URL name url')

    parser_get = subparsers.add_parser(
        'SHELL',
        usage = '%(prog)s [-h]',
        help = 'Open a shell.')
    parser_get.add_argument(
        action = 'store_true',
        dest = 'shell',
        default = False,
        help = 'Open a shell.')
    return parser.parse_args()

config = {}
args = arg_parse()
for k,v in vars(args).iteritems():
    if v:
        config[k] = v

print config

#HOST='127.0.0.1'
#PORT=5678
#BUFSIZ=1024
#ADDR=(HOST, PORT)

#ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ClientSock.connect(ADDR)

#while True:
#    sdata = raw_input('> ')
#    if not sdata:
#        break
#    ClientSock.send('%s\r\n' % sdata)
#    rdata = ClientSock.recv(BUFSIZ)
#    if not rdata:
#        break
#    print rdata

#ClientSock.close()



