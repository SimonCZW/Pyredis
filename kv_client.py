#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import argparse

#parsing arguments and subcommand
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

#get config
def get_config():
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
    return config


#print help information before interact shell
def print_help():
    print "Help:"
    print """    SET key value           Set value.
    GET key
    AUTH username password
    URL name url
    QUIT|quit|EXIT|exit|q       close termimal"""
    print


#wrapper client tcp socket
class ClientSocket(object):
    def __init__(self, ADDR):
        self.addr = ADDR
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect()
        except:
            print "Cannot connect to:", ADDR

    def connect(self):
        self.tcpsock.connect(self.addr)

    def send(self, data):
        self.tcpsock.send('%s\r\n' % data)
        #self.tcpsock.send(data)

    def sendall(self, data):
        self.tcpsock.sendall('%s\r\n' % data)

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

    #get config
    config = get_config()
    ADDR=(config['HOST'], config['PORT'])

    #get socket and auto connect to ADDR
    clisock = ClientSocket(ADDR)

    #interact shell with server
    if config['shell']:
        print_help()
        try:
            while True:
                sdata = raw_input('> ').strip()

                #input nothing
                if not sdata:
                    continue

                #quit shell
                elif (sdata == 'exit' or sdata == 'EXIT' or
                      sdata == 'quit' or sdata == 'QUIT' or
                      sdata == 'q' or sdata == 'Q'):
                    break

                #help
                elif sdata == 'help' or sdata == 'HELP':
                    print_help()

                #send something to server
                else:
                    clisock.send(sdata)
                    rdata = clisock.recv()
                    #if not rdata:
                    #    break
                    print rdata
        #ctrl-c
        except KeyboardInterrupt:
            #send none, cause disconnect message printed in server
            clisock.send('')
            #connect close
            clisock.close()

    #subcommand: SET key value
    elif config['kvset']:
        #sdata = {'SET': {config['kvset'][0]: config['kvset'][1]}}
        sdata = 'SET'+" "+config['kvset'][0]+" "+config['kvset'][1]
        print clisock.sendrecvclose(sdata)

    #subcommand: GET key
    elif config['kget']:
        sdata = 'GET'+" "+config['kget'][0]
        print clisock.sendrecvclose(sdata)

    #subcommand: AUTH username password
    elif config['auth']:
        sdata = 'AUTH'+" "+config['auth'][0]+" "+config['auth'][1]
        print clisock.sendrecvclose(sdata)

    #subcommand: URL name url
    elif config['url']:
        sdata = 'URL'+" "+config['url'][0]+" "+config['url'][1]
        print clisock.sendrecvclose(sdata)


if __name__ == '__main__':
    main()


