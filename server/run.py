#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import argparse

from SocketServer import (TCPServer as TCP, StreamRequestHandler as SRH)
from time import ctime

HOST=''
PORT=5678
ADDR=(HOST, PORT)
#AUTH_FILE = '/etc/pyredis/auth.conf'
AUTH_FILE = 'auth.conf'

def arg_parse():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        '-d', '--debug',
        action = 'store_true',
        default = False,
        help = 'print debug infomation'
        )

    parser = argparse.ArgumentParser(
        prog = 'kv_server',
        parents = [parent_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = 'pyredis server.')
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
    parser.add_argument(
        '--authconfig',
        action = 'store',
        type = argparse.FileType('r'),
        dest = 'authconf',
        #default = './auth.conf',
        #required = False,
        help = 'auth.conf for cmd: AUTH.',
        metavar = 'auth.conf')
    return parser.parse_args()

def get_config():
    config = {}
    user = {}
    args = arg_parse()
    for k,v in vars(args).iteritems():
        #get username,password from auth.conf
        if k == 'authconf':
            config['authconf']=[]
            if v is not None:
                for line in v.readlines():
                    #make sure auth.conf file format is username:password
                    if len(line.strip('\n').split(':')) == 2:
                        (username, password) = line.strip('\n').split(':')
                        config['authconf'].append({username: password})
                v.close()
            #default auth.conf
            else:
                if os.path.isfile(AUTH_FILE):
                    with open(AUTH_FILE) as f:
                        for line in f.readlines():
                            if len(line.strip('\n').split(':')) == 2:
                                (username, password) = line.strip('\n').split(':')
                                config['authconf'].append({username: password})
        elif v is not None:
            config[k] = v

    return config

print get_config()

class MyRequestHandler(SRH):
    def handle(self):
        print 'connected from:', self.client_address
        self.wfile.write('[%s] %s' % (ctime(),
            self.rfile.readline()))

#tcpServ=TCP(ADDR, MyRequestHandler)
#print 'waiting for connecting...'
#tcpServ.serve_forever()

