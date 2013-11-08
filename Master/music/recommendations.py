#!/usr/bin/env python
#coding=utf-8
if __name__ == "__main__":
    import sys
    sys.path.insert(0, "../")
import random
from math import sqrt
from user.model import UserSet
from model import MusicSet

import mutagen
import mongoengine.errors
from mongoengine import *
from bson.objectid import ObjectId


def generator(M, N):
    ret = []
    for idx in range(0, M):
        if random.random() * M <= N :
            ret.append(idx)
    return ret

def sim_pearson(prefs, user1, user2):
    si = {}
    for tag in prefs[user1]:
        if tag in prefs[user2]:
            si[tag] = 1

    n = len(si)

    if n == 0:
        return 0

    sum_tag_uesr1 = sum([prefs[user1][tag] for tag in si])
    sum_tag_uesr2 = sum([prefs[user2][tag] for tag in si])

    sumsq_tag_user1 = sum([pow(prefs[user1][tag], 2) for tag in si])
    sumsq_tag_user2 = sum([pow(prefs[user2][tag], 2) for tag in si])

    pearson_sum = sum([prefs[user1][tag] * prefs[user2][tag] for tag in si])

    num = pearson_sum - float(sum_tag_uesr1) * sum_tag_uesr2 / n
    den = sqrt((sumsq_tag_user1 - pow(sum_tag_uesr1, 2) / float(n)) * (sumsq_tag_user2 -
        pow(sum_tag_uesr2,2) / float(n)))

    if den == 0:
        return 0
    return num / den

def sim_distance(prefs, user1_id, user2_id):
    si = {}
    for item in prefs[user1_id]:
        if item in prefs[user2_id]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([ pow(prefs[user1_id][item] - prefs[user2_id][item], 2) for item in
        prefs[user1_id] if item in prefs[user2_id]])
    return 1 / (1 + sqrt(sum_of_squares))

def top_k_matches(prefs, user_id, k = 10, similarity = sim_distance):
    scores = [(similarity(prefs, user_id, other), other) for other in prefs if other != user_id]
    scores.sort()
    scores.reverse()
    return scores[0:k]

def transform_prefs(prefs):
    ret = {}
    for user_id in prefs:
        for item in prefs[user_id]:
            ret.setdefault(item, {})

            ret[item][user_id] = prefs[user_id][item]

    return ret

def calc_similarity_matrix(prefs, k = 100):
    ret = {}
    for item_id in prefs:
        scores = top_k_matches(prefs, item_id, k = k, similarity = sim_pearson)
        ret[item_id] = scores
    return ret

class Recommend():

    music_tag_prefs = {}
    user_tags_prefs = {}
    user_music_prefs = {}
    music_mat = {}

    def __init__(self):
        print "init start"
        self.music_tag_prefs = self.get_music_tag_prefs()
        self.user_music_prefs = self.get_user_music_prefs()
        self.user_tags_prefs = self.get_user_tags_prefs()
        self.music_mat = calc_similarity_matrix(self.music_tag_prefs, 100)
        print "init finished"


    def get_music_tag_prefs(self):

        ret = {}
        for music in MusicSet.get_all_music():
            ret.setdefault(str(music.music_id), {})
            for tag, value in music.music_tag.items():
                if tag == "update_datetime":
                    continue
                ret[str(music.music_id)][tag] = music.music_tag[tag]
        return ret

    def get_user_tags_prefs(self):
        '''
        pack the tags prefs in follwing data type:
        {
            user1 : { tag1 : value1 , tag2 : value2},
            user1 : { tag4 : value4 , tag5 : value5}
        }
        '''
        ret = {}
        all_user = UserSet.get_all_user()
        for user in all_user:
            ret.setdefault(str(user.user_id), {})
            for music_id in user.user_favour:
                for tags, value in MusicSet.get_music(music_id).music_tag.items():
                    if tags == "update_datetime":
                        continue
                    ret[str(user.user_id)].setdefault(tags, 0)
                    ret[str(user.user_id)][tags] += self.user_music_prefs[str(user.user_id)][music_id] * value

            for music_id in user.user_dislike:
                for tags, value in MusicSet.get_music(music_id).music_tag.items():
                    if tags == "update_datetime":
                        continue
                    ret[str(user.user_id)].setdefault(tags, 0)
                    ret[str(user.user_id)][tags] += self.user_music_prefs[str(user.user_id)][music_id] * value

        return ret

    def get_user_music_prefs(self):
        '''
        pack the music prefs in follwing data type:
        {
            user1 : { music_id1 : value1 , music_id2 : value2},
            user1 : { music_id3 : value4 , music_id4 : value5}
        }
        '''

        ret = {}
        all_user = UserSet.get_all_user()
        for user in all_user:
            ret.setdefault(str(user.user_id), {})
            for music_id in user.user_favour:
                ret[str(user.user_id)][music_id] = 1
            for music_id in user.user_dislike:
                ret[str(user.user_id)][music_id] = -1
        return ret

    def get_recommendations_with_user_based(self, user_id, similarity = sim_distance):
        totals = {}
        simSums = {}
        for other in self.user_tags_prefs:
            if other == user_id:
                continue
            sim = similarity(self.user_tags_prefs, user_id, other)

            if sim <= 0:
                continue

            for music_id in self.user_music_prefs[other]:
                if music_id not in self.get_user_music_prefs[user_id]:
                    totals.setdefault(music_id, 0)
                    totals[music_id] += self.user_music_prefs[other][music_id] * sim
                    simSums[music_id] += sim

        rankings = [(total / simSums[music_id], music_id) for music_id, total in totals.items() if
                simSums[music_id] != 0]
        rankings.sort()
        rankings.reverse()
        return rankings

    def get_recommendations_with_item_based(self, user_id):
        user_rating = self.user_music_prefs[user_id]
        scores = {}
        total_sim = {}
        for (music_id, rating) in user_rating.items():
            for (similarity, other_music_id) in self.music_mat[music_id]:
                if other_music_id in user_rating:
                    continue
                scores.setdefault(other_music_id, 0)
                scores[other_music_id] += similarity * rating
                total_sim.setdefault(other_music_id, 0)
                total_sim[other_music_id] += similarity
        rankings = [(score / total_sim[music_id], music_id) for music_id, score in scores.items() if
                total_sim[music_id] != 0]
        rankings.sort()
        rankings.reverse()
        return rankings

    def get_musics(self, user_id):
        recommend_algo = self.get_recommendations_with_item_based
        ret = [music_id for (score, music_id) in recommend_algo(user_id)]
        ret.extend([music_id for music_id in UserSet.get_user(user_id).user_favour])
        ret.extend([str(MusicSet.get_music_by_idx(idx).music_id) for idx in
            generator(MusicSet.get_music_count(), 100
            - len(ret))])
        ret = list(set(ret))
        return ret

def user_get_music():
    recom = Recommend()

    for user in UserSet.get_all_user():
        user.remove_all_recommend()
        user.user_recommend.extend(recom.get_musics(user.user_id))
        user.save()
        print recom.get_musics(str(user.user_id))

def get_next_music(user_id):
    pass


if __name__ == '__main__':
    from master_config import MONGODB_URL, MONGODB_PORT
    connect('miao_fm', host=MONGODB_URL ,port=MONGODB_PORT)
    register_connection('miao_fm_cdn', 'miao_fm_cdn', host=MONGODB_URL ,port=MONGODB_PORT)


    user_get_music()


