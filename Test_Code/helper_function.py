import couchdb

# functions to add into differnt documents

"""
sample of user document in couchdb:
{"_id": str,
"location": string of one of five cities #only have this if the location is checked
"timeline_extracted": string: 0 or 1
"follower_extracted": string: 0 or 1
"instance": string 0 or 1, depends on which instance find this user id first, suppose 2 instances
"rank": string: 0 or 1 or 2 (maybe change another name other than rank)
}

if a user has not been check the location, it has no location attribute

rank:
0 means from original search api or from stream
1 means the follower of original user
2 means the follower of follower

how to update priority:
view will return you a list of list: [[user_id, priority],....] (all int format)
after extract follower of on user_id, priority + 1
e.g.
update_follower_extracted(database, user_id, priority)

how to update timeline_extracted:
view will return you a list of user id only: [user_id,....] (int format)
after extract the time line, update the original document
e.g.
update_timeline_extracted(database, user_id)
"""

# following is the corrent set up of couchdb
couch = couchdb.Server('http://admin:admin@127.0.0.1:5984')
user_db = couch['user']