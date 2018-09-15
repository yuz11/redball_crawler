# -*- coding:utf-8 -*-
def NemoCfgMongoClient():
    #user = "root"
    #pw   = "bYKH2Utx47Nw4P"
    host = "0.0.0.0"
    port = 27017
    from pymongo import MongoClient
    uri = "mongodb://%s:%s" % (host, port)
    client = MongoClient(uri)
    return client
