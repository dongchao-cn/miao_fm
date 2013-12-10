#! /usr/bin/env python
#coding=utf-8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import json
import datetime
from mongoengine import *
from master_config import MONGODB_URL, MONGODB_PORT

from music.model import MusicSet
from user.model import UserSet
from report.model import ReportSet


class Status(Document):
    '''
    store status info
    '''
    status_gen_date = DateTimeField()
    status_music = DictField()
    status_user = DictField()

    meta = {
        'ordering': ['-status_gen_date']
    }

    def to_dict(self):
        ret = super(Status, self).to_json()
        ret = json.loads(ret)
        # replace status_music.played list
        for i in range(len(self.status_music['played'])):
            ret['status_music']['played'][i][0] = self.status_music['played'][i][0].to_dict()

        # replace status_music.favourite list
        for i in range(len(self.status_music['favourite'])):
            ret['status_music']['favourite'][i][0] = self.status_music['favourite'][i][0].to_dict()

        # replace status_music.weekly_favourite list
        for i in range(len(self.status_music['weekly_favourite'])):
            ret['status_music']['weekly_favourite'][i][0] = self.status_music['weekly_favourite'][i][0].to_dict()

        # replace status_user.listened list
        for i in range(len(self.status_user['listened'])):
            ret['status_user']['listened'][i][0] = self.status_user['listened'][i][0].to_dict()

        # replace status_user.favour list
        for i in range(len(self.status_user['favour'])):
            ret['status_user']['favour'][i][0] = self.status_user['favour'][i][0].to_dict()
        return ret

    def _gen_music_status(self):
        # calc total_count
        self.status_music['total_count'] = MusicSet.get_music_count()

        # calc played_count
        self.status_music['played_count'] = 0
        for music in MusicSet.get_all_music():
            self.status_music['played_count'] += music.music_played

        # calc played list
        sorted_music = sorted(MusicSet.get_all_music(), key=lambda x: x.music_played, reverse=True)
        self.status_music['played'] = [[music, music.music_played] for music in sorted_music][:100]

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
        self.status_music['favourite'] = [[MusicSet.get_music(each[0]), each[1]] for each in favourite][:100]

        # calc 1 week favour list
        weekly_favourite = {}
        users = UserSet.get_all_user()
        for user in users:
            for music in user.user_favour_log:
                try:
                    weekly_favourite[music] += 1
                except:
                    weekly_favourite[music] = 1
        weekly_favourite = sorted(weekly_favourite.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        self.status_music['weekly_favourite'] = [[MusicSet.get_music(each[0]), each[1]] for each in weekly_favourite][:100]

    def _gen_user_status(self):
        # calc total_count
        self.status_user['total_count'] = UserSet.get_user_count()

        # calc listened list
        sorted_user = sorted(UserSet.get_all_user(), key=lambda x: x.user_listened, reverse=True)
        self.status_user['listened'] = [[user, user.user_listened] for user in sorted_user][:100]

        # calc favour list
        sorted_user = sorted(UserSet.get_all_user(), key=lambda x: len(x.user_favour), reverse=True)
        self.status_user['favour'] = [[user, len(user.user_favour)] for user in sorted_user][:100]

    def gen_all_status(self):
        self.status_gen_date = datetime.datetime.now()
        self._gen_music_status()
        self._gen_user_status()
        self.save()

    def get_brief_status(self):
        self.status_music['favourite'] = self.status_music['favourite'][:10]
        self.status_music['weekly_favourite'] = self.status_music['weekly_favourite'][:10]
        self.status_music['played'] = self.status_music['played'][:10]
        self.status_user['listened'] = self.status_user['listened'][:10]
        self.status_user['favour'] = self.status_user['favour'][:10]


def gen_status():
    '''gen all status'''
    status = Status()
    status.gen_all_status()
    return status


def gc():
    '''Garbage Collection, exec it before gen_status and others'''
    for music in MusicSet.get_all_music():
        music.gc()
    for user in UserSet.get_all_user():
        user.gc()
    for report in ReportSet.get_all_report():
        report.gc()

if __name__ == '__main__':
    connect('miao_fm', host=MONGODB_URL, port=MONGODB_PORT)
    gc()
    status = gen_status()
    print status.status_gen_date
    print status.status_music
    print status.status_user
