#!/usr/bin/env python
#coding:utf8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import random
import json
from mongoengine import *
from bson.objectid import ObjectId
from master_config import MASTER_CDN, MASTER_MONGODB_PORT

connect('miao_fm', host=MASTER_CDN ,port=MASTER_MONGODB_PORT)

class CdnJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cdn):
            return { 'cdn_id' : obj.cdn_id,
                'name' : obj.name,
                'url_path' : obj.url_path,
                'online' : obj.online}
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)

class Cdn(Document):
    '''
    store cdn info
    '''
    name = StringField(max_length=100,unique=True)
    url_path = StringField(max_length=50)
    online = BooleanField(default=False)

    def __str__(self):
        return ('%s' % (self.name)).encode('utf-8')

    @property
    def cdn_id(self):
        return self.pk

    @property
    def url(self):
        '''
        get url
        '''
        return self.url_path

    def update_info(self, name, url_path, online=False):
        '''
        update cdn info
        '''
        self.name = name
        self.url_path = url_path
        self.online = online
        self.save()

    def remove(self):
        '''
        del cdn from db
        '''
        self.delete()

class CdnControl(object):
    '''
    CDN control functions
    '''

    def __init__(self):
        raise Exception,'CdnControl can\'t be __init__'

    @classmethod
    def add_cdn(cls, name, url_path, online=False):
        '''
        add new cdn
        '''
        return Cdn(name, url_path, online).save()

    @classmethod
    def get_cdn(cls, cdn_id):
        '''
        get cdn
        '''
        try:
            return Cdn.objects(pk=cdn_id).first()
        except ValidationError:
            return None

    @classmethod
    def get_cdn_by_name(cls, name):
        '''
        get cdn
        '''
        try:
            return Cdn.objects(name=name).first()
        except ValidationError:
            return None

    @classmethod
    def get_all_cdn(cls):
        '''
        get all cdn
        '''
        return Cdn.objects()

    @classmethod
    def remove_all_cdn(cls):
        '''
        del all cdn
        '''
        for cdn in Cdn.objects():
            cdn.remove()

    @classmethod
    def get_free_cdn(cls):
        '''
        get free cdn
        '''
        assert Cdn.objects().count() != 0
        return _get_random_cdn()

    @classmethod
    def get_cdn_by_range(cls, start, end):
        '''
        get cdn by range
        '''
        return [each for each in Cdn.objects[start : end]]

    @classmethod
    def get_cdn_count(cls):
        '''
        get cdn count
        '''
        return Cdn.objects().count()


def _get_random_cdn():
    '''
    get random cdn
    '''
    online_cdn = [cdn for cdn in Cdn.objects() if cdn.online]
    num = random.randint(0, len(online_cdn)-1)
    return online_cdn[num]

if __name__ == '__main__':
    CdnControl.remove_all_cdn()
    CdnControl.add_cdn("xidian1",'cdn1.xidian.com')
    CdnControl.add_cdn("xidian2",'cdn2.xidian.com')
    print CdnControl.get_all_cdn()
    CdnControl.get_all_cdn()[0].remove()
    print CdnControl.get_all_cdn()