#coding:utf8
import os
import tornado
from .model import get_music,set_music,del_music,get_empty_music_obj,save_music_obj,\
    get_random_music,get_music_by_order,get_music_count
from config import PAGE_RANGE

class NextMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music = get_random_music()
        self.write(music.play_data())

class AddMusicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("add_music.html", msg='新建歌曲', music=get_empty_music_obj())

    def post(self):
        music = get_empty_music_obj()
        try:
            music_name = self.get_argument("music_name")
            assert music_name
            music.music_name = music_name
            music_artist = self.get_argument("music_artist")
            assert music_artist
            music.music_artist = music_artist

            file = self.request.files['file'][0]
            save_file_path = "uploads/" + file['filename']
            with open(save_file_path, 'w') as f:
                f.write(file['body'])
        except:
            self.render("add_music.html", msg='参数填写错误，上传失败！', music=music)
            return
        set_music(music_name, music_artist, save_file_path)
        os.remove(save_file_path)
        self.render("add_music.html", msg='上传成功！', music=get_empty_music_obj())
        return

class EditMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_name = self.get_argument("music_name")
        self.render("edit_music.html", msg='编辑歌曲', music=get_music(music_name))

    def post(self):
        music_name = self.get_argument("music_name")
        music = get_music(music_name)
        try:
            music_artist = self.get_argument("music_artist")
            assert music_artist
            music.music_artist = music_artist
        except :
            self.render("edit_music.html", msg='参数填写错误！', music=music)
            return
        save_music_obj(music)
        self.render("edit_music.html", msg='修改成功！', music=music)
        return

class MusicHandler(tornado.web.RequestHandler):
    def get(self):
        page = int(self.get_argument("page",1))
        music_list = get_music_by_order((page-1)*PAGE_RANGE,PAGE_RANGE)
        page_num = get_music_count()/PAGE_RANGE
        self.render("music.html", msg='', music_list=music_list, page_num=page_num)
        return

class DelMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_name = self.get_argument("music_name")
        del_music(music_name)
        page = int(self.get_argument("page",1))
        music_list = get_music_by_order((page-1)*PAGE_RANGE,PAGE_RANGE)
        page_num = get_music_count()/PAGE_RANGE
        self.render("music.html", msg='删除成功！', music_list=music_list, page_num=page_num)
        return

class FindMusicHandler(tornado.web.RequestHandler):
    def get(self):
        print 'get!!!!'
        music_name = self.get_argument("music_name")
        music = get_music(music_name)
        if music:
            self.render("edit_music.html", msg='', music=music)
            return
        else:
            page = int(self.get_argument("page",1))
            music_list = get_music_by_order((page-1)*PAGE_RANGE,PAGE_RANGE)
            page_num = get_music_count()/PAGE_RANGE
            self.render("music.html", msg='未找到对应歌曲！', music_list=music_list, page_num=page_num)
            return