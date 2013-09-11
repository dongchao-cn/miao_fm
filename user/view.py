#coding:utf8
import tornado
from model import User

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):
    def post(self):
        user_name = self.get_argument("user_name")
        user_password = self.get_argument("user_password")
        if User.check_login(user_name, user_password):
            self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

    def get(self):
        self.render("user/user_login.html")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class RegistHandler(BaseHandler):
    def post(self):
        user_name = self.get_argument("user_name")
        user_password = self.get_argument("user_password")
        self.write(User.regist_new_user(user_name, user_password))
        self.redirect("/")

    def get(self):
        self.render("user/user_regist.html")
