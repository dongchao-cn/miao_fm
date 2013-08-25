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
import multiprocessing
import subprocess
from os.path import getsize

import id3reader
from mongoengine import *

from cdn.model import CdnControl
from config import MUSIC_FILE_PATH, ITEM_PER_PAGE, MASTER_CDN

connect('miao_fm')

class Music(Document):
    '''
    store music info
    '''
    # music meta
    music_name = StringField(max_length=200, default='', unique=True)
    music_artist = StringField(max_length=50, default='')
    music_album = StringField(max_length=100, default='')

    # file info
    file_name = StringField(max_length=40, required=True)

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

    def update(self, music_name, music_artist, music_album):
        '''
        update music info
        '''
        self.music_name = music_name
        self.music_artist = music_artist
        self.music_album = music_album
        self.upload_data = datetime.datetime.now()
        self.save()

    @property
    def local_url(self):
        return 'http://%s/music_file/%s' % (MASTER_CDN, self.file_name)

class MusicControl(object):
    '''
    Music control functions
    '''

    def __init__(self):
        raise Exception,'MusicControl can\'t be __init__'

    @classmethod
    def add_music(cls, file, remove=False):
        '''
        add new music and store the music file
        read music info from id3
        if music_name exist, rewrite it
        '''
        with open(file,'r') as f:
            file_name = hashlib.md5(f.read()).hexdigest() + file[file.rindex('.'):]
        music_name, music_artist, music_album = _get_info_from_id3(file)
        Music(music_name=music_name, music_artist=music_artist, 
            music_album=music_album, file_name=file_name).save()
        # shutil.copy(file, MUSIC_FILE_PATH+file_name)
        multiprocessing.Process(target=_lame_mp3, args=(file, MUSIC_FILE_PATH+file_name, remove)).start()
        return music_name

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

def _lame_mp3(infile, outfile, remove=False):
    try:
        subprocess.call([ 
            "lame", 
            "--quiet", 
            "--mp3input", 
            "--abr", 
            "64", 
            infile, 
            outfile, 
            ])
    except:
        shutil.copy(infile, outfile)
    if remove:
        os.remove(infile)

def _get_info_from_id3(file):
    id3r = id3reader.Reader(file)
    
    try:
        music_name = id3r.getValue('title')
        music_name.encode('utf8')
    except:
        music_name = ''

    try:
        music_artist = id3r.getValue('performer')
        music_artist.encode('utf8')
    except :
        music_artist = ''

    try:
        music_album = id3r.getValue('album')
        music_album.encode('utf8')
    except :
        music_album = ''

    # music_name.encode('utf8')
    # music_artist.encode('utf8')
    # music_album.encode('utf8')

    # print music_name.encode('utf8')
    # print music_artist.encode('utf8')
    # print music_album.encode('utf8')
    # print type(music_name),type(music_artist),type(music_album)
    return (music_name, music_artist, music_album)

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

    # MusicControl.add_music(u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # MusicControl.add_music(u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # for i in range(8):
    #     MusicControl.add_music(u'兄妹'+str(i),'eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # print MusicControl.get_music_page_count()
    # print MusicControl.get_music_by_page(1)
    # print MusicControl.get_music_by_page(2)

    music = MusicControl.get_music(u'兄妹')
    print music.local_url
    # MusicControl.del_music(u'兄妹')
    # print MusicControl.get_music(u'兄妹')
    # MusicControl.add_music(u'兄妹','eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')

    # music = MusicControl.get_music(u'兄妹')
    # print music.play_data

    # print MusicControl.get_next_music()

    # MusicControl.add_music(u'兄妹','eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # music = MusicControl.get_music(u'兄妹')
    # print music.play_data
    # music.update("dsdsds")
    # print music.play_data

    # print MusicControl.get_music_page_count()

    # print _get_info_from_id3('/home/dc/Music/music_file/a01a45b7e7dd1f5b0e0a85db09d581c1.mp3')
    pass
