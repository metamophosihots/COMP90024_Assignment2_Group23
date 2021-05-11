import couchdb
import json


# ignore this for now
def load_json(path):
    with open(path) as file:
        content = json.load(file)
    return content


# this function writes the view document and store into the database
def create_view(db, doc_name, view_name, map_function):
    """
    :param db: the database you want to save to
    :param doc_name: name of the view document
    :param view_name: name of the view
    :param map_function: the map function, need to use mapreduce format
    :return: None, will save the view document to database
    """
    data = {
        "_id": f"_design/{doc_name}",
        "views": {
            view_name: {
                "map": map_function
            }
        },
        "language": "javascript",
        "options": {"partitioned": False}
    }
    # logging.info( f"creating view {design_doc}/{view_name}" )
    db.save(data)


# this is the local couchdb server
couch = couchdb.Server('http://admin:admin@127.0.0.1:5984')
db = couch['test']  # assume databse 'test' already exist

# a sample map function
mapFunction = '''function (doc) {
                      if(doc.retweet_count == 3)
                      emit(doc.user_id, doc);
                    }'''
create_view(db, "python_view", "python_view", mapFunction)
