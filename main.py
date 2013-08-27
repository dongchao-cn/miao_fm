import os
import tornado.ioloop
import tornado.web
import cdn.view
import music.view

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("admin_base.html")

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
    (r"/admin/", AdminHandler),

    (r"/admin/music/", music.view.MusicHandler),
    (r"/admin/music/add_music/", music.view.AddMusicHandler),
    (r"/admin/music/edit_music/", music.view.EditMusicHandler),
    (r"/admin/music/find_music/", music.view.FindMusicHandler),
    (r"/admin/music/del_music/", music.view.DelMusicHandler),

    (r"/admin/cdn/", cdn.view.CdnHandler),
    (r"/admin/cdn/add_cdn/", cdn.view.AddCdnHandler),
    (r"/admin/cdn/del_cdn/", cdn.view.DelCdnHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
