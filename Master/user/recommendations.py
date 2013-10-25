#!/usr/bin/env python
#coding=utf-8
from math import sqrt
from model import UserSet

def get_prefs():
    ret = {}
    all_user = UserSet.get_all_user()
    for user in all_user:
        for music_id in user.user_listened:
            ret.setdefault(user, {})
            ret[user][music_id] = 0
        for music_id in user.user_favour:
            ret.setdefault(user, {})
            ret[user][music_id] = 1
        for music_id in user.user_dislike:
            ret[user][music_id] = -1

    return ret

def sim_distance(prefs, user1, user2):
    si = {}
    for item in prefs[user1]:
        if item in prefs[user2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([ pow(prefs[user1][item] - prefs[user2][item], 2) for item in prefs[user1] if item in prefs[user2]])
    return 1 / (1 + sqrt(sum_of_squares))

def top_k_matches(prefs, user, k = 10, similarity = sim_distance):
    scores = [(similarity(prefs, user, other), other) for other in prefs if other != user]
    scores.sort()
    scores.reverse()
    return scores[0:k]

def get_recommendations_with_user_based(prefs, user, similarity = sim_distance):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == user:
            continue
        sim = similarity(prefs, user, other)

        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[user] or prefs[user] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other] * sim
                simSums[item] += sim

    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def transform_prefs(prefs):
    ret = {}
    for user in prefs:
        for item in prefs[user]:
            ret.setdefault(item, {})

            ret[item][user] = prefs[user][item]

    return ret

def calc_item_similarity_items(prefs, k = 10):
    ret = {}
    item_prefs = transform_prefs(prefs)
    for item in item_prefs:
        scores = top_k_matches(item_prefs, item, k = k, similarity = sim_distance)
        ret[item] = scores
    return ret

def get_recommendations_with_item_based(prefs, user):
    user_rating = prefs[user]
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

def get_next_musics(user, recommend_algo = get_recommendations_with_item_based):
    prefs = get_prefs()
    ret = [music_id for (score, music_id) in recommend_algo(prefs, user)]
    return ret

