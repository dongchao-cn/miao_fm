#coding:utf8
import time
import json
import tornado
import functools

from tornado.web import HTTPError

from model import UserControl, UserJsonEncoder

class APIBaseHandler(tornado.web.RequestHandler):
    # def prepare(self):
    #     self.begin_time = time.time()

    # def on_finish(self):
    #     self.cost = time.time() - self.begin_time
    #     print self.request.method, self.request.uri, int(self.cost * 10e3)

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def set_default_headers(self):
        self.set_header ('Content-Type', 'application/json')

def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # print self.current_user
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

class APIUserControlHandler(APIBaseHandler):
    '''
    get:
        get user status or range

    post:
        add a new user

    del:
        del all user
    '''
    @authenticated
    def get(self):
        by = self.get_argument('by')
        if by == 'status':
            base_info = {'total_count':UserControl.get_user_count()}
            self.write(base_info)
        elif by == 'range':
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
            user_list = UserControl.get_user_by_range(start, start+count)
            self.write(json.dumps(user_list, cls=UserJsonEncoder))
        else:
            raise HTTPError(400)

    @authenticated
    def post(self):
        user_name = self.get_argument("user_name")
        user_password = self.get_argument("user_password")
        user = UserControl.add_user(user_name, user_password)
        self.write(json.dumps(user, cls=UserJsonEncoder))

    @authenticated
    def delete(self):
        UserControl.remove_all_user()
        self.write({})

class APIUserHandler(APIBaseHandler):
    '''
    get:
        get user details

    put:
        update user

    delete:
        delete user
    '''

    @authenticated
    def get(self, user_id):
        user = UserControl.get_user(user_id)
        self.write(json.dumps(user, cls=UserJsonEncoder))

    @authenticated
    def put(self, user_id):
        user_password = self.get_argument("user_password")
        user = UserControl.get_user(user_id)
        user.update_info(user_password)
        user = UserControl.get_user(user_id)
        self.write(json.dumps(user, cls=UserJsonEncoder))

    @authenticated
    def delete(self, user_id):
        user = UserControl.get_user(user_id)
        user.remove()
        self.write({})

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
        user = self.get_secure_cookie('user')
        self.write({'user_name':user})

    def post(self):
        user_name = self.get_argument('user_name')
        user_password = self.get_argument('user_password')
        user = UserControl.get_user_by_name(user_name)
        if user and user.check_pw(user_password):
            self.set_secure_cookie('user', user_name)
            self.write({'status':True})
            return
        self.write({'status':False})

    def delete(self):
        self.clear_cookie('user')
        self.write({})

class UserLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("user/login.html")
