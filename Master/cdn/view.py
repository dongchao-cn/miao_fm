#coding:utf8
import os
import json
import tornado
from user.view import authenticated, BaseHandler
from .model import CdnControl, CdnJsonEncoder

class APICdnControlHandler(BaseHandler):
    '''
    get:
        get cdn range
        list all cdn by range

    post:
        add a new cdn

    del:
        del all cdn
    '''
    @authenticated
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
        self.write('')

class APICdnHandler(BaseHandler):
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
        self.write('')

class CdnHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("cdn/cdn.html")
