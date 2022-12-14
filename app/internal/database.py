import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database


# Database class using MongoDB
class BettingDatabase:
    # pylint: disable=too-few-public-methods
    client: MongoClient
    database: Database

    def __init__(self):
        load_dotenv()

        self.client = MongoClient(os.getenv("DB_URI"))
        self.database = self.client[os.getenv("DB_NAME")]
        print("Connected to the MongoDB database!")


# Create database instance
db = BettingDatabase()

# Expose database variable
database = db.database
