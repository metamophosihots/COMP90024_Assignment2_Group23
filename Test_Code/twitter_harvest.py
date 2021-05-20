import tweepy.error
import twitter_miner
import json
import couchdb
import re
import random
import time


SEARCH_FOLLOWER_A_TIME = 15
SEARCH_TIMELINE_A_TIME = 125
SEARCH_LOCATION_A_TIME = 900
MAX_PAGE = 8
SLEEP_TIME = 900


def send_data_to_db(database, data_list):
    if len(data_list) > 0:
        for item in data_list:
            if item["_id"] not in database:
                try:
                    database.save(item)
                except couchdb.http.ResourceConflict:
                    continue


# transfer user location to one of the cities in interest
# if use is not in the city list, return empty string
def location_to_city(user_location):
    location = ""
    city_name_list = ["melbourne", "sydney", "perth", "brisbane", "adelaide"]
    for city in city_name_list:
        if re.search(city.lower(), user_location.lower()):
            location = city.lower()
    return location


# this function will pop up users that have not been searched for timeline
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
        elif type == "location":
            for row in view:
                user_info = {'id': int(row.key)}
                user_list.append(user_info)
        return user_list


def update_follower_extracted(database, user_id):
    doc = database[str(user_id)]
    doc['follower_extracted'] = '1'
    database[str(user_id)] = doc


def update_timeline_extracted(database, user_id):
    doc = database[str(user_id)]
    doc['timeline_extracted'] = '1'
    database[str(user_id)] = doc


def update_location(database, user_id, location):
    doc = database[str(user_id)]
    doc['location'] = location
    database[str(user_id)] = doc


# read configuration from the config json file
with open('config_harvest.json') as file:
    config = json.load(file)

food_keyword = config["food_keyword"]

# set up miner to harvest tweets
account_info = config['account_info']
miner = twitter_miner.TwitterMiner(account_info, 200, food_keyword)

#set the up the number of instance of this program
instance = int(config['instance'])


# set up city list and geo code to search
city_list = config['city_list']
city_name_list = []
city_geocode_dict = {}
for city in city_list:
    city_name_list.append(city['city_name'])
    city_geocode_dict[city['city_name']] = city['geo_code']

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

print('start to search for twitters for the first list of user ids using search API')
# get the original twitters
# going to change to stream to keep getting twitter and extract user_id
search_tweets_list = []
for food_name in food_keyword:
    for city_name in city_name_list:
        search_tweets_list = search_tweets_list + miner.mineSearchTweets(food_name, city_geocode_dict[city_name])

# get the original twitters' author and check location
one_user = {}
for twitter in search_tweets_list:
    location = twitter['user_location']
    if location is not None:
        location = location_to_city(location)
        if not location == "":
            user_id = str(twitter['user_id'])
            one_user = {'_id': user_id, 'location': location, 'timeline_extracted': '0',
                        "follower_extracted": "0", "instance": instance, 'rank': '0'}
            if user_id not in user_db:
                try:
                    user_db.save(one_user)
                except couchdb.http.ResourceConflict:
                    continue
#print('finish search for the original twitters and keep only the users with correct location')

# start tweets harvest using author's followers with their timelines
# unsearched_user = True
while True:
    # for city_this_loop in city_name_list:
    # first determine for this loop which city user to search
    city_this_loop = random.choice(city_name_list)
    print('the city of interest for this instance is:', city_this_loop)
    # ask couchdb for user profile as a dictionary, amount is 15 users
    # (or less if there is no un-searched user left)
    # one item of follower list will be {'id': int, 'rank': int}

    print('start to search for user followers, save their id to db without checking location')
    follower_search_user_list = get_user_from_db(city_this_loop, user_db, 'follower', SEARCH_FOLLOWER_A_TIME)
    while len(follower_search_user_list) > 0:
        user = follower_search_user_list.pop(0)
        mined_followers_list = miner.mineUserFollowers(user["id"])
        # after extract his follower, update this user to follower_extracted status
        try:
            update_follower_extracted(user_db, str(user["id"]))
        except couchdb.http.ResourceConflict:
            continue

        if len(mined_followers_list) > 0:
            follower_rank = str(int(user["rank"]) + 1)
            for follower in mined_followers_list:
                follower_dic = {"_id": str(follower), "instance": instance, "follower_extracted": "0",
                                "timeline_extracted": "0", "rank": follower_rank}
                if str(follower) not in user_db:
                    try:
                        user_db.save(follower_dic)
                    except couchdb.http.ResourceConflict:
                        continue

    # ask couch db for user_id that has not confirmed location, amount is 900 users
    print('start to check the location of followers, 900 a time')
    check_profile_user_list = get_user_from_db(instance, user_db, 'location', SEARCH_LOCATION_A_TIME)
    while len(check_profile_user_list) > 0:
        one_user = check_profile_user_list.pop(0)
        user_location = ''
        try:
            user_location = miner.get_user_location(int(one_user["id"]))
        except tweepy.error.TweepError:
            continue
        user_location = location_to_city(user_location)
        try:
            if user_location == "":
                update_location(user_db, one_user['id'], 'other')
            else:
                update_location(user_db, one_user["id"], user_location)
        except couchdb.http.ResourceConflict:
            continue

    print('finish searching for followers, start to extract user time line, 25 users a time')
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
        # update the status of this user to timeline already extracted
        try:
            update_timeline_extracted(user_db, user["id"])
        except couchdb.http.ResourceConflict:
            continue
    print('finish extracting timeline, save to twitter_db and rest for 900 seconds')


    time.sleep(SLEEP_TIME)

    check_left = user_db.view(f'check/{instance}', group = True).rows
    if check_left[0].value == 0:
        print('has extracted timeline of all users in the cities, sleep for 3 hours')
        time.sleep(10800)
