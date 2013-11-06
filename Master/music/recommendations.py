#!/usr/bin/env python
#coding=utf-8
import random
from math import sqrt
from user.model import UserSet
from model import MusicSet

def get_music_tag_prefs():
    ret = {}
    for music in MusicSet.get_all_music():
        ret[music.music_id] = music.music_tag
    return ret

def get_tags_prefs(music_prefs):
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
        ret.setdefault(user.user_id, {})
        for music_id in user.user_favour:
            for tags, value in MusicSet.get_music(music_id).music_tag.items():
                if tags == "update_datetime":
                    continue
                ret[user.user_id].setdefault(tags, 0)
                ret[user.user_id] += music_prefs[user.user_id][music_id] * value

        for music_id in user.user_dislike:
            for tags, value in MusicSet.get_music(music_id).music_tag.items():
                if tags == "update_datetime":
                    continue
                ret[user.user_id].setdefault(tags, 0)
                ret[user.user_id] += music_prefs[user.user_id][music_id] * value

    return ret

def get_music_prefs():
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
        ret.setdefault(user.user_id, {})
        for music_id in user.user_favour:
            ret[user.user_id][music_id] = 1
        for music_id in user.user_dislike:
            ret[user.user_id][music_id] = -1
    return ret

def sim_pearson(prefs, user1, user2):
    si = {}
    for tag in prefs[user1]:
        if tag in prefs[user2]:
            si[tag] = 1

    n = len(si)

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

def get_recommendations_with_user_based(prefs, user_id, similarity = sim_distance):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == user_id:
            continue
        sim = similarity(prefs, user_id, other)

        for item in prefs[other]:
            if item not in prefs[user_id] or prefs[user_id] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other] * sim
                simSums[item] += sim

    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def transform_prefs(prefs):
    ret = {}
    for user_id in prefs:
        for item in prefs[user_id]:
            ret.setdefault(item, {})

            ret[item][user_id] = prefs[user_id][item]

    return ret

def calc_item_similarity_items(prefs, k = 50):
    ret = {}
    item_prefs = transform_prefs(prefs)
    for item in item_prefs:
        scores = top_k_matches(item_prefs, item, k = k, similarity = sim_distance)
        ret[item] = scores
    return ret

def get_recommendations_with_item_based(prefs, user_id):
    user_rating = prefs[user_id]
    scores = {}
    total_sim = {}
    item_mat = calc_item_similarity_items(prefs)
    for (item, rating) in user_rating.items():
        for (similarity, other_item) in item_mat[item]:
            print other_item
            if other_item in user_rating:
                continue
            scores.setdefault(other_item, 0)
            scores[other_item] += similarity * rating
            total_sim.setdefault(other_item, 0)
            total_sim[other_item] += similarity
    rankings = [(score / total_sim[item], item) for item, score in scores.items() if total_sim[item]
            != 0]
    rankings.sort()
    rankings.reverse()
    return rankings

def generator(M, N):
    ret = []
    for idx in range(0, M):
        if random.random() * M <= N :
            ret.append(idx)
    return ret

def get_musics(user_id, recommend_algo = get_recommendations_with_item_based):
    prefs = get_music_prefs()
    ret = [music_id for (score, music_id) in recommend_algo(prefs, user_id)]
    ret.extend([music_id for music_id in UserSet.get_user(user_id).user_favour])
    ret.extend([MusicSet.get_music_by_idx(idx).music_id for idx in generator(MusicSet.get_music_count(), 50
        - len(ret))])
    ret = list(set(ret))
    return ret

def get_next_music(user_id):
    if user_id is None:
        return MusicSet.get_music_by_idx(random.randint(0, MusicSet.get_music_count() - 1))
    music_id_list = get_musics(user_id)
    return MusicSet.get_music(music_id_list[random.randint(0, len(music_id_list) - 1)])
