#coding:utf8
import os
import tornado
import json

from util import APIBaseHandler, MainJsonEncoder
from user.model import authenticated
from user.model import UserSet
from .model import MusicSet
from .recommendations import get_next_music
from master_config import ABS_PATH

class APIMusicSetHandler(APIBaseHandler):
    '''
    get:
        get music status or range

    post:
        add a new music

    del:
        del all music
    '''
    @authenticated(['uploader', 'admin'])
    def get(self):
        by = self.get_argument('by')
        if by == 'status':
            base_info = {'total_count':MusicSet.get_music_count()}
            self.write(base_info)
        elif by == 'range':
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
            music_list = MusicSet.get_music_by_range(start, start+count)
            self.write(music_list)
        else:
            raise HTTPError(400)

    @authenticated(['uploader', 'admin'])
    def post(self):
        music_list = []
        user_name = self.get_secure_cookie('user')
        for upload_file in self.request.files['file']:
            save_file_path = ABS_PATH + "/uploads/" + upload_file['filename']
            save_file_path = save_file_path.encode('utf8')
            with open(save_file_path, 'w') as f:
                f.write(upload_file['body'])
                music_list.append(MusicSet.add_music(save_file_path, user_name, True))
        self.write(music_list)

    @authenticated(['uploader', 'admin'])
    def delete(self):
        MusicSet.remove_all_music()
        self.write(None)

class APIMusicHandler(APIBaseHandler):
    '''
    get:
        get music details

    put:
        update music

    delete:
        delete music
    '''

    @authenticated(['uploader', 'admin'])
    def get(self, music_id):
        music = MusicSet.get_music(music_id)
        self.write(music)

    @authenticated(['uploader', 'admin'])
    def put(self, music_id):
        music_name = self.get_argument("music_name")
        music_artist = self.get_argument("music_artist")
        music_album = self.get_argument("music_album")

        music = MusicSet.get_music(music_id)
        if music:
            music.update_info(music_name, music_artist, music_album)
            music = MusicSet.get_music(music_id)
            self.write(music)
        else:
            self.write(None)

    @authenticated(['uploader', 'admin'])
    def delete(self, music_id):
        music = MusicSet.get_music(music_id)
        music.remove()
        self.write(None)

class APIMusicNextHandler(APIBaseHandler):
    '''
    get:
        get next music info for play
    '''
    def get(self):
        # print 'APIMusicNextHandler'
        user = UserSet.get_user_by_name(self.current_user)
        # print user
        if user:
            user.user_listened += 1
            user.save()
        music = get_next_music(user.user_id)
        self.write(music)

class MusicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("music.html")
