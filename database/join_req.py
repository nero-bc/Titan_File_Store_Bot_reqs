import datetime
import pytz
from motor.motor_asyncio import AsyncIOMotorClient
from config import DB_NAME, DB_URI

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(DB_URI)
        self.db = self.client[DB_NAME]
        self.req = self.db.requests

    async def find_join_req(self, id):
        return bool(await self.req.find_one({'id': id}))

    async def add_join_req(self, id):
        await self.req.insert_one({'id': id})

    async def del_join_req(self):
        await self.req.drop()

db = Database()
