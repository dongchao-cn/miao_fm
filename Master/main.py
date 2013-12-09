#!/usr/bin/env python
#coding:utf8
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import music.view
import user.view
import report.view
import status.view

import gridfs
from pymongo import Connection
from bson.objectid import ObjectId
from mongoengine import *
from tornado.options import define, options

from master_config import MONGODB_URL, MONGODB_PORT

define("port", default=8000, help="run on the given port", type=int)
con = Connection("%s:%s" % (MONGODB_URL, MONGODB_PORT))
db = con['miao_fm_cdn']
fs = gridfs.GridFS(db)

connect('miao_fm', host=MONGODB_URL, port=MONGODB_PORT)
register_connection('miao_fm_cdn', 'miao_fm_cdn', host=MONGODB_URL, port=MONGODB_PORT)


class FileHandler(tornado.web.RequestHandler):
    def get(self, file_id):
        self.set_header('Content-Type', 'audio/mpeg')
        self.write(fs.get(ObjectId(file_id)).read())


class ImgHandler(tornado.web.RequestHandler):
    def get(self, file_id):
        self.set_header('Content-Type', 'image/jpeg')
        self.write(fs.get(ObjectId(file_id)).read())


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("admin_base.html")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "debug": True,
    "cookie_secret": "63oETzKXQkGaYdkLqw421fdasqw12335uYh7EQnp2XdTP1o/Vo=",
    # "xsrf_cookies": True,
}

application = tornado.web.Application([
    # main page
    (r"/", MainHandler),

    # api
    (r"/api/status/", status.view.APIStatusHandler),

    (r"/api/music/", music.view.APIMusicSetHandler),
    (r"/api/music/(\w{24})/", music.view.APIMusicHandler),
    (r"/api/music/next/", music.view.APIMusicNextHandler),

    (r"/api/user/", user.view.APIUserSetHandler),
    (r"/api/user/(\w{24})/", user.view.APIUserHandler),
    (r"/api/user/current/", user.view.APIUserCurrentHandler),
    (r"/api/user/current/favour/", user.view.APIUserFavourSetHandler),
    (r"/api/user/current/favour/(\w{24})/", user.view.APIUserFavourHandler),
    (r"/api/user/current/dislike/", user.view.APIUserDislikeSetHandler),
    (r"/api/user/current/dislike/(\w{24})/", user.view.APIUserDislikeHandler),
    (r"/api/user/current/vote/", user.view.APIUserVoteSetHandler),

    (r"/api/report/", report.view.APIReportSetHandler),
    (r"/api/report/(\w{24})/", report.view.APIReportHandler),

    # admin page
    (r"/admin/", AdminHandler),
    (r"/login/", user.view.LoginHandler),
    (r"/regist/", user.view.RegistHandler),
    (r"/admin/music/", music.view.MusicHandler),
    (r"/admin/report/", report.view.ReportHandler),
    (r"/admin/user/", user.view.UserHandler),

    # local music server
    (r"/music_file/(\w{24})/", FileHandler),
    (r"/music_img/(\w{24})/", ImgHandler),
], **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
