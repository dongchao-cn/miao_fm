#!/usr/bin/env python
#coding=utf-8
from math import sqrt
from model import UserSet

def get_prefs():
    ret = {}
    all_user = UserSet.get_all_user()
    for user in all_user:
        for music_id in user.user_listened:
            ret.setdefault(user.user_id, {})
            ret[user.user_id][music_id] = 0
        for music_id in user.user_favour:
            ret.setdefault(user.user_id, {})
            ret[user.user_id][music_id] = 1
        for music_id in user.user_dislike:
            ret[user.user_id][music_id] = -1

    return ret

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

        if sim <= 0:
            continue
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

def calc_item_similarity_items(prefs, k = 10):
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
        for (similarity, other_item) in item_mat:
            if other_item in user_rating:
                continue
            scores.setdefault(other_item, 0)
            scores[other_item] += similarity * rating
            total_sim.setdefault(other_item, 0)
            total_sim += similarity
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings

def get_next_musics(user_id, recommend_algo = get_recommendations_with_item_based):
    prefs = get_prefs()
    ret = [music_id for (score, music_id) in recommend_algo(prefs, user_id)]
    return ret

