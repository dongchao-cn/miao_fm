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
            return del_dollor_in_dict(obj.to_dict())
        elif isinstance(obj, Report):
            return del_dollor_in_dict(obj.to_dict())
        elif isinstance(obj, User):
            return del_dollor_in_dict(obj.to_dict())
        elif isinstance(obj, Status):
            return del_dollor_in_dict(obj.to_dict())
        else:
            return json.JSONEncoder.default(self, obj)


def del_dollor_in_dict(d):
    if isinstance(d, dict):
        ret = {}
        for key in d:
            ret[key.replace('$', '')] = del_dollor_in_dict(d[key])
        return ret
    else:
        return d


if __name__ == '__main__':
    print del_dollor_in_dict({
        "music_artist": "陈奕迅",
        "music_url": "/music_file/528a35a856a9e50ae4c039d1/",
        "music_name": "沒有手機的日子",
        "music_id": "528a359456a9e50aa9c039d0",
        "music_file": {
            "$oid": "528a35a856a9e50ae4c039d1"
        },
        "music_tag": {
            "update_datetime": {
                "$date": 1384818280784
            }
        },
        "music_img": "http://img.xiami.com/images/album/img35/135/588_2.jpg",
        "music_played": 8,
        "music_upload_user": {
            "$oid": "527b46be56a9e50e002f5caf"
        },
        "_id": {
            "$oid": "528a359456a9e50aa9c039d0"
        },
        "music_album": "你的陈奕迅国语精选 CD 2",
        "music_upload_date": {
            "$date": 1384863638056
        }
    })
