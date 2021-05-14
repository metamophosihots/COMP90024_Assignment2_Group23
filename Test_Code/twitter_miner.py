import tweepy
from textblob import TextBlob
import re
from datetime import datetime

class TwitterMiner(object):
    result_limit = 0
    data = []
    api = False
    twitter_developer_account_keys = {
        'consumer_key': '--KEY--',
        'consumer_secret_key': '--KEY--',
        'access_token': '--TOKEN--',
        'access_token_secret': '--TOKEN--'
    }

    def __init__(self, keys_dict, limit, food_keyword):
        self.twitter_developer_account_keys = keys_dict
        auth = tweepy.OAuthHandler(keys_dict['consumer_key'], keys_dict['consumer_secret_key'])
        auth.set_access_token(keys_dict['access_token'], keys_dict['access_token_secret'])
        self.api = tweepy.API(auth)
        self.result_limit = limit
        self.food_keyword = food_keyword


    def mineUserTimeline(self, user_id, user_location, max_pages):
        twitter_list = []
        last_twitter_id = False
        page = 1

        while page <= max_pages:
            if last_twitter_id:
                timeline_result = self.api.user_timeline(user_id=user_id, count=self.result_limit,
                                                         max_id=last_twitter_id - 1, tweet_model='extended',
                                                         include_rts=False)
            else:
                timeline_result = self.api.user_timeline(user_id=user_id, count=self.result_limit,
                                                         tweet_mode='extended', include_rts=False)

            for timeline_tweet in timeline_result:
                mined_timeline_twitter = timeline_tweet._json
                time = self.time_to_iso(mined_timeline_twitter['created_at'])
                mined_twitter = {
                    '_id': mined_timeline_twitter['id_str'],
                    'created_at': time,
                    'user_id': user_id,
                    'location': user_location,
                    "retweet_count": mined_timeline_twitter['retweet_count'],
                    'favorite_count': mined_timeline_twitter['favorite_count'],
                    'coordinates': mined_timeline_twitter['coordinates'],
                    'source_device': mined_timeline_twitter['source']
                }
                try:
                    text = mined_timeline_twitter['full_text']
                except KeyError:
                    text = mined_timeline_twitter['text']
                text, keyword = self.process_text(text)
                polarity = TextBlob(text).sentiment.polarity
                mined_twitter['text'] = text
                mined_twitter['polarity'] = polarity
                if len(keyword) > 0:
                    mined_twitter['keyword'] = keyword
                last_twitter_id = int(mined_twitter['_id'])
                twitter_list.append(mined_twitter)
            page += 1

        return twitter_list

    def mineUserFollowers(self, user_id):
        follower_list = self.api.followers_ids(user_id=user_id, count=200)
        """valid_follower_list = []
        for each_follower_id in follower_list:
            location = self.getUserProfile(user_id=each_follower_id)
            if location is None:
                continue
            else:
                for each_city in city_name_list:
                    if re.search(each_city, location):
                        valid_follower_list.append(id)"""
        return follower_list

    def mineSearchTweets(self, food_name, geo_code):
        twitter_list = []
        last_twitter_id = False
        page = 1
        max_pages = 1

        while page <= max_pages:
            if last_twitter_id:
                search_result = self.api.search(q=food_name, geocode=geo_code, count=15,
                                                max_id=last_twitter_id - 1, entities=True)
            else:
                search_result = self.api.search(q=food_name, geocode=geo_code, count=15, entities=True)

            for search_object in search_result:
                twitter = search_object._json
                searched_twitter = {
                    'tweet_id': twitter['id'],
                    'user_id': twitter['user']['id'],
                    #'user_name': twitter['user']['screen_name'],
                    'user_location': twitter['user']['location'],
                    #'created_at': twitter['created_at'],
                    #'source': twitter['source'],
                }
                last_twitter_id = searched_twitter['tweet_id']
                twitter_list.append(searched_twitter)
            page += 1

        return twitter_list

    def getUserProfile(self, user_id):
        user = self.api.get_user(user_id=user_id)
        return user['location']

    def time_to_iso(self, time_string):
        time = datetime.strptime(time_string, '%a %b %d %H:%M:%S %z %Y')
        time = time.isoformat()
        return time

    def process_text(self, text):
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
        text = text.lower()
        keyword = self.search_keyword(text)
        return text, keyword

    def search_keyword(self, text):
        pattern = "|".join(self.food_keyword)
        keyword = re.findall(pattern, text)
        return keyword

