#!/usr/bin/env python
#coding:utf8

# mongo config
MONGODB_URL = '127.0.0.1'
MONGODB_PORT = 27017

# admin user
ADMIN_NAME = 'admin'
ADMIN_PASSWORD = 'admin'

# music tag
update_tag_thresh_day = 30  # days

import os
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]

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

def config():
    import mongoengine
    print 'Configing MongoDB...'
    try:
        mongoengine.connect('miao_fm', host=MONGODB_URL ,port=MONGODB_PORT)
        mongoengine.register_connection('miao_fm_cdn', 'miao_fm_cdn', host=MONGODB_URL ,port=MONGODB_PORT)
        print 'add admin user...'
        add_user_admin()
        print 'add demo music...'
        add_demo_music()
    except mongoengine.connection.ConnectionError:
        print 'Error!'
        print 'Can\'t connect to MongoDB!'
        os._exit(-1)
    print 'Finish!'

if __name__ == '__main__':
    config()
