import tweepy


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
                    'created_at': mined_timeline_twitter['created_at'],
                    'tweet_id': mined_timeline_twitter['id'],
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
                last_twitter_id = mined_twitter['tweet_id']
                twitter_list.append(mined_twitter)
            page += 1

        return twitter_list

    def mineUserFollowers(self, user_id):
        follower_list = self.api.followers_ids(user_id=user_id, count=10)
        follower_list = list(set(follower_list))
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
                    'user_name': twitter['user']['screen_name'],
                    'created_at': twitter['created_at'],
                    'source': twitter['source'],
                }
                last_twitter_id = searched_twitter['tweet_id']
                twitter_list.append(searched_twitter)
            page += 1

        return twitter_list

    def getUserProfile(self, user_id):
        user = self.api.get_user(user_id=user_id)
        return user.location
