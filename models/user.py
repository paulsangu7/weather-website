from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.weather_app
users_collection = db.users


def create_user(username, email, password):
    """Create a new user with hashed password"""
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {
        "username": username,
        "email": email,
        "password": hashed_pw,
        "search_history": []
    }
    users_collection.insert_one(user)
    return user


def find_user_by_email(email):
    """Find user by email"""
    return users_collection.find_one({"email": email})


def validate_user(email, password):
    """Validate login credentials"""
    user = find_user_by_email(email)
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return user
    return None
