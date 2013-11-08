#!/usr/bin/env python
#coding:utf8
import datetime
import os
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]
MASTER_CONFIG = ABS_PATH+'/master_config.py'

demo_config = '''
# mongo config
MONGODB_URL = '127.0.0.1'
MONGODB_PORT = 27017

# admin user
ADMIN_NAME = 'admin'
ADMIN_PASSWORD = 'admin'

# music tag
update_tag_thresh_day = 30  # days
update_tag_thresh_random = 10  # days
# random the update day if the music upload in one day
# range it to `update_tag_thresh_day +
#   random.randint(-update_tag_thresh_random, update_tag_thresh_random)`

import os
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]
'''


def gen_config():
    with open(MASTER_CONFIG, 'w') as f:
        f.write(demo_config)


def add_user_admin():
    from user.model import UserSet
    user = UserSet.get_user_by_name(ADMIN_NAME)
    if user:
        user.update_info(ADMIN_PASSWORD)
        user.update_level('admin')
    else:
        user = UserSet.add_user(ADMIN_NAME, ADMIN_PASSWORD, 'admin')


def add_demo_music():
    from music.model import MusicSet
    music = MusicSet.get_music_by_name('To Be With You')
    if not music:
        MusicSet.add_music(ABS_PATH+'/demo.mp3', ADMIN_NAME)


def update_init_status():
    from scheduler import update_all
    update_all()


def config():
    import mongoengine
    print '[config] start', datetime.datetime.now()
    try:
        mongoengine.connect('miao_fm', host=MONGODB_URL, port=MONGODB_PORT)
        mongoengine.register_connection('miao_fm_cdn', 'miao_fm_cdn', host=MONGODB_URL, port=MONGODB_PORT)
    except mongoengine.connection.ConnectionError:
        print '[Error] Can\'t connect to MongoDB!'
        os._exit(-1)
    print '[user] add admin...'
    add_user_admin()
    print '[music] add demo music...'
    add_demo_music()
    print '[status] gen init status...'
    update_init_status()
    print '[config] finish', datetime.datetime.now()

if __name__ == '__main__':
    try:
        from master_config import *
    except ImportError:
        gen = raw_input('Can\'t find `master_config.py`.Do you want to generate it?(y/n) ')
        gen = gen.lower()
        if gen in ['y', 'yes']:
            gen_config()
            print '`master_config.py` generated, Please edit it & retry this config!'
        exit(0)
    config()
    print 'Config success! Please run `main.py` & visit http://localhost:8000/'
