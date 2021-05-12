import tweepy.error
import twitter_miner
import time
import json
import couchdb
import re


def sendDataToCouchDB(database, tweets):
    for tweet in tweets:
        if tweet["_id"] not in database:
            database.save(tweet)


# connect to different database in couchdb. If already exist, connect, otherwise create a new database to connect
def connect_db(db_name, couch):
    if db_name in couch:
        db = couch[db_name]
    else:
        db = couch.create(db_name)
    return db


# transfer user location to one of the cities in interest
# if use is not in the city list, return empty string
def location_to_city(user_location, city_name_list):
    location = ""
    for city in city_name_list:
        if re.search(city.lower(), user_location.lower()):
            location = city
    return location


# this function writes the view document and store into the database
def create_view(database, doc_name, view_dic):
    """
    :param db: the database you want to save to
    :param doc_name: name of the view document
    :param view_dic: dictionary of all the views you want to add, key = viewname, value = map function
    """
    if f"_design/{doc_name}" in database:
        view = database[f"_design/{doc_name}"]
        view['views'] = view_dic
        database[f"_design/{doc_name}"] = view
    else:
        view = {
            "_id": f"_design/{doc_name}",
            "views": view_dic,
            "language": "javascript",
            # "options": {"partitioned": False}
        }
        # logging.info( f"creating view {design_doc}/{view_name}" )
        database.save(view)


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
user_db = connect_db(user_db_name, couch)
twitter_db = connect_db(twitter_db_name, couch)




# this part need to be reworked after new implementation
view_melb_user = {'melb': {'map': 'function (doc) {\n  if(doc.location == "Melbourne" && doc.timeline_extracted == "0")\n  emit(doc._id, doc.from_stream);\n}'}}
# you may have to write several view of users for Adelaide, Perth.....
create_view(user_db, 'by_city', view_melb_user)
# this part need to be reworked after new implementation





# complement food list to a full list, here we test with pizza and burger
food_keyword = ['pizza', 'burger']


# so this part is not useful anymore, we get all users id from stream api?

# get the original twitters
# going to change to stream to keep getting twitter and extract user_id
search_tweets_list = []
for food_name in food_keyword:
    for city_name in city_name_list:
        search_tweets_list = search_tweets_list + miner.mineSearchTweets(food_name, city_geocode_dict[city_name])

# get the original twitters' author and deduplicate
one_user = {}
for twitter in search_tweets_list:
    location = location_to_city(twitter['user_location'], city_name_list)
    if location is not None:
        user_id = str(twitter['user_id'])
        one_user = {'_id': user_id, 'location': location,
                    'location_confirmed': "1", 'timeline_extracted': '0', 'round_number': 0}
        if user_id not in user_db:
            user_db.save(one_user)
time.sleep(300)

# This part may need to be re-writen for multi-cities and this should be in a while loop
# double dictionary
user_melb_list = user_db.view('by_city/melb', limit=15)
search_id_list = []
for row in user_melb_list:
    search_id_list.append(int(row.key))


# start tweets harvest using author's followers with their timelines
while True:
    # ask couchdb for user profile as a dictionary, amount is 15 users
    follower_search_user_list = [1, 2]
    if len(follower_search_user_list) == 0:
        time.sleep(1800)
        # ask couchdb for user profile as a dictionary, check the amount
        check_list = [1, 2]
        if len(check_list) == 0:
            break

    for user in follower_search_user_list:
        mined_followers_list = miner.mineUserFollowers(user["_id"])
        if len(mined_followers_list) > 0:
            round_number = int(user["round_number"]) + 1
            for follower in mined_followers_list:
                if str(follower) not in user_db:
                    follower_dic = {"_id": str(follower), "location": "Melbourne", "location_confirmed": '0',
                                    "timeline_extracted": "0", "round_number": round_number}
                    user_db.save(follower_dic)

    # ask couchdb for user profile as a dictionary, amount is 125 users
    # max pages for timeline search is 8 pages
    timeline_search_user_list = [1, 2]
    timeline_tweets = []
    for user in timeline_search_user_list:
        try:
            mined_timeline_tweets = miner.mineUserTimeline(user["_id"], 1)
            timeline_tweets = timeline_tweets + mined_timeline_tweets
        except tweepy.error.TweepError:
            continue
    # send the timeline tweets to the couchdb
    sendDataToCouchDB(twitter_db, timeline_tweets)

    # change the user_ids that has been searched to status 1
    for user in timeline_search_user_list:
        user_doc = user_db[user["_id"]]
        user_doc['timeline_extracted'] = "1"
        user_doc[str(id)] = user_doc

    time.sleep(900)