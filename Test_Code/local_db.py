import couchdb
import json

"""
couch = couchdb.Server('http://admin:admin@127.0.0.1:5984')
db = couch.create('test')
"""
#with open('../tweets_mined.json') as file:
with open('smallTwitter.json') as file:
    jsonfile = json.load(file)

data = jsonfile['tweets']
print(data[3])