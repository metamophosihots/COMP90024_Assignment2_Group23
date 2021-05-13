import tweepy.error
import twitter_miner
import time
import json
import couchdb
import re
import random

INSTANCE = '1'
SEARCH_FOLLOWER_A_TIME = 15
SEARCH_TIMELINE_A_TIME = 125
MAX_PAGE = 8


def send_data_to_db(database, data_list):
    for item in data_list:
        if item["_id"] not in database:
            database.save(item)


# transfer user location to one of the cities in interest
# if use is not in the city list, return empty string
def location_to_city(user_location, city_name_list):
    location = ""
    for city in city_name_list:
        if re.search(city.lower(), user_location.lower()):
            location = city
    return location


# this function will pop up up to 15 users that have not been searched for timeline
def get_user_from_db(city, database, type, amount):
    view = database.view(f'{type}/{city}', limit=int(amount)).rows
    if len(view) == 0:
        return view
    else:
        user_list = []
        if type == "timeline":
            for row in view:
                user_info = {'id': int(row.key), 'location': row.value}
                user_list.append(user_info)
        elif type == "follower":
            for row in view:
                user_info = {'id': int(row.key), 'rank': int(row.value)}
                user_list.append(user_info)
        return user_list


# read configuration from the config json file
with open('config_harvest.json') as file:
    config = json.load(file)

# set up miner to harvest tweets
account_info = config['account_info']
miner = twitter_miner.TwitterMiner(account_info, 60)

# set up city list and geo code to search
city_list = config['city_list']
city_name_list = []
city_geocode_dict = {}
location_list = []
for city in city_list:
    city_name_list.append(city['city_name'])
    city_geocode_dict[city['city_name']] = city['geo_code']
    location_list = location_list + city['location']

# Adelaide: -34.8917,138.6033,16km
# Perth: -32.0117,115.3986,60km
# Sydney: -33.8917,151.0708,20km
# Brisbane: -27.5125,153.0136,32km

# set up the corresponding database log in info
login_info = config['couchdb_info']['login_url']
user_db_name = config['couchdb_info']['database_name'][0]
twitter_db_name = config['couchdb_info']['database_name'][1]

# connect to couchdb
couch = couchdb.Server(login_info)
user_db = couch[user_db_name]
twitter_db = couch[twitter_db_name]

# complement food list to a full list, here we test with pizza and burger
food_keyword = ['pizza', 'burger']

# get the original twitters
# going to change to stream to keep getting twitter and extract user_id
search_tweets_list = []
for food_name in food_keyword:
    for city_name in city_name_list:
        search_tweets_list = search_tweets_list + miner.mineSearchTweets(food_name, city_geocode_dict[city_name])

# get the original twitters' author and check location
one_user = {}
for twitter in search_tweets_list:
    location = location_to_city(twitter['user_location'], city_name_list)
    if not location == "":
        user_id = str(twitter['user_id'])
        one_user = {'_id': user_id, 'location': location, 'timeline_extracted': '0',
                    "follower_extracted": "0", "instance": INSTANCE, 'rank': 0}
        if user_id not in user_db:
            user_db.save(one_user)
time.sleep(300)
"""
# This part may need to be re-writen for multi-cities and this should be in a while loop
# double dictionary
user_melb_list = user_db.view('by_city/melb', limit=15)
search_id_list = []
for row in user_melb_list:
    search_id_list.append(int(row.key))
"""

# start tweets harvest using author's followers with their timelines
unsearched_user = True
while unsearched_user:

    # first determine for this loop which city user to search
    city_this_loop = random.choice(city_name_list)
    # ask couchdb for user profile as a dictionary, amount is 15 users
    # (or less if there is no un-searched user left)
    # one item of follower list will be {'id': int, 'rank': int}
    follower_search_user_list = get_user_from_db(city_this_loop, user_db, 'follower', SEARCH_FOLLOWER_A_TIME)
    while len(follower_search_user_list) > 0:
        user = follower_search_user_list.pop(0)
        mined_followers_list = miner.mineUserFollowers(user["id"])
        if len(mined_followers_list) > 0:
            follower_rank = str(int(user["rank"]) + 1)
            for follower in mined_followers_list:
                follower_dic = {"_id": str(follower), "instance": INSTANCE, "follower_extracted": "0",
                                "timeline_extracted": "0", "rank": follower_rank}
                if str(follower) not in user_db:
                    user_db.save(follower_dic)

    # ask couchdb for user profile as a dictionary, amount is 125 users
    # max pages for timeline search is 8 pages
    # one user dic in the list is formatted as: {"id": int, "location": str}
    timeline_search_user_list = get_user_from_db(city_this_loop, user_db, 'timeline', SEARCH_TIMELINE_A_TIME)
    while len(timeline_search_user_list) > 0:
        timeline_tweets = []
        user = timeline_search_user_list.pop(0)
        try:
            mined_timeline_tweets = miner.mineUserTimeline(user["id"], user['location'], MAX_PAGE)
            timeline_tweets = timeline_tweets + mined_timeline_tweets
        except tweepy.error.TweepError:
            continue
        # send the timeline tweets to the couchdb
        send_data_to_db(twitter_db, timeline_tweets)

    # change the user_ids that has been searched to status 1
    for user in timeline_search_user_list:
        user_doc = user_db[user["_id"]]
        user_doc['timeline_extracted'] = "1"
        user_doc[str(id)] = user_doc

    time.sleep(900)
