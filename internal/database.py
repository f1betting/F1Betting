from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.database import Database


class BettingDatabase:
    client: MongoClient
    database: Database

    def connect(self):
        config = dotenv_values(".env")

        self.client = MongoClient(config["DB_URI"])
        self.database = self.client[config["DB_NAME"]]
        print("Connected to the MongoDB database!")

    def shutdown(self):
        self.client.close()

    def get_database(self):
        return self.database


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonDatabase(BettingDatabase, metaclass=Singleton):
    pass


database = SingletonDatabase()
database.connect()

db = database


def get_database():
    return database.database
