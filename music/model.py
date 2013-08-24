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
from os.path import getsize
from mongoengine import *

from config import MUSIC_FILE_PATH

connect('miao_fm')

class Music(Document):
    # music meta
    music_name = StringField(primary_key=True, max_length=200, default='')
    music_artist = StringField(max_length=40, required=True, default='')

    # file info
    file_name = StringField(max_length=40, required=True, default='')

    # upload info
    # upload_user = ReferenceField('')
    upload_data = DateTimeField(default=datetime.datetime.now())
    
    meta = {
        'ordering': ['-upload_data']
    }

    def __str__(self):
        return ('music_name = %s\nfile_name = %s\n' % \
            (self.music_name, self.file_name)).encode('utf-8')

    def play_data(self):
        return json.dumps({ 'music_name' : self.music_name, 
            'music_artist' : self.music_artist,
            'file' : self.file_name })

def get_music(music_name):
    '''
    get music by music_name
    return Music Object or None
    '''
    return Music.objects(music_name=music_name).first()

def set_music(music_name, music_artist, file):
    '''
    set music info and store the music file
    if music_name exist, rewrite it
    '''
    with open(file,'r') as f:
        file_name = hashlib.md5(f.read()).hexdigest() + file[file.rindex('.'):]
    shutil.copy(file,MUSIC_FILE_PATH+file_name)
    Music(music_name, music_artist, file_name).save()
    
def del_music(music_name):
    '''
    del music from db and del file
    '''
    music = Music.objects(music_name=music_name).first()
    try:
        music.delete()
        os.remove(MUSIC_FILE_PATH+music.file_name)
    except:
        pass

def get_empty_music_obj():
    '''
    get random music
    '''
    return Music()

def save_music_obj(music_obj):
    '''
    get random music
    '''
    music_obj.save()

def get_random_music():
    '''
    get random music
    '''
    num = random.randint(0,Music.objects().count()-1)
    return Music.objects[num]

def get_music_by_order(start, limit):
    return Music.objects[start:start+limit]

def get_music_count():
    '''
    get music count
    '''
    return Music.objects().count()

if __name__ == '__main__':
    # set_music(u'兄妹','eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # print get_music(u'兄妹')
    # set_music(u'兄妹1','eason',u'/media/823E59BF3E59AD43/Music/02十年.mp3')
    # print get_music(u'兄妹1')
    # set_music(u'floorfiller','eason',u'/media/823E59BF3E59AD43/Music/floorfiller.mp3')
    # print get_music(u'floorfiller')
    # del_music(u'兄妹')
    # print get_music(u'兄妹')

    # print get_random_music()
    # print get_music_by_order(0,3)
    pass
