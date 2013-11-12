#!/usr/bin/env python
#coding:utf8

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import hashlib
import json

from mongoengine import *
import functools
from tornado.web import HTTPError


def authenticated(req):
    def actualDecorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = UserSet.get_user_by_name(self.current_user)
            if not user:
                raise HTTPError(403)
            user_level = user.user_level
            # print self.current_user,user_level,req
            if user_level not in req:
                raise HTTPError(403)
            return method(self, *args, **kwargs)
        return wrapper
    return actualDecorator


class User(Document):
    '''
    store user info
    all item and functions start with *user_* will be auto serialized
    '''
    user_name = StringField(max_length=50, unique=True)
    user_password = StringField(max_length=40, required=True)

    # 4 user level : disable, normal, uploader, admin
    user_level = StringField(max_length=20, default='normal')
    user_listened = IntField(default=0)
    user_favour = ListField(StringField(max_length=24), default=[])
    user_dislike = ListField(StringField(max_length=24), default=[])

    @property
    def user_id(self):
        return self.pk

    def __str__(self):
        return ('user_name = %s') % (self.user_name).encode('utf-8')

    def to_dict(self):
        user_str = super(User, self).to_json()
        user = json.loads(user_str)
        user['user_id'] = str(self.user_id)
        return user

    def update_info(self, user_password):
        self.user_password = hashlib.md5(
            user_password.encode('utf8') + self.user_name.encode('utf8')).hexdigest().upper()
        self.save()

    def check_pw(self, user_password):
        check_password = hashlib.md5(user_password.encode('utf8') + self.user_name.encode('utf8')).hexdigest().upper()
        return check_password == self.user_password

    def update_level(self, user_level):
        self.user_level = user_level
        self.save()

    def add_favour(self, music_id):
        self.update(add_to_set__user_favour=music_id)

    def remove_favour(self, music_id):
        self.user_favour.remove(music_id)
        self.save()

    def remove_all_favour(self):
        self.user_favour = []
        self.save()

    def add_dislike(self, music_id):
        self.update(add_to_set__user_dislike=music_id)

    def remove_dislike(self, music_id):
        self.user_dislike.remove(music_id)
        self.save()

    def remove_all_dislike(self):
        self.user_dislike = []
        self.save()

    def remove(self):
        self.delete()

    def gc(self):
        from music.model import MusicSet
        self.user_favour = [music for music in self.user_favour if MusicSet.get_music(music)]
        self.user_dislike = [music for music in self.user_dislike if MusicSet.get_music(music)]
        self.save()


class UserSet(object):
    '''
    User control functions
    '''
    def __init__(self):
        raise Exception('UserSet can\'t be __init__')

    @classmethod
    def add_user(cls, user_name, user_password, user_level):
        save_password = hashlib.md5(user_password.encode('utf8') + user_name.encode('utf8')).hexdigest().upper()
        try:
            return User(user_name, save_password, user_level).save()
        # except NotUniqueError:
        except:
            return None

    @classmethod
    def get_user(cls, user_id):
        try:
            return User.objects(pk=user_id).first()
        except ValidationError:
            return None

    @classmethod
    def get_all_user(cls):
        return User.objects()

    @classmethod
    def remove_all_user(cls):
        for user in User.objects():
            user.remove()

    @classmethod
    def get_user_by_range(cls, start, end):
        return [each for each in User.objects[start: end]]

    @classmethod
    def get_user_count(cls):
        return User.objects().count()

    @classmethod
    def get_user_by_name(cls, user_name):
        return User.objects(user_name=user_name).first()
