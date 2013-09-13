#!/usr/bin/env python
#coding:utf8
import os
import tornado.ioloop
import tornado.web
import cdn.view
import music.view
import user.view

import gridfs
from pymongo import Connection
from bson.objectid import ObjectId

from master_config import MASTER_CDN, MASTER_MONGODB_PORT

con = Connection("%s:%s" % (MASTER_CDN, MASTER_MONGODB_PORT))
db = con['miao_fm_cdn']
fs = gridfs.GridFS(db)

class FileHandler(tornado.web.RequestHandler):
    def get(self, file_id):
        self.set_header ('Content-Type', 'audio/mpeg')
        self.write(fs.get(ObjectId(file_id)).read())

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

class AdminHandler(tornado.web.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin_base.html")

settings = {
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "debug" : True,
    "cookie_secret": "63oETzKXQkGaYdkLqw421fdasqw12335uYh7EQnp2XdTP1o/Vo=",
    "login_url": "/admin/login/",
    # "xsrf_cookies": True,
}

application = tornado.web.Application([
    # main page
    (r"/", MainHandler),

    # local music server
    (r"/music_file/(\w{24})/", FileHandler),

    # api
    # (r"/api/music/(\w{24})/", music.view.APIMusicHandler),
    (r"/api/music/", music.view.APIMusicControlHandler),
    (r"/api/music/next/", music.view.APINextMusicHandler),
    (r"/api/music/(\w{24})/", music.view.APIMusicHandler),

    (r"/api/cdn/", cdn.view.APICdnControlHandler),
    (r"/api/cdn/(\w{24})/", cdn.view.APICdnHandler),

    # admin page
    (r"/admin/", AdminHandler),

    (r"/admin/music/", music.view.MusicControlHandler),

    (r"/admin/cdn/", cdn.view.CdnHandler),
    
    (r"/admin/login/", user.view.LoginHandler),
    (r"/admin/regist/", user.view.RegistHandler),
    (r"/admin/logout/", user.view.LogoutHandler),
    
],**settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
