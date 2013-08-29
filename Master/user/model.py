#!/usr/bin/env python
#coding:utf8

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')

import hashlib
from mongoengine import *
import datetime
class User(Document):
    '''
    store user info
    '''
    user_name = StringField(max_length = 20, default = '', unique = True)
    user_password = StringField(max_length = 20, required = True)
    user_status = IntField(required = True)
    user_create_time = DateTimeField(required = True)

    def __str__(self):
        return ('user_name = %s\n') % (self.username).encode('utf-8')

    def update(self, user_name):
        if User.find_user_by_name(self.user_name) is None:
            self.user_name = user_name
            self.save()

    @classmethod
    def find_user_by_name(cls, user_name):
        return User.objects(user_name = username).first()

    @classmethod
    def check_login(cls, user_name, user_password):
        user = User.find_user_by_name(user_name)
        if user is not None:
            check_password = hashlib.md5(user_password +
                str(user.user_create_time)).hexdigest().upper()
            if (check_password == user.user_password):
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def regist_new_user(cls, user_name, user_password):
        if User.find_user_by_name(user_name) is not None:
            return u"用户名已经存在"
        user_create_time = datatime.now()
        save_password = hashlib.md5(user_name + str(user_create_time
          )).hexdigest().upper()
        new_user = User(user_name = user_name, user_password = save_password, user_status = 0,
            user_create_time = user_create_time
            )
        new_user.save()
        return u"注册成功"

