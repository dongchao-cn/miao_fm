#coding:utf8
import os
import tornado
from .model import MusicControl

class NextMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music = MusicControl.get_next_music()
        self.write(music.play_data)

class MusicHandler(tornado.web.RequestHandler):
    def get(self):
        page = int(self.get_argument("page",1))
        music_list = MusicControl.get_music_by_page(page)
        page_num = MusicControl.get_music_page_count()
        self.render("music.html", msg='', music_list=music_list, page_num=page_num)

class AddMusicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("add_music.html", msg=u'新增音乐')

    def post(self):
        try:
            music_name = self.get_argument("music_name")
            assert music_name
            music_artist = self.get_argument("music_artist")
            assert music_artist

            file = self.request.files['file'][0]
            save_file_path = "uploads/" + file['filename']
            with open(save_file_path, 'w') as f:
                f.write(file['body'])
        except:
            self.render("add_music.html", msg=u'参数填写错误！')
            return
        MusicControl.add_music(music_name, music_artist, save_file_path)
        os.remove(save_file_path)
        self.render("add_music.html", msg=u'新增成功！')
        return

class EditMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_name = self.get_argument("music_name")
        self.render("edit_music.html", msg=u'编辑歌曲', 
            music=MusicControl.get_music(music_name))

    def post(self):
        music_name = self.get_argument("music_name")
        music_artist = self.get_argument("music_artist")
        assert music_artist
        music = MusicControl.get_music(music_name)
        music.update(music_artist)
        self.render("edit_music.html", msg=u'修改成功！', music=music)
        return

class DelMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_name = self.get_argument("music_name")
        MusicControl.del_music(music_name)
        music_list = MusicControl.get_music_by_page(1)
        page_num = MusicControl.get_music_page_count()
        self.render("music.html", msg=u'删除成功！', music_list=music_list, page_num=page_num)
        return

class FindMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_name = self.get_argument("music_name")
        music = MusicControl.get_music(music_name)
        if music:
            self.render("edit_music.html", msg='', music=music)
            return
        else:
            music_list = MusicControl.get_music_by_page(1)
            page_num = MusicControl.get_music_page_count()
            self.render("music.html", msg=u'未找到对应歌曲！', music_list=music_list, page_num=page_num)
            return