#(©)CodeXBotz

from motor.motor_asyncio import AsyncIOMotorClient
from config import DB_URI, DB_NAME

dbclient = AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']


async def present_user(user_id: int) -> bool:
    found = await user_data.find_one({'_id': user_id})
    return bool(found)


async def add_user(user_id: int):
    await user_data.insert_one({'_id': user_id})
    return


async def full_userbase():
    user_ids = []
    async for doc in user_data.find({}, {'_id': 1}):
        user_ids.append(doc['_id'])
    return user_ids


async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})
    return
