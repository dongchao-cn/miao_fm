#!/usr/bin/env python
#coding:utf8

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import json
import hashlib
import datetime

from mongoengine import *
from bson.objectid import ObjectId
import functools
from tornado.web import HTTPError

def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # print self.current_user
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

class User(Document):
    '''
    store user info
    '''
    user_name = StringField(max_length = 50, unique = True)
    user_password = StringField(max_length = 40, required = True)

    def __str__(self):
        return ('user_name = %s\n') % (self.user_name).encode('utf-8')

    @property
    def user_id(self):
        return self.pk

    def update_info(self, user_password):
        self.user_password = hashlib.md5(user_password +
            self.user_name).hexdigest().upper()
        self.save()

    def check_pw(self, user_password):
        check_password = hashlib.md5(user_password +
            self.user_name).hexdigest().upper()
        return check_password == self.user_password

    def remove(self):
        '''
        del user from db
        '''
        self.delete()

class UserControl(object):
    '''
    User control functions
    '''
    def __init__(self):
        raise Exception,'UserControl can\'t be __init__'

    @classmethod
    def add_user(cls, user_name, user_password):
        save_password = hashlib.md5(user_password + 
            user_name).hexdigest().upper()
        return User(user_name, save_password).save()

    @classmethod
    def get_user(cls, user_id):
        '''
        get user
        '''
        try:
            return User.objects(pk=user_id).first()
        except ValidationError:
            return None

    @classmethod
    def get_all_user(cls):
        '''
        get all user from db
        '''
        return User.objects()

    @classmethod
    def remove_all_user(cls):
        '''
        del user info
        '''
        for user in User.objects():
            user.remove()

    @classmethod
    def get_user_by_range(cls, start, end):
        '''
        get cdn by range
        '''
        return [each for each in User.objects[start : end]]

    @classmethod
    def get_user_count(cls):
        '''
        get cdn count
        '''
        return User.objects().count()

    @classmethod
    def get_user_by_name(cls, user_name):
        return User.objects(user_name = user_name).first()
