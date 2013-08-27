#coding:utf8

# set SERVER and MASTER_CDN to one machine
SERVER = 'xdfm.com'
MASTER_CDN = 'cdn1.xdfm.com'

# how many items in one page (for admin pages)
ITEM_PER_PAGE = 10


# DON'T EDIT BELOW
import os
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]

def generate_nginx_config():
    server_config = '''
upstream frontends {
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
        proxy_pass http://frontends;
    }
}
''' % (SERVER, ABS_PATH+'/static/')

    master_cdn_config = '''

server {
    listen 80;
    server_name %s;

    location /music_file/ {
        gridfs miao_fm;
    }
}
''' % (MASTER_CDN)

    config = server_config + master_cdn_config
    with open('server_nginx.config','w') as f:
        f.write(config)

def add_master_cdn():
    from cdn.model import CdnControl
    import mongoengine
    try:
        CdnControl.add_cdn("master",MASTER_CDN)
    except mongoengine.NotUniqueError:
        pass


def add_demo_music():
    from music.model import MusicControl
    import mongoengine
    try:
        MusicControl.add_music(ABS_PATH+'/demo.mp3')
    except mongoengine.NotUniqueError:
        pass

def main():
    print 'generate nginx config...'
    generate_nginx_config()
    print 'add master cdn...'
    add_master_cdn()
    print 'add demo music...'
    add_demo_music()
    print 'Finish!'
    print 'Please set %s, %s DNS settings.' % (SERVER,MASTER_CDN)
    print 'Please include "%s/server_nginx.config" in nginx.conf.' % (ABS_PATH)
    print 'and visit http://%s/admin/ for admin page.' % (SERVER)

if __name__ == '__main__':
    main()
