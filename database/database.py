import pymongo, os
import motor.motor_asyncio
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids

async def full_userbase1():
    user_ids = []
    async for doc in user_data.find():
        user_ids.append(doc['_id'])
    return user_ids

async def add_banned_user(user_id: int):
    user_data.update_one({'_id': user_id}, {'$set': {'banned': True}}, upsert=True)
    return

async def remove_banned_user(user_id: int):
    user_data.update_one({'_id': user_id}, {'$unset': {'banned': ''}})
    return

async def list_banned_users():
    banned_users = user_data.find({'banned': True})
    return [user['_id'] for user in banned_users]

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return
