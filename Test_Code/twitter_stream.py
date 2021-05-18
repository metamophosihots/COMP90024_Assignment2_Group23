import time
import tweepy
import json
import datetime
import re
import couchdb
from Test_Code.twitter_harvest import get_user_from_db

# transfer user location to one of the cities in interest
# if use is not in the city list, return empty string


def location_to_city(user_location, city_name_list):
    location = ""
    for city in city_name_list:
        if re.search(city.lower(), user_location.lower()):
            location = city
    return location

def update_location(database, user_id, location):
    doc = database[str(user_id)]
    doc['location'] = location
    database[str(user_id)] = doc

# read configuration from the config json file
with open('config_stream.json') as file:
    config = json.load(file)

# set up streamer to stream tweets
account_info = config['account_info']
auth = tweepy.OAuthHandler(account_info['consumer_key'], account_info['consumer_secret_key'])
auth.set_access_token(account_info['access_token'], account_info['access_token_secret'])
api = tweepy.API(auth)

# set up city list and geo code to search
bounding_box_coordinates = config['bounding_box']
city_list = config['city_name_list']

# Adelaide: 138.45,-35.04,138.7489,-34.7175
# Perth: 115.6325,-32.5417,116.0558,-31.6625
# Sydney: 150.83,-33.9486,151.2917,-33.8167
# Brisbane: 153.7031,27.7942,153.3964,-27.1439


# set up the corresponding database log in info
login_info = config['couchdb_info']['login_url']
database_name = config['couchdb_info']['database_name']

# set up the food list to search as key word
food_keyword = config["food_keywords"]

# set up the corresponding database log in info
login_info = config['couchdb_info']['login_url']
user_db_name = config['couchdb_info']['database_name'][0]
twitter_db_name = config['couchdb_info']['database_name'][1]

# connect to couchdb
couch = couchdb.Server(login_info)
user_db = couch[user_db_name]
twitter_db = couch[twitter_db_name]


class ProjectStreamListener(tweepy.StreamListener):

    tweets_list = []

    def __init__(self, threshold_time):
        super(ProjectStreamListener, self).__init__()
        # test code
        self.save_file = open('tweets_streamed_original.json', 'w')
        # test code
        self.tweets_list = []
        self.upperbound_time = threshold_time

    def on_data(self, tweet):
        if datetime.datetime.now().time().__le__(self.upperbound_time):
            self.tweets_list.append(json.loads(tweet))
            self.save_file.write(str(tweet))
            return True
        else:
            self.save_file.close()
            return False

    def on_error(self, status):
        print(status)
        return True

    def clear_tweets_dict(self):
        self.tweets_list = []




# bound time could be changed to satisfy demand
bound_time = datetime.time(23, 45, 0, 0)
start_time = datetime.time(21, 0, 0, 0)
#city_name_list = ['Melbourne', 'Sydney', 'Brisbane', 'Perth', 'Adelaide']
project_stream_listener = ProjectStreamListener(bound_time)
project_stream = tweepy.Stream(auth=api.auth, listener=project_stream_listener)

# suppose this is the core for 1
INSTANCE = 1
SEARCH_LOCATION_A_TIME = 900
city_name_list = ["melbourne", "sydney", "perth", "brisbane", "adelaide"]

another_round = True
while another_round:

    while datetime.datetime.now().time().__ge__(start_time):
        if datetime.datetime.now().time().__ge__(bound_time):
            time.sleep(900)
        else:
            project_stream.filter(track=food_keyword, locations=bounding_box_coordinates)
            processed_tweets = []
            for each_twitter in project_stream_listener.tweets_list:
                processed_twitter = {
                    "_id": str(each_twitter["id"]),
                    'user_id': each_twitter['user']['id'],
                    'location': each_twitter['user']['location']
                }
                processed_tweets.append(processed_twitter)
            for tweets in processed_tweets:
                user_id = tweets['user_id']
                location = location_to_city(tweets['user_location'], city_name_list)
                if str(user_id) not in user_db and location is not "":
                    follower_dic = {"_id": str(user_id), "location": location, "follower_extracted": "0",
                                    "timeline_extracted": "0", "rank": "0", "instance": INSTANCE}
                    user_db.save(follower_dic)
