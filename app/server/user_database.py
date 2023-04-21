from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

def db_init():
    load_dotenv()
    CONNECTION_STRING = os.getenv("CONNECTION_STRING")
    client = MongoClient(CONNECTION_STRING)
    db = client['users']
    user_collection=db["user_collection"]
    return user_collection

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "hashed_password": user["hashed_password"],
        "disabled": user["disabled"],
    }

async def get_users() -> dict:
    user_collection = db_init()
    users=[]
    for user in user_collection.find():
        users.append(user_helper(user))
    return users

async def add_user(user_data: dict) -> dict:
    user_collection = db_init()
    already_exists = user_collection.find_one({"username": user_data["username"]})
    if already_exists:
        return None
    user = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def get_user(id: str) -> dict:
    user_collection = db_init()
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)
    
async def change_password(new_password: str, username: str) -> dict:
    user_collection = db_init()
    user = user_collection.find_one({"username":username})
    if user:
        data = {"hashed_password" : new_password}
        new_user = user_collection.update_one({"username":username},{"$set" : data})
        if new_user:
            return True