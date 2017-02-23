#!/usr/bin/python

import socket

HOST='127.0.0.1'
PORT=5678
ADDR=(HOST, PORT)
BUFSIZ=1024

tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSock.bind(ADDR)
tcpSock.listen(5)

while True:
    print 'waiting connecting ...'
    tcpCliSock, addr = tcpSock.accept()
    print '... connected from:', addr

    while True:
        #data = tcpCliSock.recv(BUFSIZ)
        rdata = tcpCliSock.makefile('rb', BUFSIZ)
        wdata = tcpCliSock.makefile('wb', BUFSIZ)
        data = rdata.readline()
        if not data:
            break
        #tcpCliSock.send('[%s] %s' % ('ttttt', data))
        wdata.write('[%s] %s' % ('ttt', data))

tcpCliSock.close()
tcpSock.close()
