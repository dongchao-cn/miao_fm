#!/usr/bin/env python
#coding:utf8

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')

import hashlib
import json
from mongoengine import *
class User(Document):
    '''
    store user info
    '''
    user_name = StringField(max_length = 20, default = '', unique = True)
    user_password = StringField(max_length = 20, required = True)
    user_create_time = DateTimeField(required = True)

    def __str__(self):
        return ('user_name = %s\n') % (self.username).encode('utf-8')

    def create(self):
        if User.find_user_by_name(self.user_name) is not None:
            self.save()

    def update(self, user_name):
        if User.find_user_by_name(self.user_name) is None:
            self.user_name = user_name
            self.save()

    @classmethod
    def find_user_by_name(cls, user_name):
        return User.objects(user_name = username).first()
