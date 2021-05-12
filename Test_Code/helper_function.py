import couchdb

# functions to add into differnt documents

"""
sample of user document in couchdb:
{"_id": str,
"location": string of one of five cities
"timeline_extract": string: 0 or 1
"priority": string: 0 or 1 or 2 (maybe change another name other than priority)
}

priority:
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


def update_follower_extracted(database, user_id, priority):
    doc = database[str(user_id)]
    doc['priority'] = str(priority+1)
    database[str(user_id)] = doc


def update_timeline_extracted(database, user_id):
    doc = database[str(user_id)]
    doc['timeline_extracted'] = '1'
    database[str(user_id)] = doc


# this function writes the view document and store into the database
def write_view(database, doc_name, view_dic):
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


def get_15_user_timeline(city, database):
    view = database.view(f'timeline/{city}', limit=15).rows
    if len(view) == 0:
        return view
    else:
        user_list = []
        for row in view:
            user_list.append(int(row.key))
        return user_list


def get_15_user_follower(city, database):
    view = database.view(f'follower/{city}', limit=15).rows
    if len(view) == 0:
        return view
    else:
        user_list = []
        for row in view:
            user_list.append([int(row.key), int(row.value)])
        return user_list


# following is the corrent set up of couchdb
couch = couchdb.Server('http://admin:admin@127.0.0.1:5984')
user_db = couch['user']

#write the views
view_dic_timeline = {'Melbourne': {'map': 'function (doc) {\n  if(doc.location == "Melbourne" && doc.timeline_extracted == "0")\n  emit(doc._id, doc.location);\n}'}}
view_dic_follower = {'Melbourne': {'map': 'function (doc) {\n  if(doc.location == "Melbourne" && (doc.priority == "0" || doc.priority == "1"))\n  emit(doc._id,doc.priority);\n}'}}
write_view(user_db, 'timeline', view_dic_timeline)
write_view(user_db, 'follower', view_dic_follower)


user_list_timeline = get_15_user_timeline('Melbourne', user_db)
user_list_follower = get_15_user_follower('Melbourne', user_db)

print(len(user_list_follower))
print(len(user_list_timeline))