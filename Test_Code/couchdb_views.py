import couchdb
import json

# connect to different database in couchdb.
# If already exist, connect, otherwise create a new database to connect
def connect_db(db_name, couch):
    if db_name in couch:
        db = couch[db_name]
    else:
        db = couch.create(db_name)
    return db


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
            "language": "javascript"
        }
        database.save(view)


with open('config_couchdb.json') as file:
    config = json.load(file)

login_info = config['login_url']
user_db_name = config['database_name'][0]
twitter_db_name = config['database_name'][1]
stats_db_name = config['database_name'][2]
city_list = config["city"]

couch = couchdb.Server(login_info)
user_db = connect_db(user_db_name, couch)
twitter_db = connect_db(twitter_db_name, couch)
stats_db = connect_db(stats_db_name, couch)
empty = connect_db('empty', couch)

# start to write views for user database
timeline_dic = {}
follower_dic = {}
for city in city_list:
    map_timeline = 'function (doc) {\n  if(doc.location == ' + city \
                   + ' && doc.timeline_extracted == "0")\n  emit(doc._id, doc.location);\n}'
    timeline_dic[city] = {"map": map_timeline}

    map_follower = 'function (doc) {\n  if(doc.location == ' + city \
                   + ' && doc.follower_extracted == "0" && (doc.rank == "0" || doc.rank == "1"))' + \
                   '\n  emit(doc._id, doc.rank);\n}'
    follower_dic[city] = {"map": map_follower}

write_view(empty, 'timeline', timeline_dic)
write_view(empty, 'follower', follower_dic)

location_dic = {}
for instance in ["0", "1", "2"]:
    map_location = 'function (doc) {if ((!doc.location) && doc.instance == ' + instance \
                   + ') { emit(doc._id, doc.instance); }}'
    location_dic[instance] = {"map": map_location}
write_view(empty, 'location', location_dic)



