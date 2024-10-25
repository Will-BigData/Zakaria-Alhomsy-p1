import logging
from pymongo import MongoClient # type: ignore

class MongoDBHandler(logging.Handler):
    def __init__(self, mongo_uri, db_name, collection_name):
        super().__init__()
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def emit(self, record):
        log_entry = self.format(record)
        self.collection.insert_one({"message": log_entry, "level": record.levelname, "timestamp": record.asctime})

def start_logging():
    logger = logging.getLogger("StoreLogger")
    logger.setLevel(logging.INFO)
    mongo_handler = MongoDBHandler("mongodb://localhost:27017/", "store", "logs")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    mongo_handler.setFormatter(formatter)
    logger.addHandler(mongo_handler)
    logger.info("Logging initialized and connected to MongoDB.")
    return logger