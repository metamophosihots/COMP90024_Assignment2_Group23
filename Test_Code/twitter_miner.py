import tweepy
import re


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

    def __init__(self, keys_dict, limit):
        self.twitter_developer_account_keys = keys_dict
        auth = tweepy.OAuthHandler(keys_dict['consumer_key'], keys_dict['consumer_secret_key'])
        auth.set_access_token(keys_dict['access_token'], keys_dict['access_token_secret'])
        self.api = tweepy.API(auth)
        self.result_limit = limit

    # need to rewrite
    def mineUserTimeline(self, user_id, max_pages):
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
                mined_twitter = {
                    '_id': str(mined_timeline_twitter['id']),
                    'created_at': mined_timeline_twitter['created_at'],
                    'source_device': mined_timeline_twitter['source'],
                    'user_id': mined_timeline_twitter['user']['id'],
                    'user_name': mined_timeline_twitter['user']['screen_name'],
                    'location': mined_timeline_twitter['user']['location'],
                    "retweet_count": mined_timeline_twitter['retweet_count'],
                    'favorite_count': mined_timeline_twitter['favorite_count'],
                    'coordinates': mined_timeline_twitter['coordinates'],
                    'obtain_method': 'timeline_mine'
                }
                try:
                    mined_twitter['text'] = mined_timeline_twitter['full_text']
                except KeyError:
                    mined_twitter['text'] = mined_timeline_twitter['text']
                last_twitter_id = mined_twitter['_id']
                twitter_list.append(mined_twitter)
            page += 1

        return twitter_list

    def mineUserFollowers(self, user_id, city_name_list):
        follower_list = self.api.followers_ids(user_id=user_id, count=10)
        valid_follower_list = []
        for each_follower_id in follower_list:
            location = self.getUserProfile(user_id=each_follower_id)
            if location is None:
                continue
            else:
                for each_city in city_name_list:
                    if re.search(each_city, location):
                        valid_follower_list.append(id)
        return valid_follower_list

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
