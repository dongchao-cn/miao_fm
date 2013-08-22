import os
import tornado.ioloop
import tornado.web
from music.view import GetMusicHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

settings = { 
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "debug" : True,
}

application = tornado.web.Application([
    (r"/", GetMusicHandler),
    # (r"/music_file/(.*)", ), handle in nginx
],**settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()