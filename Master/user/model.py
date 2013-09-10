#!/usr/bin/env python
#coding:utf8

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import hashlib
import datetime

from mongoengine import *

class User(Document):
    '''
    store user info
    '''
    user_name = StringField(max_length = 20, default = '', unique = True)
    user_password = StringField(max_length = 100, required = True)

    def __str__(self):
        return ('user_name = %s\n') % (self.user_name).encode('utf-8')

    def update(self, user_password):
        self.user_password = hashlib.md5(user_password +
            self.user_name).hexdigest().upper()
        self.save()

    def check_pw(self, user_password):
        check_password = hashlib.md5(user_password +
            self.user_name).hexdigest().upper()
        return check_password == self.user_password

class UserControl(object):
    '''
    User control functions
    '''

    @classmethod
    def regist_new_user(cls, user_name, user_password):
        if UserControl.find_user_by_name(user_name):
            return False
        save_password = hashlib.md5(user_password + 
            user_name).hexdigest().upper()
        print save_password
        new_user = User(user_name = user_name, user_password = save_password)
        new_user.save()
        return True

    @classmethod
    def find_user_by_name(cls, user_name):
        return User.objects(user_name = user_name).first()
