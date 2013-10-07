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
import traceback
from os.path import getsize

import mutagen
import mongoengine.errors
from mongoengine import *
from bson.objectid import ObjectId

from cdn.model import CdnSet
from master_config import MASTER_CDN, MASTER_MONGODB_PORT

from user.model import User, UserSet
# connect('miao_fm', host='127.0.0.1' ,port=MASTER_MONGODB_PORT)
# register_connection('miao_fm_cdn', 'miao_fm_cdn', host='127.0.0.1' ,port=MASTER_MONGODB_PORT)

class Music(Document):
    '''
    store music info
    '''
    # music meta
    music_name = StringField(max_length=200, default='')
    music_artist = StringField(max_length=50, default='')
    music_album = StringField(max_length=100, default='')
    music_genre = StringField(max_length=100, default='')

    # file info
    music_file = FileField('miao_fm_cdn')

    # upload info
    upload_user = ReferenceField(User, reverse_delete_rule=NULLIFY)
    upload_date = DateTimeField()

    @property
    def music_id(self):
        return self.pk

    @property
    def music_url(self):
        return 'http://%s/music_file/%s/' % (CdnSet.get_free_cdn().url, self.file_id)

    @property
    def file_id(self):
        try:
            return self.music_file._id
        except AttributeError:
            return ''

    meta = {
        'ordering': ['-upload_date']
    }

    def __str__(self):
        return ('music_name = %s\nmusic_file = %s\n' % \
            (self.music_name, self.music_file)).encode('utf-8')
    
    def update_info(self, music_name, music_artist, music_album, music_genre):
        self.music_name = music_name
        self.music_artist = music_artist
        self.music_album = music_album
        self.music_genre = music_genre
        self.upload_date = datetime.datetime.now()
        self.save()

    def update_file(self, file):
        try:
            self.reload()
            with open(file, 'r') as f:
                self.music_file.replace(f)
                self.save()
        except mongoengine.errors.OperationError:
            pass

    def remove(self):
        self.music_file.delete()
        self.delete()

class MusicSet(object):
    '''
    Music control functions
    '''

    def __init__(self):
        raise Exception,'MusicSet can\'t be __init__'

    @classmethod
    def add_music(cls, file, user_name, remove=False):
        music_name, music_artist, music_album, music_genre = _get_info_from_id3(file)
        user = UserSet.get_user_by_name(user_name)
        music = Music(music_name=music_name, music_artist=music_artist, 
            music_album=music_album, music_genre=music_genre, 
            upload_user=user, upload_date=datetime.datetime.now(),
            music_file=open(file, 'r').read()).save()
        multiprocessing.Process(target=_lame_mp3, args=(file, music, remove)).start()
        return music

    @classmethod
    def get_music(cls, music_id):
        try:
            return Music.objects(pk=music_id).first()
        except ValidationError:
            return None

    @classmethod
    def remove_all_music(cls):
        for music in Music.objects():
            music.remove()

    @classmethod
    def get_next_music(cls):
        assert Music.objects().count() != 0
        return _get_random_music()

    @classmethod
    def get_music_by_name(cls, music_name):
        return Music.objects(music_name=music_name).first()

    @classmethod
    def get_music_by_range(cls, start, end):
        return [each for each in Music.objects[start : end]]

    @classmethod
    def get_music_count(cls):
        return Music.objects().count()

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
    music_name = ''
    music_artist = ''
    music_album = ''
    music_genre = ''

    os.system('mid3iconv -q -e GBK "%s"' % (file.encode('utf8')))
    try:
        audio = mutagen.File(file, easy=True)
    except:
        print 'On mutagen.File : %s' % (file)
        traceback.print_exc()
        return music_name, music_artist, music_album, music_genre

    try:
        music_name = audio['title'][0]
    except:
        pass

    try:
        music_artist = audio['artist'][0]
    except:
        pass

    try:
        music_album = audio['album'][0]
    except:
        pass

    try:
        music_genre = audio['genre'][0]
    except:
        pass

    return music_name, music_artist, music_album, music_genre

def _get_random_music():
    num = random.randint(0,Music.objects().count()-1)
    return Music.objects[num]

if __name__ == '__main__':
    # connect('miao_fm', host=MASTER_CDN ,port=MASTER_MONGODB_PORT)
    # try:
    #     MusicSet()
    # except Exception:
    #     pass

    # music = MusicSet.add_music(u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # print music
    # import time
    # time.sleep(10)
    # music = MusicSet.get_music(u'兄妹')
    # print music.play_data
    # print music.local_url

    # MusicSet.del_music(u'兄妹')
    # music = MusicSet.get_music(u'兄妹')
    # print music

    # MusicSet.add_music(u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # for i in range(8):
    #     MusicSet.add_music(u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # print MusicSet.get_music_page_count()
    # print MusicSet.get_music_by_page(1)
    # print MusicSet.get_music_by_page(2)

    # music = MusicSet.get_music(u'兄妹')
    # print music.local_url
    # MusicSet.del_music(u'兄妹')
    # print MusicSet.get_music(u'兄妹')
    # MusicSet.add_music(u'兄妹','eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')

    # music = MusicSet.get_music(u'兄妹')
    # print music.play_data

    # print MusicSet.get_next_music()

    # MusicSet.add_music(u'兄妹','eason',u'/media/823E59BF3E59AD43/Music/01兄妹.mp3')
    # music = MusicSet.get_music(u'兄妹')
    # print music.play_data
    # music.update("dsdsds")
    # print music.play_data

    # print MusicSet.get_music_page_count()

    list_dirs = os.walk('/media/823E59BF3E59AD43/Music/')
    for root, dirs, files in list_dirs: 
        for f in files: 
            if os.path.join(root, f).endswith('.mp3'):
                print os.path.join(root, f)
                for each in _get_info_from_id3(os.path.join(root, f)):
                    print each.encode('utf8')
                    pass
                print
    
    # for each in _get_info_from_id3('/media/823E59BF3E59AD43/Music/mariah carey - without you - 玛丽亚凯莉 失去你.mp3'):
    #     print each
    # for each in _get_info_from_id3('/media/823E59BF3E59AD43/Music/01兄妹.mp3'):
    #     print each



    # print MusicSet.add_music('/media/823E59BF3E59AD43/Music/buckle up n chuggeluck heaven.mp3')
    pass
