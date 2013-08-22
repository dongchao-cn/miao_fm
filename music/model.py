#!/usr/bin/env python
#coding:utf8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import hashlib
import random
import shutil
import os
from os.path import getsize
from mongoengine import *

from config import MUSIC_FILE_PATH

connect('miao_fm')

class Music(Document):
    music_name = StringField(primary_key=True, max_length=200)
    file_name = StringField(max_length=40, required=True)
    file_size = IntField(required=True)

    def __str__(self):
        return ('music_name = %s\nfile_name = %s\nfile_size = %s\n' % \
            (self.music_name, self.file_name, self.file_size)).encode('utf-8')

def get_music(music_name):
    '''
    get music by music_name
    return Music Object or None
    '''
    return Music.objects(music_name=music_name).first()

def set_music(music_name, file):
    '''
    set music info and store the music file
    if music_name exist, rewrite it
    '''
    file_size = getsize(file)
    with open(file,'r') as f:
        file_name = hashlib.md5(f.read()).hexdigest() + file[file.rindex('.'):]
    shutil.copy(file,MUSIC_FILE_PATH+file_name)
    Music(music_name,file_name,file_size).save()
    pass

def del_music(music_name):
    '''
    del music from db and del file
    '''
    music = Music.objects(music_name=music_name).first()
    os.remove(MUSIC_FILE_PATH+music.file_name)
    music.delete()

def get_random_music():
    '''
    get random music
    '''
    num = random.randint(0,Music.objects().count()-1)
    return Music.objects[num]

if __name__ == '__main__':
    set_music(u'兄妹',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    print get_music(u'兄妹')
    set_music(u'兄妹1',u'/media/823E59BF3E59AD43/Music/02十年.mp3')
    # set_music(u'兄妹2',u'/media/823E59BF3E59AD43/Music/02十年.mp3')
    # set_music(u'兄妹3',u'/media/823E59BF3E59AD43/Music/02十年.mp3')
    # set_music(u'兄妹4',u'/media/823E59BF3E59AD43/Music/02十年.mp3')
    print get_music(u'兄妹')
    # del_music(u'兄妹')
    # print get_music(u'兄妹')

    print get_random_music()
