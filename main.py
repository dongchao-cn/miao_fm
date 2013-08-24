import os
import tornado.ioloop
import tornado.web
import music.view

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

settings = {
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "debug" : True,
}

application = tornado.web.Application([
    # main page
    (r"/", MainHandler),

    # api
    (r"/api/next_music/", music.view.NextMusicHandler),

    # admin page
    (r"/admin/music/", music.view.MusicHandler),
    (r"/admin/music/add_music/", music.view.AddMusicHandler),
    (r"/admin/music/edit_music/", music.view.EditMusicHandler),
    (r"/admin/music/find_music/", music.view.FindMusicHandler),
    (r"/admin/music/del_music/", music.view.DelMusicHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()