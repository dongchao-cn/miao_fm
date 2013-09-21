#!/usr/bin/env python
#coding:utf8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import datetime
import random
import os
import json
import multiprocessing
import subprocess
from os.path import getsize

import id3reader
from mongoengine import *
from bson.objectid import ObjectId

from cdn.model import CdnControl
from master_config import ITEM_PER_PAGE, MASTER_CDN, MASTER_MONGODB_PORT

# connect('miao_fm', host=MASTER_CDN ,port=MASTER_MONGODB_PORT)
register_connection('miao_fm_cdn', 'miao_fm_cdn', host=MASTER_CDN ,port=MASTER_MONGODB_PORT)

class MusicJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, GridFSProxy):
            try:
                return obj._id
            except AttributeError:
                return ''
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, Music):
            return {'music_id' : obj.music_id,
                'music_name' : obj.music_name,
                'music_artist' : obj.music_artist,
                'music_album' : obj.music_album,
                'file_id' : obj.file_id,
                'music_url' : obj.music_url,
                'upload_data' : obj.upload_data}
        else:
            return json.JSONEncoder.default(self, obj)

class Music(Document):
    '''
    store music info
    '''
    # music meta
    music_name = StringField(max_length=200, default='')
    music_artist = StringField(max_length=50, default='')
    music_album = StringField(max_length=100, default='')

    # file info
    music_file = FileField('miao_fm_cdn')

    # upload info
    # upload_user = ReferenceField('')
    upload_data = DateTimeField(default=datetime.datetime.now())

    @property
    def music_id(self):
        return self.pk

    @property
    def music_url(self):
        return 'http://%s/music_file/%s/' % (CdnControl.get_free_cdn().url, self.file_id)

    @property
    def file_id(self):
        try:
            return self.music_file._id
        except AttributeError:
            return ''

    meta = {
        'ordering': ['-upload_data']
    }

    def __str__(self):
        return ('music_name = %s\nmusic_file = %s\n' % \
            (self.music_name, self.music_file)).encode('utf-8')
    
    def update_info(self, music_name, music_artist, music_album):
        '''
        update music info
        '''
        self.music_name = music_name
        self.music_artist = music_artist
        self.music_album = music_album
        self.upload_data = datetime.datetime.now()
        self.save()

    def update_file(self, file):
        '''
        update music info
        '''
        try:
            self.reload()
            with open(file, 'r') as f:
                self.music_file.replace(f)
            self.save()
        except mongoengine.errors.OperationError:
            pass

    def remove(self):
        '''
        del music from db and remove file
        '''
        self.music_file.delete()
        self.delete()

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
        music_name, music_artist, music_album = _get_info_from_id3(file)
        music = Music(music_name=music_name, music_artist=music_artist, 
            music_album=music_album, music_file=open(file, 'r').read()).save()
        multiprocessing.Process(target=_lame_mp3, args=(file, music, remove)).start()
        return music

    @classmethod
    def get_music(cls, music_id):
        '''
        get music by music_id
        return Music Object or None
        '''
        try:
            return Music.objects(pk=music_id).first()
        except ValidationError:
            return None

    @classmethod
    def remove_all_music(cls):
        '''
        del music from db and remove file
        '''
        for music in Music.objects():
            music.remove()

    @classmethod
    def get_next_music(cls):
        assert Music.objects().count() != 0
        return _get_random_music()

    @classmethod
    def get_music_by_name(cls, music_name):
        '''
        get music by music_name
        return Music Object or None
        '''
        return Music.objects(music_name=music_name).first()

    @classmethod
    def get_music_by_range(cls, start, end):
        '''
        get music by range
        '''
        return [each for each in Music.objects[start : end]]

    @classmethod
    def get_music_count(cls):
        '''
        get music count
        '''
        return Music.objects().count()

    @classmethod
    def get_music_by_page(cls, page):
        '''
        get music by page
        '''
        page -= 1
        return cls.get_music_by_range(page*ITEM_PER_PAGE, (page+1)*ITEM_PER_PAGE)
        # return Music.objects[page*ITEM_PER_PAGE: (page+1)*ITEM_PER_PAGE]

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

def _lame_mp3(infile, music, remove=False):
    '''
    lame the mp3 to smaller
    '''
    outfile = infile+'.tmp'
    subprocess.call([ 
        "lame", 
        "--quiet", 
        "--mp3input", 
        "--abr", 
        "64", 
        infile, 
        outfile
        ])
    music.update_file(outfile)
    os.remove(outfile)

    if remove:
        os.remove(infile)

def _get_info_from_id3(file):
    id3r = id3reader.Reader(file)
    
    try:
        music_name = id3r.getValue('title').encode('utf8')
    except:
        music_name = ''

    try:
        music_artist = id3r.getValue('performer').encode('utf8')
    except :
        music_artist = ''

    try:
        music_album = id3r.getValue('album').encode('utf8')
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

    # music = MusicControl.add_music(u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # print music
    # import time
    # time.sleep(10)
    # music = MusicControl.get_music(u'兄妹')
    # print music.play_data
    # print music.local_url

    # MusicControl.del_music(u'兄妹')
    # music = MusicControl.get_music(u'兄妹')
    # print music

    # MusicControl.add_music(u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # for i in range(8):
    #     MusicControl.add_music(u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # print MusicControl.get_music_page_count()
    # print MusicControl.get_music_by_page(1)
    # print MusicControl.get_music_by_page(2)

    # music = MusicControl.get_music(u'兄妹')
    # print music.local_url
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
