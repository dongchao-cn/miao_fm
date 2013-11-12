#coding:utf8
import json
import tornado
from mongoengine import *
from music.model import Music
from report.model import Report
from user.model import User
from status.model import Status


class APIBaseHandler(tornado.web.RequestHandler):
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
        if isinstance(obj, Music):
            return obj.to_dict()
        elif isinstance(obj, Report):
            return obj.to_dict()
        elif isinstance(obj, User):
            return obj.to_dict()
        elif isinstance(obj, Status):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)
