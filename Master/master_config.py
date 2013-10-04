#!/usr/bin/env python
#coding:utf8

# set SERVER and MASTER_CDN to one machine
SERVER = 'xdfm.com'
MASTER_CDN = 'cdn.xdfm.com'

MASTER_MONGODB_PATH = '/data/mongo_db'
MASTER_MONGODB_PORT = 6867

# admin user
ADMIN_NAME = 'admin'
ADMIN_PASSWORD = 'admin'

# DON'T EDIT BELOW
import os
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]

def master_nginx_config():
    server_config = '''
upstream master_stream {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name %s;

    # Allow file uploads
    client_max_body_size 100M;

    location /static/ {
        alias %s;
        if ($query_string) {
            expires max;
        }
    }
    
    location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://master_stream;
    }
}
''' % (SERVER, ABS_PATH+'/static/')

    master_cdn_config = '''

server {
    listen 80;
    server_name %s;

    location /music_file/ {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://master_stream;
    }
}
''' % (MASTER_CDN)

    config = server_config + master_cdn_config
    with open('master_nginx.conf','w') as f:
        f.write(config)

def master_mongodb_config():
    master_mongodb_dir = '%s/master' % (MASTER_MONGODB_PATH)
    log_path = '%s/mongod.log' % (master_mongodb_dir)
    config = '''
master = true
fork = true
dbpath = %s
port = %d
logpath = %s
logappend = true
nojournal = true
rest = true''' % (master_mongodb_dir, MASTER_MONGODB_PORT, log_path)
    try:
        if not os.path.exists(master_mongodb_dir):
            os.makedirs(master_mongodb_dir)
    except OSError:
        print 'Can\'t mkdir "%s", check permission!' % (master_mongodb_dir)
        os._exit(-1)
    with open('master_mongodb.conf','w') as f:
        f.write(config)

def add_master_cdn():
    from cdn.model import CdnControl
    cdn = CdnControl.get_cdn_by_name("master")
    if cdn:
        cdn.remove()
    CdnControl.add_cdn("master", MASTER_CDN, True)

def add_demo_music():
    from music.model import MusicControl
    music = MusicControl.get_music_by_name('To Be With You')
    if music:
        music.remove()
    MusicControl.add_music(ABS_PATH+'/demo.mp3')

def add_user_admin():
    from user.model import UserControl
    user = UserControl.get_user_by_name(ADMIN_NAME)
    if user:
        user.remove()
    UserControl.add_user(ADMIN_NAME, ADMIN_PASSWORD)

def config():
    import mongoengine
    mongoengine.connect('miao_fm', host=MASTER_CDN ,port=MASTER_MONGODB_PORT)
    print 'generate nginx config...'
    master_nginx_config()
    print 'generate mongodb config...'
    master_mongodb_config()
    try:
        print 'add master cdn...'
        add_master_cdn()
        print 'add admin user...'
        add_user_admin()
        print 'add demo music...'
        add_demo_music()
    except mongoengine.connection.ConnectionError:
        print 'MongoDB NOT started!!!'
        print 'Please use "mongod -f %s/master_mongodb.conf" to start MongoDB.' % (ABS_PATH)
        print 'And check %s, %s DNS settings.' % (SERVER,MASTER_CDN)
        print 'Then re execute this file.'
        os._exit(-1)
    print 'Finish!'
    print 'Please include "%s/master_nginx.conf" in nginx.conf.' % (ABS_PATH)
    print 'Then visit http://%s/admin/ for admin page.' % (SERVER)

if __name__ == '__main__':
    config()
