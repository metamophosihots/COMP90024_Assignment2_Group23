import time
import tweepy
import json
import datetime
import re
import couchdb

# read configuration from the config json file
with open('config_stream.json') as file:
    config = json.load(file)

# set up streamer to stream tweets
account_info = config['account_info']
auth = tweepy.OAuthHandler(account_info['consumer_key'], account_info['consumer_secret_key'])
auth.set_access_token(account_info['access_token'], account_info['access_token_secret'])
api_stream = tweepy.API(auth)

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

# complement food list to a full list, here we test with pizza and burger
food_keyword = ['pizza', 'burger']


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
bound_time = datetime.time(21, 57, 0, 0)
project_stream_listener = ProjectStreamListener(bound_time)
project_stream = tweepy.Stream(auth=api_stream.auth, listener=project_stream_listener)


while True:
    if datetime.datetime.now().time().__ge__(bound_time):
        time.sleep(1800)
    else:
        project_stream.filter(track=food_keyword, locations=bounding_box_coordinates)
        processed_tweets = {}
        for each_twitter in project_stream_listener.tweets_list:
            processed_tweets[str(each_twitter['id'])] = {
                'user_id': each_twitter['user']['id'],
                'location': each_twitter['user']['location'],
                'obtain_method': 'stream'
            }
        for tweet_id_key in processed_tweets.keys():
            user_location = processed_tweets[tweet_id_key]['location']
            if user_location is not None:
                for city in city_list:
                    if re.search(city, user_location):
                        processed_tweets[tweet_id_key]['location'] = city

        '''
        # send data to couchdb
        # it should be sent to user database now
        couch = couchdb.Server(login_info)
        db = couch[database_name]
        for each_twitter in project_stream_listener.tweets_list:
        db.save(each_twitter)
        # send data to couchdb
        '''

        '''
        project_stream_listener.clear_tweets_dict()
        time.sleep(1800)
        '''