#coding:utf8
import os
import tornado
from .model import CdnControl

class CdnHandler(tornado.web.RequestHandler):
    def get(self):
        cdn_list = CdnControl.get_all_cdn()
        self.render("cdn/cdn.html", msg='', cdn_list=cdn_list)

class AddCdnHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("cdn/add_cdn.html", msg=u'新增CDN')

    def post(self):
        try:
            name = self.get_argument("name")
            assert name
            url_path = self.get_argument("url_path")
            assert url_path
        except:
            self.render("cdn/add_cdn.html", msg=u'参数填写错误！')
            return
        CdnControl.add_cdn(name, url_path)
        self.render("cdn/add_cdn.html", msg=u'新增成功！')
        return

class DelCdnHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name")
        CdnControl.del_cdn(name)
        cdn_list = CdnControl.get_all_cdn()
        self.render("cdn/cdn.html", msg=u'删除成功！', cdn_list=cdn_list)
        return