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
        description = """    SHELL                   Open a shell.
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
        help = 'Open a shell.')
    return parser.parse_args()

config = {}
args = arg_parse()
for k,v in vars(args).iteritems():
    if v:
        config[k] = v
    config.setdefault('shell', False)
    config.setdefault('kvset', False)
    config.setdefault('kget', False)
    config.setdefault('auth', False)
    config.setdefault('url', False)

#print config

ADDR=(config['HOST'], config['PORT'])

def print_help():
    print "Help:"
    print """    SET key value           Set value.
    GET key
    AUTH username password
    URL name url
    QUIT|quit|EXIT|exit|q       close termimal"""
    print

class ClientSocket(object):
    def __init__(self, ADDR):
        self.addr = ADDR
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.tcpsock.connect(self.addr)

    def send(self, data):
        self.tcpsock.send('%s\r\n' % data)

    def recv(self, bufsize=1024):
        return self.tcpsock.recv(bufsize)

    def close(self):
        self.tcpsock.close()

    def sendrecvclose(self, data):
        self.send(data)
        rdata = self.recv()
        self.close()
        return rdata

def main():

    clisock = ClientSocket(ADDR)

    #是否为交互shell情况
    if config['shell']:
        print_help()
        while True:
            sdata = raw_input('> ').strip()
            if not sdata:
                continue
            elif (sdata == 'exit' or sdata == 'EXIT' or
                  sdata == 'quit' or sdata == 'QUIT' or
                  sdata == 'q' or sdata == 'Q'):
                break

            clisock.send(sdata)
            rdata = clisock.recv()
            if not rdata:
                break
            print rdata

        clisock.close()

    elif config['kvset']:
        sdata = {'SET': {config['kvset'][0]: config['kvset'][1]}}
        print clisock.sendrecvclose(sdata)
    elif config['kget']:
        sdata = {'GET': config['kget'][0]}
        print clisock.sendrecvclose(sdata)
    elif config['auth']:
        sdata = {'AUTH': {config['auth'][0]: config['auth'][1]}}
        print clisock.sendrecvclose(sdata)
    elif config['url']:
        sdata = {'URL': {config['url'][0]: config['url'][1]}}
        print clisock.sendrecvclose(sdata)

if __name__ == '__main__':
    main()


