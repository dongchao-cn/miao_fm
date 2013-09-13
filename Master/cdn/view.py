#coding:utf8
import os
import json
import tornado
from .model import CdnControl, CdnJsonEncoder

class APICdnControlHandler(tornado.web.RequestHandler):
    '''
    get:
        get cdn range
        list all cdn by range

    post:
        add a new cdn

    del:
        del all cdn
    '''
    def get(self):
        '''
        return base info about music if can't get start or end
        else return music list
        '''
        try:
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
        except:
            base_info = {'total_count':CdnControl.get_cdn_count()}
            self.write(base_info)
            return
        cdn_list = CdnControl.get_cdn_by_range(start, start+count)
        self.write(json.dumps(cdn_list, cls=CdnJsonEncoder))

    def post(self):
        name = self.get_argument("name")
        url_path = self.get_argument("url_path")
        online = self.get_argument("online")
        online = True if online else False
        cdn = CdnControl.add_cdn(name, url_path, online)
        self.write(json.dumps(cdn, cls=CdnJsonEncoder))

    def delete(self):
        CdnControl.remove_all_cdn()
        self.write('')

class APICdnHandler(tornado.web.RequestHandler):
    '''
    get:
        get cdn details

    put:
        update cdn

    delete:
        delete cdn
    '''

    def get(self, cdn_id):
        music = CdnControl.get_cdn(cdn_id)
        self.write(json.dumps(music, cls=CdnJsonEncoder))

    def put(self, cdn_id):
        name = self.get_argument("name")
        url_path = self.get_argument("url_path")
        online = self.get_argument("online")
        online = True if online else False
        cdn = CdnControl.get_cdn(cdn_id)
        cdn.update_info(name, url_path, online)
        cdn = CdnControl.get_cdn(cdn_id)
        self.write(json.dumps(cdn, cls=CdnJsonEncoder))

    def delete(self, cdn_id):
        cdn = CdnControl.get_cdn(cdn_id)
        cdn.remove()
        self.write('')

class CdnHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("cdn/cdn.html")

# class AddCdnHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("cdn/add_cdn.html", msg=u'新增CDN')

#     def post(self):
#         try:
#             name = self.get_argument("name")
#             assert name
#             url_path = self.get_argument("url_path")
#             assert url_path
#         except:
#             self.render("cdn/add_cdn.html", msg=u'参数填写错误！')
#             return
#         try:
#             CdnControl.add_cdn(name, url_path)
#         except:
#             self.render("cdn/add_cdn.html", msg=u'CDN名已存在！')
#             return
#         self.render("cdn/add_cdn.html", msg=u'新增成功！')
#         return

# class DelCdnHandler(tornado.web.RequestHandler):
#     def get(self):
#         name = self.get_argument("name")
#         CdnControl.del_cdn(name)
#         cdn_list = CdnControl.get_all_cdn()
#         self.render("cdn/cdn.html", msg=u'删除成功！', cdn_list=cdn_list)
#         return