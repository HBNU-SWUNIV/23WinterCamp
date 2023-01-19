from instance import config
import motor.motor_asyncio
import pprint
import asyncio

async def do_check(db, collections:list):
    for item in collections:
        cursor = db[item].find({})
        for document in await cursor.to_list(length=100):
            print(type(document["_id"]))
            pprint.pprint(document)

client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URL)
db = client["simulverse"]

loop = client.get_io_loop()
loop.run_until_complete(do_check(db, ['spaces']))
