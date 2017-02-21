#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import threading
from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler

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
#print get_config()


class MyRequestHandler(StreamRequestHandler):
    def handle(self):
        cur_thread = threading.current_thread()
        print 'connected from:', self.client_address, cur_thread
        self.wfile.write('[%s] %s' % (cur_thread,
            self.rfile.readline()))


class PyredisThreadingTCPServer(ThreadingMixIn, TCPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == '__main__':
    config = get_config()
    ADDR = (config['HOST'], config['PORT'])

    server = PyredisThreadingTCPServer(ADDR, MyRequestHandler)
    try:
        server.serve_forever()
    #ctrl - c
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

    #try:
    #    server_thread = threading.Thread(target = server.serve_forever)
    #    server_thread.setDaemon(True)
    #    server_thread.start()
    #    print "Server loop runing in thread:", server_thread.name
    #except KeyboardInterrupt:
    #    server.shutdown()
    #    server.server_close()


