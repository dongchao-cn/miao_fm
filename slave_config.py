#coding:utf8

# set MASTER_CDN
MASTER_CDN = 'cdn.xdfm.com'
MASTER_MONGODB_PORT = 6867

SLAVE_CDN = 'cdn1.xdfm.com'
SLAVE_MONGODB_PATH = '/data/mongo_db'
SLAVE_MONGODB_PORT = 7090

# DON'T EDIT BELOW
import os
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]

def slave_nginx_config():
    config = '''
server {
    listen 80;
    server_name %s;

    location /music_file/ {
        gridfs miao_fm_cdn;
        mongo 127.0.0.1:%d;
    }
}
''' % (SLAVE_CDN, SLAVE_MONGODB_PORT)
    with open('slave_nginx.conf','w') as f:
        f.write(config)

def slave_mongodb_config():
    slave_mongodb_dir = '%s/slave' % (SLAVE_MONGODB_PATH)
    config = '''
slave = true
dbpath = %s
source = %s:%d
port = %d
oplogSize = 64
slavedelay = 10
only = miao_fm_cdn
autoresync = true
nojournal = true''' % (slave_mongodb_dir, MASTER_CDN, MASTER_MONGODB_PORT, SLAVE_MONGODB_PORT)
    try:
        if not os.path.exists(slave_mongodb_dir):
            os.makedirs(slave_mongodb_dir)
    except OSError:
        print 'Can\'t mkdir "%s", check permission!' % (slave_mongodb_dir)
        os._exit(-1)
    with open('slave_mongodb.conf','w') as f:
        f.write(config)

def main():
    print 'generate nginx config...'
    slave_nginx_config()
    print 'generate mongodb config...'
    slave_mongodb_config()
    print 'Finish!'
    print 'Please include "%s/server_nginx.conf" in nginx.conf and restart nginx.' % (ABS_PATH)
    print 'Please use "mongod -f slave_mongodb.conf" to start MongoDB.'

if __name__ == '__main__':
    main()
