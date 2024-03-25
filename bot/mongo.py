import pymongo

class MongoConnect(object):

    def __init__(self) -> None:
        self.connect_recipes= self.connect_recipes()

    def connect_recipes(self):
        return pymongo.MongoClient("mongodb://localhost:27017/")
    
    def insert_recipes(self, page, document):
        # Access a specific database
        recipe_db = self.connect_recipes["gordon_recipes"]
        # Access a specific collection within the database
        collection = recipe_db[page]
        collection.insert_one(document)



