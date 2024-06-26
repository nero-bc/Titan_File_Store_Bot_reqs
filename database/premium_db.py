import motor.motor_asyncio
import datetime
from config import DB_NAME, DB_URI2

class Database:
    def __init__(self, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI2)
        self.db = self._client[database_name]
        self.users = self.db.users
        self.groups = self.db.groups

    async def has_premium_access(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                return False
            elif isinstance(expiry_time, datetime.datetime) and datetime.datetime.now() <= expiry_time:
                return True
            else:
                await self.users.update_one({"id": user_id}, {"$set": {"expiry_time": None}})
        return False

    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def get_expired(self, current_time):
        expired_users = []
        async for user in self.users.find({"expiry_time": {"$lt": current_time}}):
            expired_users.append(user)
        return expired_users

    async def remove_premium_access(self, user_id):
        return await self.update_user({"id": user_id, "expiry_time": None})

    async def get_user(self, user_id):
        return await self.users.find_one({"id": user_id})

    async def update_one(self, filter_query, update_data):
        try:
            result = await self.users.update_one(filter_query, update_data)
            return result.matched_count == 1
        except Exception as e:
            print(f"Error updating document: {e}")
            return False

db1 = Database(DB_NAME)
