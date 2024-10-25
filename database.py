from pymongo import MongoClient # type: ignore
from logger import start_logging # type: ignore
from pymongo.errors import ConnectionFailure # type: ignore

logger = start_logging()

def connect(): 
    try:
        client = MongoClient('mongodb://localhost:27017/')
        client.admin.command('ismaster')
        logger.info("MongoDB connection successful.")
        return client['store']
    except ConnectionFailure:
        logger.error(f"MongoDB connection failed: {e}")
        print("MongoDB connection failed.")