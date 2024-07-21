import datetime
import pytz
from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_NAME, DATABASE_URI

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(DATABASE_URI)
        self.db = self.client[DATABASE_NAME]
        self.req = self.db.requests

    async def find_join_req(self, id):
        return bool(await self.req.find_one({'id': id}))

    async def add_join_req(self, id):
        await self.req.insert_one({'id': id})

    async def del_join_req(self):
        await self.req.drop()

db = Database()
