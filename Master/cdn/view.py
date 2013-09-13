#coding:utf8
import os
import tornado
from .model import CdnControl

class APICdnControlHandler(tornado.web.RequestHandler):
    '''
    get:
        get music range
        list all music by range

    post:
        add a new music

    del:
        del all music
    '''
    def get(self):
        '''
        return base info about music if can't get start or end
        else return music list
        '''
        try:
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
        except:
            base_info = {'total_count':MusicControl.get_music_count()}
            self.write(base_info)
            return
        music_list = MusicControl.get_music_by_range(start, start+count)
        self.write(json.dumps(music_list, cls=MusicJsonEncoder))

    def post(self):
        music_list = []
        for upload_file in self.request.files['file']:
            save_file_path = ABS_PATH + "/uploads/" + upload_file['filename']
            with open(save_file_path, 'w') as f:
                f.write(upload_file['body'])
                music_list.append(MusicControl.add_music(save_file_path, True))
        self.write(json.dumps(music_list, cls=MusicJsonEncoder))

    def delete(self):
        MusicControl.remove_all_music()
        self.write('')

class APICdnHandler(tornado.web.RequestHandler):
    '''
    get:
        get music details

    put:
        update music

    delete:
        delete music
    '''

    def get(self, music_id):
        music = MusicControl.get_music(music_id)
        self.write(json.dumps(music, cls=MusicJsonEncoder))

    def put(self, music_id):
        music_name = self.get_argument("music_name")
        music_artist = self.get_argument("music_artist")
        music_album = self.get_argument("music_album")

        music = MusicControl.get_music(music_id)
        music.update_info(music_name, music_artist, music_album)
        music = MusicControl.get_music(music_id)
        self.write(json.dumps(music, cls=MusicJsonEncoder))

    def delete(self, music_id):
        music = MusicControl.get_music(music_id)
        music.remove()
        self.write('')


class CdnHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("cdn/cdn.html")

# class AddCdnHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("cdn/add_cdn.html", msg=u'新增CDN')

#     def post(self):
#         try:
#             name = self.get_argument("name")
#             assert name
#             url_path = self.get_argument("url_path")
#             assert url_path
#         except:
#             self.render("cdn/add_cdn.html", msg=u'参数填写错误！')
#             return
#         try:
#             CdnControl.add_cdn(name, url_path)
#         except:
#             self.render("cdn/add_cdn.html", msg=u'CDN名已存在！')
#             return
#         self.render("cdn/add_cdn.html", msg=u'新增成功！')
#         return

# class DelCdnHandler(tornado.web.RequestHandler):
#     def get(self):
#         name = self.get_argument("name")
#         CdnControl.del_cdn(name)
#         cdn_list = CdnControl.get_all_cdn()
#         self.render("cdn/cdn.html", msg=u'删除成功！', cdn_list=cdn_list)
#         return