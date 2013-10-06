#!/usr/bin/env python
#coding:utf8
import os
import tornado.ioloop
import tornado.web
import cdn.view
import music.view
import user.view
import report.view

import gridfs
from pymongo import Connection
from bson.objectid import ObjectId
from mongoengine import *

from master_config import MASTER_CDN, MASTER_MONGODB_PORT

con = Connection("%s:%s" % ('127.0.0.1', MASTER_MONGODB_PORT))
db = con['miao_fm_cdn']
fs = gridfs.GridFS(db)

connect('miao_fm', host='127.0.0.1' ,port=MASTER_MONGODB_PORT)
register_connection('miao_fm_cdn', 'miao_fm_cdn', host='127.0.0.1' ,port=MASTER_MONGODB_PORT)

class FileHandler(tornado.web.RequestHandler):
    def get(self, file_id):
        self.set_header ('Content-Type', 'audio/mpeg')
        self.write(fs.get(ObjectId(file_id)).read())

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("admin_base.html")

settings = {
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "debug" : True,
    "cookie_secret": "63oETzKXQkGaYdkLqw421fdasqw12335uYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login/",
    # "xsrf_cookies": True,
}

application = tornado.web.Application([
    # main page
    (r"/", MainHandler),

    # api
    (r"/api/music/", music.view.APIMusicSetHandler),
    (r"/api/music/(\w{24})/", music.view.APIMusicHandler),
    (r"/api/music/next/", music.view.APIMusicNextHandler),

    (r"/api/cdn/", cdn.view.APICdnSetHandler),
    (r"/api/cdn/(\w{24})/", cdn.view.APICdnHandler),

    (r"/api/user/", user.view.APIUserSetHandler),
    (r"/api/user/(\w{24})/", user.view.APIUserHandler),
    (r"/api/user/current/", user.view.APIUserCurrentHandler),

    (r"/api/report/", report.view.APIReportSetHandler),
    (r"/api/report/(\w{24})/", report.view.APIReportHandler),

    # admin page
    (r"/admin/", AdminHandler),
    (r"/login/", user.view.LoginHandler),
    (r"/admin/music/", music.view.MusicHandler),
    (r"/admin/report/", report.view.ReportHandler),
    
    # local music server
    (r"/music_file/(\w{24})/", FileHandler),
],**settings)

if __name__ == "__main__":
    application.listen(6000)
    tornado.ioloop.IOLoop.instance().start()
