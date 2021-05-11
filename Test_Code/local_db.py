import couchdb
import json


# ignore this for now
def load_json_file(path):
    with open(path) as file:
        content = json.load(file)
        data = content['tweets']
    return data


# this function writes the view document and store into the database
def create_view(db, doc_name, view_dic):
    """
    :param db: the database you want to save to
    :param doc_name: name of the view document
    :param view_dic: dictionary of all the views you want to add, key = viewname, value = map function
    """
    data = {
        "_id": f"_design/{doc_name}",
        "views": view_dic,
        "language": "javascript",
        # "options": {"partitioned": False}
    }
    # logging.info( f"creating view {design_doc}/{view_name}" )
    db.save(data)


# this function updates a view document when the document already exist and you know the document name
def update_view(db, doc_name, new_view_dic):
    """
    :param db: the database you want to save to
    :param doc_name: name of the view document that already exist
    :param view_name: name of the view
    :param map_function: the map function, need to use mapreduce format
    :return: None, will update the view document to database
    """
    origin = db[f"_design/{doc_name}"]
    origin['views'] = new_view_dic
    db[f"_design/{doc_name}"] = origin


# this is the local couchdb server
couch = couchdb.Server('http://admin:admin@127.0.0.1:5984')
db = couch['test']  # assume datbase 'test' already exist
"""
# read the sample tweets file tweets_mined and save them to local couchdb
sample = load_json_file('../tweets_mined.json')
for tweet in sample:
    db.save(tweet)

# a sample map function --ignore this for now
mapFunction = '''function (doc) {
                      if(doc.retweet_count == 3)
                      emit(doc.user_id, doc);
                    }'''
"""

# a sample view dictionary
view_dic = {'view': {'map': 'function (doc) {\n  if(doc.retweet_count == 3)\n  emit(doc._id, doc);\n}'}}
view_dic2 = {'view_1': {'map': 'function (doc) {\n  if(doc.location == "Melbourne")\n  emit(doc.created_at, doc.location);\n}'}}

# create this view
create_view(db, "python_view", view_dic)

# update_view(db, "python_view", "updated_python_view", mapFunction)
# if you get the document using the ducument id, you are getting an class obejct
# access the object attributes directly
sample_view = db['_design/python_view']
print(sample_view.id)
print(sample_view['views'])

# how to update a document/a view document
# change on the class object directly using the function
# need to define a new view dictionary first
update_view(db, 'python_view', view_dic2)

# now access the view result
test = db.view('python_view/view_1')
# test is <class 'couchdb.client.ViewResults'>
for row in test:
    print(row.key, row.value)

