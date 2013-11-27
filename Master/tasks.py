import os
import subprocess
from celery import Celery
from mongoengine import *

from music.model import MusicSet
from master_config import MONGODB_URL, MONGODB_PORT

app = Celery('tasks', broker='mongodb://%s:%d' % (MONGODB_URL, MONGODB_PORT))
connect('miao_fm', host=MONGODB_URL, port=MONGODB_PORT)
register_connection('miao_fm_cdn', 'miao_fm_cdn', host=MONGODB_URL, port=MONGODB_PORT)


@app.task
def _lame_mp3(infile, music_id, remove=False):
    '''
    lame the mp3 to smaller
    '''
    outfile = infile+'.tmp'
    subprocess.call([
        "lame",
        "--quiet",
        "--mp3input",
        "--abr",
        "64",
        infile,
        outfile])
    music = MusicSet.get_music(music_id)
    if music:
        music.update_file(outfile)
    os.remove(outfile)

    if remove:
        os.remove(infile)
