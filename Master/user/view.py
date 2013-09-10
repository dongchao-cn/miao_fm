#coding:utf8
import tornado
from model import UserControl

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("user/login.html")

    def post(self):
        user_name = self.get_argument("user_name")
        user_password = self.get_argument("user_password")
        user = UserControl.find_user_by_name(user_name)
        if user and user.check_pw(user_password):
            print 'success'
            self.set_secure_cookie("user", self.get_argument("user_name"))
        self.redirect("/admin/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class RegistHandler(BaseHandler):
    def get(self):
        self.render("user/reg.html")

    def post(self):
        user_name = self.get_argument("user_name")
        user_password = self.get_argument("user_password")
        if UserControl.regist_new_user(user_name, user_password):
            self.redirect("/admin/")
        else:
            self.redirect("/")
