#!/usr/bin/env python
#coding:utf8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import hashlib
import datetime
import random
import json
import shutil
import os
import subprocess
from os.path import getsize

from mongoengine import *

from cdn.model import CdnControl
from config import MUSIC_FILE_PATH, ITEM_PER_PAGE

connect('miao_fm')

class Music(Document):
    '''
    store music info
    '''
    # music meta
    music_name = StringField(primary_key=True, max_length=200, default='')
    music_artist = StringField(max_length=40, required=True, default='')

    # file info
    file_name = StringField(max_length=40, required=True,unique=True)

    # upload info
    # upload_user = ReferenceField('')
    upload_data = DateTimeField(default=datetime.datetime.now())
    
    meta = {
        'ordering': ['-upload_data']
    }

    def __str__(self):
        return ('music_name = %s\nfile_name = %s\n' % \
            (self.music_name, self.file_name)).encode('utf-8')

    @property
    def play_data(self):
        '''
        get the play data for music
        return json
        '''
        return json.dumps({ 'music_name' : self.music_name, 
            'music_artist' : self.music_artist,
            'file' : '%s/music_file/%s' % (CdnControl.get_free_cdn().url, self.file_name) })

    def update(self, music_artist):
        '''
        update music info
        '''
        self.music_artist = music_artist
        self.upload_data = datetime.datetime.now()
        self.save()

class MusicControl(object):
    '''
    Music control functions
    '''

    def __init__(self):
        raise Exception,'MusicControl can\'t be __init__'

    @classmethod
    def add_music(cls, music_name, music_artist, file):
        '''
        add new music and store the music file
        if music_name exist, rewrite it
        '''
        with open(file,'r') as f:
            file_name = hashlib.md5(f.read()).hexdigest() + file[file.rindex('.'):]
        try:
            Music(music_name, music_artist, file_name).save()
        except NotUniqueError:
            return u'该文件已存在！'
        # shutil.copy(file, MUSIC_FILE_PATH+file_name)
        subprocess.call([ 
            "lame", 
            "--quiet", 
            "--mp3input", 
            "--abr", 
            "64", 
            file, 
            MUSIC_FILE_PATH+file_name, 
            ])

    @classmethod
    def get_music(cls, music_name):
        '''
        get music by music_name
        return Music Object or None
        '''
        return Music.objects(music_name=music_name).first()

    @classmethod
    def del_music(cls, music_name):
        '''
        del music from db and remove file
        '''
        music = Music.objects(music_name=music_name).first()
        try:
            music.delete()
            os.remove(MUSIC_FILE_PATH+music.file_name)
        except OSError:
            pass

    @classmethod
    def get_next_music(cls):
        assert Music.objects().count() != 0
        return _get_random_music()

    @classmethod
    def get_music_by_page(cls, page):
        '''
        get music by page
        '''
        page -= 1
        return Music.objects[page*ITEM_PER_PAGE: (page+1)*ITEM_PER_PAGE]

    @classmethod
    def get_music_page_count(cls):
        '''
        get music page count
        '''
        count = Music.objects().count()
        if count % ITEM_PER_PAGE:
            return count/ITEM_PER_PAGE+1
        else:
            return count/ITEM_PER_PAGE

def _get_random_music():
    '''
    get random music
    '''
    num = random.randint(0,Music.objects().count()-1)
    return Music.objects[num]

if __name__ == '__main__':
    # try:
    #     MusicControl()
    # except Exception:
    #     pass

    # for i in range(8):
    #     MusicControl.add_music(u'兄妹'+str(i),'eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # print MusicControl.get_music_page_count()
    # print MusicControl.get_music_by_page(1)
    # print MusicControl.get_music_by_page(2)

    # print MusicControl.get_music(u'兄妹')
    # MusicControl.del_music(u'兄妹')
    # print MusicControl.get_music(u'兄妹')
    # MusicControl.add_music(u'兄妹','eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')

    # music = MusicControl.get_music(u'兄妹')
    # print music.play_data

    # print MusicControl.get_next_music()

    MusicControl.add_music(u'兄妹','eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    music = MusicControl.get_music(u'兄妹')
    print music.play_data
    music.update("dsdsds")
    print music.play_data

    print MusicControl.get_music_page_count()
    pass
