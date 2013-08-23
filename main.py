import os
import tornado.ioloop
import tornado.web
from music.view import GetMusicHandler,AddMusicHandler,EditMusicHandler,\
	MusicHandler,DelMusicHandler,FindMusicHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

settings = { 
    # "static_path" : os.path.join(os.path.dirname(__file__), "static"),  handled in nginx
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "debug" : True,
}

application = tornado.web.Application([
    (r"/", GetMusicHandler),
    (r"/admin/music/", MusicHandler),
    (r"/admin/music/add_music/", AddMusicHandler),
    (r"/admin/music/edit_music/", EditMusicHandler),
    (r"/admin/music/find_music/", FindMusicHandler),
    (r"/admin/music/del_music/", DelMusicHandler),
    # (r"/admin/music/(.*)/", MusicHandler),
    
    
    # (r"/music_file/(.*)", ), handled in nginx
],**settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()