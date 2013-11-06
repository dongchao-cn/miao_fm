#! /usr/bin/env python
#coding=utf-8
import datetime
from mongoengine import *
from master_config import MONGODB_URL, MONGODB_PORT

from music.model import MusicSet

connect('miao_fm', host=MONGODB_URL ,port=MONGODB_PORT)

class Status(Document):
    '''
    store status info
    '''
    status_gen_date = DateTimeField()
    status_music = DictField()

    def gen_music_status(self):
        self.status_music['total_count'] = MusicSet.get_music_count()

    def gen_all_status(self):
        self.status_gen_date = datetime.datetime.now()
        self.gen_music_status()
        self.save()

def gen_status():
    status = Status()
    status.gen_all_status()
    return status

if __name__ == '__main__':
    status = gen_status()
    print status.status_gen_date
    print status.status_music
