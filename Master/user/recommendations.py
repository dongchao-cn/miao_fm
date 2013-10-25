#!/usr/bin/env python
#coding=utf-8
from math import sqrt
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([ pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sqrt(sum_of_squares))

def top_k_matches(prefs, person, k = 10, similarity = sim_distance):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    
    scores.sort()
    scores.reverse()
    return scores[0:k]

def getRecommendations(prefs, person, similarity = sim_distance):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[preson] or prefs[preson] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other] * sim
                simSum[item] += sim
                
    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    ranking.sort()
    ranking.reverse()
    return ranking
        
    
