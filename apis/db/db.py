import pymongo
from pymongo import MongoClient

def get_database():
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["FindYourJob"]
        return db

    except pymongo.errors.ConnectionError as e:
        print("Could not connect to MongoDB:", e)
        return None

# Optional: Export the collection directly if needed
def get_collection(collection_name):
    db = get_database()
    if db is not None:  # Explicitly check if db is not None
        return db[collection_name]
    else:
        print(f"Failed to get the collection: {collection_name}")
        return None
