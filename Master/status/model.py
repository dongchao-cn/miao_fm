#! /usr/bin/env python
#coding=utf-8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import datetime
from mongoengine import *
from master_config import MONGODB_URL, MONGODB_PORT

from music.model import MusicSet
from user.model import UserSet

class Status(Document):
    '''
    store status info
    '''
    status_gen_date = DateTimeField()
    status_music = DictField()

    meta = {
        'ordering': ['-status_gen_date']
    }

    def _gen_music_status(self):
        # calc total_count
        self.status_music['total_count'] = MusicSet.get_music_count()

        # calc played_count
        self.status_music['played_count'] = 0
        for music in MusicSet.get_all_music():
            self.status_music['played_count'] += music.music_played

        # calc played list
        sorted_music = sorted(MusicSet.get_all_music(), key=lambda x: x.music_played, reverse=True)
        self.status_music['played'] = [(music, music.music_played) for music in sorted_music]

        # calc favourite list
        favourite = {}
        users = UserSet.get_all_user()
        for user in users:
            for music in user.user_favour:
                try:
                    favourite[music] += 1
                except:
                    favourite[music] = 1
        favourite = sorted(favourite.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        self.status_music['favourite'] = [(MusicSet.get_music(each[0]), each[1]) for each in favourite]

    def gen_all_status(self):
        self.status_gen_date = datetime.datetime.now()
        self._gen_music_status()
        self.save()

    def get_brief_status(self):
        self.status_music['favourite'] = self.status_music['favourite'][:10]

def gen_status():
    connect('miao_fm', host=MONGODB_URL ,port=MONGODB_PORT)
    status = Status()
    status.gen_all_status()
    return status

if __name__ == '__main__':
    status = gen_status()
    print status.status_gen_date
    print status.status_music
