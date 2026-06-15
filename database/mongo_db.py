from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["polyglot_document_db"]

def get_mongo_db():
    """Returns the active MongoDB database instance."""
    return db
