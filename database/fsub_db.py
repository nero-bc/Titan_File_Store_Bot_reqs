import motor.motor_asyncio
from sample_info import tempDict
from config import REQUEST_CHANNEL, REQUEST_CHANNEL2
from typing import Union, List

REQUEST_CHANNELS = [REQUEST_CHANNEL, REQUEST_CHANNEL2]

class Fsub_DB:
    def __init__(self) -> None:
        self.client = motor.motor_asyncio.AsyncIOMotorClient(tempDict.get("indexDB"))
        self.db = self.client["Fsub_DB"]
        self.col_dict = {channel: self.db[str(channel)] for channel in REQUEST_CHANNELS}

    async def add_user(self, channel: Union[int, str], user_id: Union[int, str], first_name: str, user_name: str, date: str) -> None:
        await self.col_dict[channel].insert_one({"id": int(user_id), "fname": first_name, "uname": user_name, "date": date})

    async def get_user(self, channel: Union[int, str], user_id: Union[int, str]) -> Union[dict, None]:
        return await self.col_dict[channel].find_one({"id": int(user_id)})
    
    async def get_all(self, channel: Union[int, str]) -> Union[list, None]:
        return await self.col_dict[channel].find().to_list(length=None)
    
    async def delete_user(self, channel: Union[int, str], user_id: Union[int, str]) -> None:
        await self.col_dict[channel].delete_one({"id": int(user_id)})

    async def purge_all(self, channel: Union[int, str]) -> None:
        await self.col_dict[channel].delete_many({})

    async def total_users(self, channel: Union[int, str]) -> Union[int, None]:
        return await self.col_dict[channel].count_documents({})
