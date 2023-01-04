import pymongo
from transformer.constant.database import DATABASE_NAME,MONGODB_URL_KEY

MONGODB_URL_KEY = "mongodb+srv://vaasu:pcvaasu9dps@cluster0.wydi0u7.mongodb.net/?retryWrites=true&w=majority"


class MongoDBClient:
    def __init__(self,) -> None:
        try:
            self.client = pymongo.MongoClient(MONGODB_URL_KEY)
            self.database_name = DATABASE_NAME

        except Exception as e:
            raise e
