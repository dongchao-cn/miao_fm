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

class APIMusicNextHandler(tornado.web.RequestHandler):
    '''
    get:
        get next music for play
    '''
    def get(self):
        music = MusicControl.get_next_music()
        self.write(json.dumps(music, cls=MusicJsonEncoder))

class MusicHandler(tornado.web.RequestHandler):
    def get(self):
        page = int(self.get_argument("page",1))
        music_list = MusicControl.get_music_by_page(page)
        page_num = MusicControl.get_music_page_count()
        self.render("music/music.html", music_list=music_list, page_num=page_num)

class AddMusicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("music/add_music.html")

    def post(self):
        music_list = []
        for upload_file in self.request.files['file']:
            save_file_path = ABS_PATH + "/uploads/" + upload_file['filename']
            with open(save_file_path, 'w') as f:
                f.write(upload_file['body'])
                music_list.append(MusicControl.add_music(save_file_path, True))
        self.redirect('/admin/music/')

class EditMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_id = self.get_argument("music_id")
        self.render("music/edit_music.html", msg=u'编辑歌曲', 
            music=MusicControl.get_music(music_id))

    def post(self):
        music_id = self.get_argument("music_id")
        music_name = self.get_argument("music_name")
        music_artist = self.get_argument("music_artist")
        music_album = self.get_argument("music_album")

        music = MusicControl.get_music(music_id)
        ret = music.update_info(music_name, music_artist, music_album)
        self.redirect('/admin/music/edit_music/?music_id='+music_id)

class DelMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_id = self.get_argument("music_id")
        MusicControl.del_music(music_id)
        self.redirect('/admin/music/')

class FindMusicHandler(tornado.web.RequestHandler):
    def get(self):
        music_id = self.get_argument("music_id")
        music = MusicControl.get_music(music_id)
        if music:
            self.render("music/edit_music.html", msg='', music=music)
            return
        else:
            self.redirect('/admin/music/')
            return