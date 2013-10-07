#coding:utf8
import datetime
import json
import tornado
from mongoengine import *
from bson.objectid import ObjectId

from music.model import Music
from report.model import Report
from cdn.model import Cdn
from user.model import User

class APIBaseHandler(tornado.web.RequestHandler):
    # def prepare(self):
    #     self.begin_time = time.time()

    # def on_finish(self):
    #     self.cost = time.time() - self.begin_time
    #     print self.request.method, self.request.uri, int(self.cost * 10e3)

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def set_default_headers(self):
        self.set_header ('Content-Type', 'application/json')

    def write(self, chunk):
        '''rewrite it to serialize obj to json'''
        chunk = json.dumps(chunk, cls=MainJsonEncoder)
        super(APIBaseHandler, self).write(chunk)

class MainJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, GridFSProxy):
            try:
                return obj._id
            except AttributeError:
                return ''
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, Music):
            return {'music_id' : obj.music_id,
                'music_name' : obj.music_name,
                'music_artist' : obj.music_artist,
                'music_album' : obj.music_album,
                'music_genre' : obj.music_genre,
                'file_id' : obj.file_id,
                'music_url' : obj.music_url,
                'upload_user' : obj.upload_user,
                'upload_date' : obj.upload_date}
        elif isinstance(obj, Report):
            return {'report_id' : obj.report_id,
                'report_music' : obj.report_music,
                'report_info' : obj.report_info,
                'report_date' : obj.report_date}
        elif isinstance(obj, Cdn):
            return {'cdn_id' : obj.cdn_id,
                'name' : obj.name,
                'url_path' : obj.url_path,
                'online' : obj.online}
        elif isinstance(obj, User):
            return {'user_id' : obj.user_id,
                'user_name' : obj.user_name,
                'user_password' : obj.user_password}
        else:
            return json.JSONEncoder.default(self, obj)