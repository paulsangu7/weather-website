from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.weather_app
users_collection = db.users

def create_user(username, email, password):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_pw,
        "search_history": []
    })

def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def validate_user(email, password):
    user = find_user_by_email(email)
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return user
    return None
