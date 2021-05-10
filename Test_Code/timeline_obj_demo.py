import tweepy

user_id = '4886845565'

account_info = {"consumer_key": "o7frQQjOkrcUUJJYLIuzXltks",
                "consumer_secret_key": "BXPIsvDEif9drOnMveyyIGZhNu58pBjE7uonx0m2EBpyZV8v86",
                "access_token": "1308176095397593089-oCNxwcpMVDc6o3FOTL9hAT24LS5WG0",
                "access_token_secret": "GlnFCkxNOUwxPGDfU4agjqi4FuoWe1wACBbxChtQ6cLGO"}

auth = tweepy.OAuthHandler(account_info['consumer_key'], account_info['consumer_secret_key'])
auth.set_access_token(account_info['access_token'], account_info['access_token_secret'])
api = tweepy.API(auth)
timeline_obj = api.user_timeline(user_id=user_id, count=10, tweet_mode='extended', include_retweets=False)

'''
mined_tweets_list = []
for timeline_tweet in timeline_obj:
    mined_timeline_twitter = timeline_tweet._json
    mined_twitter = {
        'created_at': mined_timeline_twitter['created_at'],
        'tweet_id': mined_timeline_twitter['id'],
        'text': mined_timeline_twitter['full_text'],
        'source_device': mined_timeline_twitter['source'],
        'user_id': mined_timeline_twitter['user']['id'],
        'user_name': mined_timeline_twitter['user']['screen_name'],
        'location': mined_timeline_twitter['user']['location'],
        "retweet_count": mined_timeline_twitter['retweet_count'],
        'obtain_method': 'timeline_mine'
    }
    mined_tweets_list.append(mined_twitter)

for item in mined_tweets_list:
    print(item)
    print('\n')
'''
print(timeline_obj)