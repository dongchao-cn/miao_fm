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

# connect('miao_fm', host='127.0.0.1' ,port=MASTER_MONGODB_PORT)

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
        return self.url_path

    def update_info(self, name, url_path, online=False):
        self.name = name
        self.url_path = url_path
        self.online = online
        self.save()

    def remove(self):
        self.delete()

class CdnSet(object):
    '''
    CDN control functions
    '''

    def __init__(self):
        raise Exception,'CdnSet can\'t be __init__'

    @classmethod
    def add_cdn(cls, name, url_path, online=False):
        return Cdn(name, url_path, online).save()

    @classmethod
    def get_cdn(cls, cdn_id):
        try:
            return Cdn.objects(pk=cdn_id).first()
        except ValidationError:
            return None

    @classmethod
    def get_cdn_by_name(cls, name):
        try:
            return Cdn.objects(name=name).first()
        except ValidationError:
            return None

    @classmethod
    def get_all_cdn(cls):
        return Cdn.objects()

    @classmethod
    def remove_all_cdn(cls):
        for cdn in Cdn.objects():
            cdn.remove()

    @classmethod
    def get_free_cdn(cls):
        assert Cdn.objects().count() != 0
        return _get_random_cdn()

    @classmethod
    def get_cdn_by_range(cls, start, end):
        return [each for each in Cdn.objects[start : end]]

    @classmethod
    def get_cdn_count(cls):
        return Cdn.objects().count()


def _get_random_cdn():
    online_cdn = [cdn for cdn in Cdn.objects() if cdn.online]
    num = random.randint(0, len(online_cdn)-1)
    return online_cdn[num]

if __name__ == '__main__':
    CdnSet.remove_all_cdn()
    CdnSet.add_cdn("xidian1",'cdn1.xidian.com')
    CdnSet.add_cdn("xidian2",'cdn2.xidian.com')
    print CdnSet.get_all_cdn()
    CdnSet.get_all_cdn()[0].remove()
    print CdnSet.get_all_cdn()