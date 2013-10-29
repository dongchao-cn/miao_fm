#coding:utf8
import time
import json
import tornado

from util import APIBaseHandler, MainJsonEncoder
from music.model import MusicSet
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

    @authenticated(['admin'])
    def get(self, user_id):
        user = UserSet.get_user(user_id)
        self.write(user)

    @authenticated(['admin'])
    def put(self, user_id):
        '''
        only update info for admin
        only update user level
        '''
        user_level = self.get_argument("user_level")
        user = UserSet.get_user(user_id)
        user.update_level(user_level)
        user = UserSet.get_user(user_id)
        self.write(user)

    @authenticated(['admin'])
    def delete(self, user_id):
        user = UserSet.get_user(user_id)
        user.remove()
        self.write(None)

class APIUserCurrentHandler(APIBaseHandler):
    '''
    get:
        get current user

    post:
        login

    put:
        update self info

    delete:
        logout
    '''

    def get(self):
        user = UserSet.get_user_by_name(self.current_user)
        self.write(user)
        
    def post(self):
        user_name = self.get_argument('user_name')
        user_password = self.get_argument('user_password')
        user = UserSet.get_user_by_name(user_name)
        if user and user.check_pw(user_password) and user.user_level != 'disable':
            self.set_current_user(user_name)
            self.write(user)
            return
        self.write(None)

    def put(self):
        user_password = self.get_argument("user_password")
        user = UserSet.get_user_by_name(self.current_user)
        user.update_info(user_password)
        user = UserSet.get_user_by_name(self.current_user)
        self.write(user)

    def delete(self):
        self.clear_cookie('user')
        self.write(None)

class APIUserFavourSetHandler(APIBaseHandler):
    '''
    get:
        get favours

    post:
        add a new favour

    del:
        del all favours
    '''

    def get(self):
        user = UserSet.get_user_by_name(self.current_user)
        self.write(user.user_favour)

    def post(self):
        music_id = self.get_argument("music_id")
        user = UserSet.get_user_by_name(self.current_user)
        user.add_favour(music_id)
        user = UserSet.get_user_by_name(self.current_user)
        self.write(user)

    def delete(self):
        user = UserSet.get_user_by_name(self.current_user)
        user.remove_all_favour()
        self.write(None)

class APIUserFavourHandler(APIBaseHandler):
    '''
    del:
        del favour
    '''
    def delete(self, music_id):
        user = UserSet.get_user_by_name(self.current_user)
        user.remove_favour(music_id)
        self.write(user)

class APIUserDislikeSetHandler(APIBaseHandler):
    '''
    get:
        get dislikes

    post:
        add a new dislike

    del:
        del all dislikes
    '''

    def get(self):
        user = UserSet.get_user_by_name(self.current_user)
        self.write(user.user_dislike)

    def post(self):
        music_id = self.get_argument("music_id")
        user = UserSet.get_user_by_name(self.current_user)
        user.add_dislike(music_id)
        user = UserSet.get_user_by_name(self.current_user)
        self.write(user)

    def delete(self):
        user = UserSet.get_user_by_name(self.current_user)
        user.remove_all_dislike()
        self.write(None)

class APIUserDislikeHandler(APIBaseHandler):
    '''
    del:
        del dislike
    '''
    def delete(self, music_id):
        user = UserSet.get_user_by_name(self.current_user)
        user.remove_dislike(music_id)
        self.write(user)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

class RegistHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("regist.html")

class UserHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("user.html")
