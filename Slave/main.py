#!/usr/bin/env python
#coding:utf8
import os
import tornado.ioloop
import tornado.web

import gridfs
from pymongo import Connection
from bson.objectid import ObjectId

from slave_config import SLAVE_CDN, SLAVE_MONGODB_PORT

con = Connection("%s:%s" % (SLAVE_CDN, SLAVE_MONGODB_PORT))
db = con['miao_fm_cdn']
fs = gridfs.GridFS(db)

class FileHandler(tornado.web.RequestHandler):
    def get(self, file_id):
        self.set_header ('Content-Type', 'audio/mpeg')
        self.write(fs.get(ObjectId(file_id)).read())

settings = {
    "debug" : True,
}

application = tornado.web.Application([
    # main page
    (r"/music_file/(\w{24})/", FileHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()