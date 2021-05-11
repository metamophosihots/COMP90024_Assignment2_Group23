import couchdb


class DBhelper(object):
    city_list = []
    food_list = []
    general_food_list = []
    db_name = ['user', 'twitter']

    def __init__(self, city_list, food_list):
        self.city_list = city_list
        self.food_list = food_list

    def setup(self, couch):
        for db in self.db_name:
            if db not in couch:
                couch.create(db)


    def gen_view(self):
        view_list = []
        return view_list





# set up the views of user_db database
#create_view(user_db, 'city', view_city)
