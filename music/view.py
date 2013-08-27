#coding:utf8
import os
import tornado
import json

from .model import MusicControl,MusicJsonEncoder
from config import ABS_PATH

class APIMusicControlHandler(tornado.web.RequestHandler):
    '''
    get:
        list all music by range

    post:
        add a new music
    '''
    def get(self):
        start = int(self.get_argument("start",0))
        end = int(self.get_argument("end",0))
        music_list = MusicControl.get_music_by_range(start, end)
        self.write(json.dumps(music_list, cls=MusicJsonEncoder))

    def post(self):
        music_list = []
        for upload_file in self.request.files['file']:
            save_file_path = ABS_PATH + "/uploads/" + upload_file['filename']
            with open(save_file_path, 'w') as f:
                f.write(upload_file['body'])
                music_list.append(MusicControl.add_music(save_file_path, True))
        self.write(json.dumps(music_list, cls=MusicJsonEncoder))

class APIMusicHandler(tornado.web.RequestHandler):
    '''
    get:
        get music details

    put:
        update music

    delete:
        delete music
    '''
    def get(self, music_id):
        music = MusicControl.get_music(music_id)
        self.write(json.dumps(music, cls=MusicJsonEncoder))

    def put(self, music_id):
        music_id = self.get_argument("music_id")
        music_name = self.get_argument("music_name")
        music_artist = self.get_argument("music_artist")
        music_album = self.get_argument("music_album")

        music = MusicControl.get_music(music_id)
        music.update_info(music_name, music_artist, music_album)
        music = MusicControl.get_music(music_id)
        self.write(json.dumps(music, cls=MusicJsonEncoder))

    def delete(self, music_id):
        MusicControl.del_music(music_id)
        self.write('')

class NextMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music = MusicControl.get_next_music()
        self.write(music.play_data)

class MusicHandler(tornado.web.RequestHandler):
    def get(self):
        page = int(self.get_argument("page",1))
        music_list = MusicControl.get_music_by_page(page)
        page_num = MusicControl.get_music_page_count()
        self.render("music/music.html", msg='', music_list=music_list, page_num=page_num)

class AddMusicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("music/add_music.html", msg=u'新增音乐')

    def post(self):
        success_list = []
        error_list = []
        for file in self.request.files['file']:
            save_file_path = ABS_PATH + "/uploads/" + file['filename']
            with open(save_file_path, 'w') as f:
                f.write(file['body'])
            try:
                music_name = MusicControl.add_music(save_file_path, True)
                success_list.append(music_name)
            except:
                error_list.append(file['filename'])
            # os.remove(save_file_path)
        err_list_str = ''
        for each in error_list:
            err_list_str += '%s,' % each
        err_list_str = err_list_str[:-1]
        msg = u'成功添加%s个，失败%s个。\n失败文件为：%s' % \
            (len(success_list),len(error_list),err_list_str)
        self.render("music/add_music.html", msg=msg)

class EditMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_name = self.get_argument("music_name")
        self.render("music/edit_music.html", msg=u'编辑歌曲', 
            music=MusicControl.get_music(music_name))

    def post(self):
        old_music_name = self.get_argument("old_music_name")
        music_name = self.get_argument("music_name")
        music_artist = self.get_argument("music_artist")
        music_album = self.get_argument("music_album")
        music = MusicControl.get_music(old_music_name)
        try:
            ret = music.update(music_name, music_artist, music_album)
            msg = u'修改成功'
        except:
            music = MusicControl.get_music(old_music_name)
            msg = u'文件名已存在，修改失败!'
        self.render("music/edit_music.html", msg=msg, music=music)
        return

class DelMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_name = self.get_argument("music_name")
        MusicControl.del_music(music_name)
        music_list = MusicControl.get_music_by_page(1)
        page_num = MusicControl.get_music_page_count()
        self.render("music/music.html", msg=u'删除成功！', music_list=music_list, page_num=page_num)
        return

class FindMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_name = self.get_argument("music_name")
        music = MusicControl.get_music(music_name)
        if music:
            self.render("music/edit_music.html", msg='', music=music)
            return
        else:
            music_list = MusicControl.get_music_by_page(1)
            page_num = MusicControl.get_music_page_count()
            self.render("music/music.html", msg=u'未找到对应歌曲！', music_list=music_list, page_num=page_num)
            return