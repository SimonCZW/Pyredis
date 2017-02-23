#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import threading
from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler, BaseRequestHandler

from store import KVDB

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

        #sharing kvdb between threads
        global _db

        #default no auth
        is_auth_user = False

        #for recv multiple data sent from client
        #and interact with client
        while True:
            self.rfile = self.connection.makefile('rb', self.rbufsize)
            self.wfile = self.connection.makefile('wb', self.wbufsize)

            cmds = self.rfile.readline().strip().split()
            #aviod nont data from client(cause by CMD: quit|q|exit)
            if cmds:
                action = cmds[0].upper()
            else:
                action = None

            #judge action
            if action == 'SET':
                if len(cmds) != 3:
                    self.wfile.write(
                        (1, "Only need three arguements(SET key value)."))
                else:
                    #should judge key and value type before storing ...
                    (key, value) = (cmds[1].strip("\'").strip("\""),
                                    cmds[2].strip("\'").strip("\""))
                    #set k-v
                    if _db.kvset(key, value):
                        self.wfile.write(0)

            elif action == 'GET':
                if len(cmds) != 2:
                    self.wfile.write(
                        (1, "Only need two arguements(GET key)."))
                else:
                    #get value by key
                    value = _db.kget(cmds[1].strip("\'").strip("\""))
                    if value:
                        self.wfile.write(value)
                    else:
                        self.wfile.write(None)

            elif action == 'AUTH':
                if len(cmds) != 3:
                    self.wfile.write((1,
                         "Only need three arguements(AUTH username password)."))
                else:
                    (username, password)=(str(cmds[1].strip("\'").strip("\"")),
                                          str(cmds[2].strip("\'").strip("\"")))
                    #each thread get authconf by global
                    global config
                    auths = config['authconf'] #'authconf': [{'czw': '123456'}]

                    #identify username and password
                    for auth in auths:
                        if {username: password} == auth:
                            is_auth_user = True

                    if is_auth_user:
                        self.wfile.write(0)
                    else:
                        self.wfile.write(-1)

            elif action == 'URL':
                if len(cmds) != 3:
                    self.wfile.write((1,
                         "Only need three arguements(URL name url)."))
                else:
                    #not auth ,then return none
                    if not is_auth_user:
                        self.wfile.write(None)
                    #auth
                    else:
                        (name, url) = (str(cmds[1].strip("\'").strip("\"")),
                                       str(cmds[2].strip("\'").strip("\"")))
                        #attempt to get value by urlname
                        url_value = _db.kget(name)

                        #has value by name
                        if url_value:
                            self.wfile.write(url_value)
                        #without value, then obtain value by url and set k-v
                        else:
                            #get standard url format
                            import re
                            if not re.match('http://|https://', url):
                                url = 'http://' + url

                            #get url's status_code and size
                            import urllib2
                            try:
                                rq = urllib2.urlopen(url)
                                status_code = rq.code
                                url_size = len(rq.read())
                            except:
                                status_code = 404
                                url_size = 0
                            finally:
                                url_value = (status_code , url_size)

                            #set k-v and return
                            if (_db.kvset(name, url_value)
                                    and url_value is not None):
                                self.wfile.write(url_value)
                            else:
                                self.wfile.write(
                                    (1, 'Cannot combine %s with %s' %
                                        (name, url_value)))
            #cause by client CMD quit|q|exit
            elif action is None:
                pass

            #other cmd
            else:
                self.wfile.write((1, "No such command."))


class PyredisThreadingTCPServer(ThreadingMixIn, TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    config = get_config()
    ADDR = (config['HOST'], config['PORT'])

    #for threading sharing same data
    _db = KVDB()

    server = PyredisThreadingTCPServer(ADDR, MyRequestHandler)
    try:
        print "Pyredis listening in: %s ..." % str(ADDR)
        server.serve_forever()
    #ctrl - c
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


