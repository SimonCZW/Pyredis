#!/usr/bin/python
# -*- coding: utf-8 -*-

class KVDB(dict):

    def __init__(self, **kw):
        super(KVDB, self).__init__(**kw)

    def kget(self, key):
        try:
            return self[key]
        except KeyError:
            #raise AttributeError("has no attribute '%s'" % key)
            return None

    def kvset(self, key, value):
        self[key] = value
        return True


if __name__ == '__main__':
    a=KVDB()
    #a['1']=2
    a['2']=[1,2]
    #print a
    #a.kvset('2', [1, 2])
    #print a.kget('2')
    a.kvset('1', 2)
    print a.kget('1')
    print a


