#coding:utf8
import datetime
import json
import tornado
from mongoengine import *
from bson.objectid import ObjectId
from music.model import Music
from report.model import Report
from user.model import User
from status.model import Status


class APIBaseHandler(tornado.web.RequestHandler):
    # def prepare(self):
    #     self.begin_time = time.time()

    # def on_finish(self):
    #     self.cost = time.time() - self.begin_time
    #     print self.request.method, self.request.uri, int(self.cost * 10e3)

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def set_current_user(self, user_name):
        self.set_secure_cookie('user', user_name)

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

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
            return _serialize_obj(obj, Music)
        elif isinstance(obj, Report):
            return _serialize_obj(obj, Report)
        elif isinstance(obj, User):
            return _serialize_obj(obj, User)
        elif isinstance(obj, Status):
            return _serialize_obj(obj, Status)
        else:
            return json.JSONEncoder.default(self, obj)


def _serialize_obj(obj, cls):
    prefix = cls.__name__.lower() + '_'
    d = {}
    for each in dir(obj):
        if each.startswith(prefix):
            d[each] = eval("obj."+each)
    return d
