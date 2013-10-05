#coding:utf8
import os
import tornado
import json

from user.view import authenticated, APIBaseHandler
from .model import MusicControl,MusicJsonEncoder
from master_config import ABS_PATH

class APIMusicControlHandler(APIBaseHandler):
    '''
    get:
        get music status or range

    post:
        add a new music

    del:
        del all music
    '''
    @authenticated
    def get(self):
        by = self.get_argument('by')
        if by == 'status':
            base_info = {'total_count':MusicControl.get_music_count()}
            self.write(base_info)
        elif by == 'range':
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
            music_list = MusicControl.get_music_by_range(start, start+count)
            self.write(json.dumps(music_list, cls=MusicJsonEncoder))
        else:
            raise HTTPError(400)

    @authenticated
    def post(self):
        music_list = []
        for upload_file in self.request.files['file']:
            save_file_path = ABS_PATH + "/uploads/" + upload_file['filename']
            with open(save_file_path, 'w') as f:
                f.write(upload_file['body'])
                music_list.append(MusicControl.add_music(save_file_path, True))
        self.write(json.dumps(music_list, cls=MusicJsonEncoder))

    @authenticated
    def delete(self):
        MusicControl.remove_all_music()
        self.write({})

class APIMusicHandler(APIBaseHandler):
    '''
    get:
        get music details

    put:
        update music

    delete:
        delete music
    '''

    @authenticated
    def get(self, music_id):
        music = MusicControl.get_music(music_id)
        self.write(json.dumps(music, cls=MusicJsonEncoder))

    @authenticated
    def put(self, music_id):
        music_name = self.get_argument("music_name")
        music_artist = self.get_argument("music_artist")
        music_album = self.get_argument("music_album")
        music_genre = self.get_argument("music_genre")

        music = MusicControl.get_music(music_id)
        music.update_info(music_name, music_artist, music_album, music_genre)
        music = MusicControl.get_music(music_id)
        self.write(json.dumps(music, cls=MusicJsonEncoder))

    @authenticated
    def delete(self, music_id):
        music = MusicControl.get_music(music_id)
        music.remove()
        self.write({})

class APINextMusicHandler(APIBaseHandler):
    '''
    get:
        get next music for play
    '''
    def get(self):
        music = MusicControl.get_next_music()
        self.write(json.dumps(music, cls=MusicJsonEncoder))

class MusicControlHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("music.html")
