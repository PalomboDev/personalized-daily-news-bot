class NewsMongoDBClient:

    def __init__(self, mongodb_client, mongodb_database, mongodb_collection):
        self.mongodb_client = mongodb_client
        self.mongodb_database = mongodb_database
        self.mongodb_collection = mongodb_collection

    def insert_article(self, article):
        self.mongodb_collection.insert_one(article.__dict__)

    def get_unused_articles(self):
        return self.mongodb_collection.find({"used": False})

    def set_unused_articles(self, boolean=True):
        for a in self.get_unused_articles():
            a_copy = a.copy()
            a_copy["used"] = boolean
            self.mongodb_collection.replace_one(a, a_copy)

    # def get_unused_articles(self):
    #     pass
