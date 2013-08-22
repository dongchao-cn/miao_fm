#coding:utf8
import tornado
from .model import get_music,set_music,del_music,get_random_music

class GetMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music = get_random_music()
        self.render("home.html", music=music)
