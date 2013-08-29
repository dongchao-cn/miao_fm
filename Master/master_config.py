#coding:utf8

# set SERVER and MASTER_CDN to one machine
SERVER = 'xdfm.com'
MASTER_CDN = 'cdn.xdfm.com'

# how many items in one page (for admin pages)
ITEM_PER_PAGE = 10

MASTER_MONGODB_PATH = '/data/mongo_db'
MASTER_MONGODB_PORT = 6867

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
    client_max_body_size 50M;

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
    config = '''
master = true
dbpath = %s
oplogSize = 64
port = %d
nojournal = true''' % (master_mongodb_dir, MASTER_MONGODB_PORT)
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
    import mongoengine
    cdn = CdnControl.get_cdn("master")
    if cdn:
        CdnControl.del_cdn("master")
    CdnControl.add_cdn("master",MASTER_CDN)

def add_demo_music():
    from music.model import MusicControl
    import mongoengine
    music = MusicControl.get_music_by_name('To Be With You')
    if music:
        MusicControl.del_music(music.music_id)
    MusicControl.add_music(ABS_PATH+'/demo.mp3')

def main():
    print 'generate nginx config...'
    master_nginx_config()
    print 'generate mongodb config...'
    master_mongodb_config()
    print 'add master cdn...'
    add_master_cdn()
    print 'add demo music...'
    add_demo_music()
    print 'Finish!'
    print 'Please set %s, %s DNS settings.' % (SERVER,MASTER_CDN)
    print 'Please include "%s/server_nginx.conf" in nginx.conf.' % (ABS_PATH)
    print 'and visit http://%s/admin/ for admin page.' % (SERVER)

if __name__ == '__main__':
    main()
