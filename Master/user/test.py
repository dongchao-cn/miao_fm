#!/usr/bin/env python
#coding=utf-8

from pydelicious import get_popular, get_userposts, get_urlposts
import recommendations
import random

def init_userdata(tag, count = 5):
    user_dict = {}
    print "here"
    for p1 in  get_popular(tag = tag)[0:count]:
        print p1
        for p2 in get_urlposts(p1['url']):
            print p2
            user = p2['user']
            user_dict[user] = {}
    return user_dict

def fillItems(user_dict):
    all_items = {}
    for user in user_dict:
        posts = get_userposts(user)
        for post in posts:
            url = post['url']
            user_dict[user][url] = 1.0
            all_items[url] = 1
    
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item] = 0.0

if __name__ == "__main__":
    
    users = init_userdata(tag='programming')
    print users
    fillItems(users)
    user = users.keys()[random.randint(0, len(users) - 1)]
    print user
    recommendations.getRecommendations(users, user)
     

