#coding:utf8
import time
import json
import tornado

from util import APIBaseHandler, MainJsonEncoder
from .model import UserSet, authenticated

class APIUserSetHandler(APIBaseHandler):
    '''
    get:
        get user status or range

    post:
        add a new user

    del:
        del all user
    '''

    @authenticated(['admin'])
    def get(self):
        by = self.get_argument('by')
        if by == 'status':
            base_info = {'total_count':UserSet.get_user_count()}
            self.write(base_info)
        elif by == 'range':
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
            user_list = UserSet.get_user_by_range(start, start+count)
            self.write(user_list)
        else:
            raise HTTPError(400)

    def post(self):
        user_name = self.get_argument("user_name")
        user_password = self.get_argument("user_password")
        # user_level = self.get_argument("user_level")
        user_level = 'normal'
        user = UserSet.add_user(user_name, user_password, user_level)
        self.write(user)

    @authenticated(['admin'])
    def delete(self):
        UserSet.remove_all_user()
        self.write(None)

class APIUserHandler(APIBaseHandler):
    '''
    get:
        get user details

    put:
        update user

    delete:
        delete user
    '''

    @authenticated(['normal', 'uploader', 'admin'])
    def get(self, user_id):
        current_user = UserSet.get_user_by_name(self.current_user)
        if current_user.user_level == 'admin' or \
            str(UserSet.get_user_by_name(self.current_user).user_id) == user_id:
            user = UserSet.get_user(user_id)
            self.write(user)
        else:
            self.write(None)

    @authenticated(['normal', 'uploader', 'admin'])
    def put(self, user_id):
        '''
        only update info NO LEVEL
        '''
        user_password = self.get_argument("user_password")
        current_user = UserSet.get_user_by_name(self.current_user)
        if current_user.user_level == 'admin' or \
            str(UserSet.get_user_by_name(self.current_user).user_id) == user_id:
            user = UserSet.get_user(user_id)
            user.update_info(user_password)
            user = UserSet.get_user(user_id)
            self.write(user)
        else:
            self.write(None)

    @authenticated(['admin'])
    def delete(self, user_id):
        user = UserSet.get_user(user_id)
        user.remove()
        self.write(None)

class APIUserLevelHandler(APIBaseHandler):
    '''
    put:
        update user level
    '''

    @authenticated(['admin'])
    def put(self, user_id):
        '''
        only update level
        '''
        user_level = self.get_argument("user_level")
        user = UserSet.get_user(user_id)
        user.update_level(user_level)
        user = UserSet.get_user(user_id)
        self.write(user)

class APIUserCurrentHandler(APIBaseHandler):
    '''
    get:
        get current user

    post:
        login

    delete:
        logout
    '''

    def get(self):
        user_name = self.get_secure_cookie('user')
        user = UserSet.get_user_by_name(user_name)
        self.write(user)
        
    def post(self):
        user_name = self.get_argument('user_name')
        user_password = self.get_argument('user_password')
        user = UserSet.get_user_by_name(user_name)
        if user and user.check_pw(user_password) and user.user_level != 'disable':
            self.set_secure_cookie('user', user_name)
            self.write(user)
            return
        self.write(None)

    def delete(self):
        self.clear_cookie('user')
        self.write(None)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

class RegistHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("regist.html")

class UserHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("user.html")