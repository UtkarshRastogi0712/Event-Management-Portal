from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
client = MongoClient(CONNECTION_STRING)
db = client['EventsDB']
  

project_collection=db["project_collection"]

def project_helper(project) -> dict:
    return {
        "id": str(project["_id"]),
        "name": project["name"],
        "creator": project["creator"],
        "start_date": project["start_date"],
        "description": project["description"],
        "items": project["items"],
        "access": project["access"]
    }

async def get_projects(user: str) -> dict:
    project_list=[]
    for project in project_collection.find():
        if project["creator"]==user or user in project["access"]:
            project_list.append(project_helper(project))
    return project_list

async def add_project(project_data: dict) -> dict:
    project = project_collection.insert_one(project_data)
    new_project = project_collection.find_one({"_id": project.inserted_id})
    return project_helper(new_project)

async def get_project(name: str, user: str) -> dict:
    project = project_collection.find_one({"name": name})
    if project and (project["creator"]==user or user in project["access"]):
        return project_helper(project)

async def update_project(name: str, data: dict, user:str):
    if len(data)<1:
        return False
    project = project_collection.find_one({"name": name})
    if project and (project["creator"]==user or user in project["access"]):
        updated_project = project_collection.update_one({"name": name}, {"$set": data})
        if updated_project:
            return True
        return False

async def delete_project(name: str, user:str):
    project = project_collection.find_one({"name": name})
    if project and (project["creator"]==user or user in project["access"]):
        project_collection.delete_one({"name": name})
        return True
    return False