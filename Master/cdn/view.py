#coding:utf8
import os
import json
import tornado
from user.view import authenticated, APIBaseHandler
from .model import CdnControl, CdnJsonEncoder

class APICdnControlHandler(APIBaseHandler):
    '''
    get:
        get cdn status or range

    post:
        add a new cdn

    del:
        del all cdn
    '''
    @authenticated
    def get(self):
        by = self.get_argument('by')
        if by == 'status':
            base_info = {'total_count':CdnControl.get_cdn_count()}
            self.write(base_info)
        elif by == 'range':
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
            cdn_list = CdnControl.get_cdn_by_range(start, start+count)
            self.write(json.dumps(cdn_list, cls=CdnJsonEncoder))
        else:
            raise HTTPError(400)
            
    @authenticated
    def post(self):
        name = self.get_argument("name")
        url_path = self.get_argument("url_path")
        online = self.get_argument("online")
        online = True if online else False
        cdn = CdnControl.add_cdn(name, url_path, online)
        self.write(json.dumps(cdn, cls=CdnJsonEncoder))

    @authenticated
    def delete(self):
        CdnControl.remove_all_cdn()
        self.write({})

class APICdnHandler(APIBaseHandler):
    '''
    get:
        get cdn details

    put:
        update cdn

    delete:
        delete cdn
    '''
    @authenticated
    def get(self, cdn_id):
        music = CdnControl.get_cdn(cdn_id)
        self.write(json.dumps(music, cls=CdnJsonEncoder))

    @authenticated
    def put(self, cdn_id):
        name = self.get_argument("name")
        url_path = self.get_argument("url_path")
        online = self.get_argument("online")
        online = True if online else False
        cdn = CdnControl.get_cdn(cdn_id)
        cdn.update_info(name, url_path, online)
        cdn = CdnControl.get_cdn(cdn_id)
        self.write(json.dumps(cdn, cls=CdnJsonEncoder))

    @authenticated
    def delete(self, cdn_id):
        cdn = CdnControl.get_cdn(cdn_id)
        cdn.remove()
        self.write({})

class CdnHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("cdn/cdn.html")
