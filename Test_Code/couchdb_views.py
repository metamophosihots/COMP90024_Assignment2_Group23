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
food_list = config["food"]

couch = couchdb.Server(login_info)
user_db = connect_db(user_db_name, couch)
twitter_db = connect_db(twitter_db_name, couch)
stats_db = connect_db(stats_db_name, couch)

# start to write views for user database
timeline_dic = {}
follower_dic = {}
location_dic = {}

for city in city_list:
    map_timeline = 'function (doc) { if(doc.location == "' + city \
                   + '" && doc.timeline_extracted == "0")  emit(doc._id, doc.location);}'
    timeline_dic[city] = {"map": map_timeline}

    map_follower = 'function (doc) { if(doc.location == "' + city \
                   + '" && doc.follower_extracted == "0" && (doc.rank == "0" || doc.rank == "1"))' + \
                   ' emit(doc._id, doc.rank);}'
    follower_dic[city] = {"map": map_follower}

for instance in ["0", "1"]:
    map_location = 'function (doc) {if ((!doc.location) && doc.instance == "' + instance \
                   + '") { emit(doc._id, null); }}'
    location_dic[instance] = {"map": map_location}

write_view(user_db, 'timeline', timeline_dic)
write_view(user_db, 'follower', follower_dic)
write_view(user_db, 'location', location_dic)

scenario1_dic = {}
scenario2_dic = {}
scenario3_dic = {}

map_1_total = 'function (doc) { if(doc.location) emit(doc.location, 1);}'
scenario1_dic['total'] = {"map": map_1_total, "reduce": "_sum"}

map_1_food = 'function (doc) { if(doc.keyword) emit(doc.location, 1);}'
scenario1_dic['food'] = {"map": map_1_food, "reduce": "_sum"}

map_1_count = "function (doc) { if(doc.location && doc.keyword) { doc.keyword.forEach(function (word) {emit([doc.location, word.trim()], 1);});}}"
map_1_polarity =  "function (doc) { if(doc.location && doc.keyword) { doc.keyword.forEach(function (word) {emit([doc.location, word.trim()], doc.polarity);});}}"
scenario1_dic['count'] = {"map": map_1_count, "reduce": "_sum"}
scenario1_dic['polarity'] = {"map": map_1_polarity, "reduce": "_sum"}

map_2_total = "function (doc) { if (doc.year >= 2020) emit([doc.location, doc.date], 1);}"
map_2_total_polarity = "function (doc) { if (doc.year >= 2020) emit([doc.location, doc.date], doc.polarity);}"
map_2_food = "function (doc) { if (doc.keyword && doc.year >= 2020) emit([doc.location, doc.date], 1);}"
map_2_food_polarity = "function (doc) { if (doc.keyword && doc.year >= 2020) emit([doc.location, doc.date], doc.polarity);}"

scenario2_dic['total'] = {"map": map_2_total, "reduce": "_sum"}
scenario2_dic['total_polarity'] = {"map": map_2_total_polarity, "reduce": "_sum"}
scenario2_dic['food'] = {"map": map_2_food, "reduce": "_sum"}
scenario2_dic['food_polarity'] = {"map": map_2_food_polarity, "reduce": "_sum"}

map_3_total = "function (doc) { if (doc.hour) emit([doc.location, doc.year, doc.hour], 1);}"
map_3_total_polarity = "function (doc) { if (doc.hour) emit([doc.location, doc.year, doc.hour], doc.polarity);}"
map_3_food = "function (doc) { if (doc.keyword && doc.hour) emit([doc.location, doc.year, doc.hour], 1);}"
map_3_food_polarity = "function (doc) { if (doc.keyword && doc.hour) emit([doc.location, doc.year, doc.hour], doc.polarity);}"

scenario3_dic['total'] = {"map": map_3_total, "reduce": "_sum"}
scenario3_dic['total_polarity'] = {"map": map_3_total_polarity, "reduce": "_sum"}
scenario3_dic['food'] = {"map": map_3_food, "reduce": "_sum"}
scenario3_dic['food_polarity'] = {"map": map_3_food_polarity, "reduce": "_sum"}


write_view(twitter_db, 'scenario1', scenario1_dic)
write_view(twitter_db, 'scenario2', scenario2_dic)
write_view(twitter_db, 'scenario3', scenario3_dic)


# just test to see if the view can produce some result
print('now print the count of each food mentioned in each city')
count = twitter_db.view('scenario1/count', group=True)
for row in count:
    print(row.key, row.value)

print('now print the polarity of each type of food in each city')
polarity = twitter_db.view('scenario1/polarity', group=True)
for row in polarity:
    print(row.key, row.value)

print('now print the total number of tweets in each city')
total = twitter_db.view('scenario1/total', group=True)
for row in total:
    print(row.key, row.value)

print('now print the total number of tweets that mentioned any food words in each city')
food_mentioned = twitter_db.view('scenario1/food', group=True)
for row in food_mentioned:
    print(row.key, row.value)


print('now print the total number of tweets that mentioned any food words in each city by each date')
food_mentioned = twitter_db.view('scenario2/food', group=True)
for row in food_mentioned:
    print(row.key, row.value)

