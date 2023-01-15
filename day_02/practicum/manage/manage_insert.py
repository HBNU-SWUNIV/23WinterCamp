import motor.motor_asyncio
from bson import ObjectId

async def do_insert(db):
    data = [{'_id': ObjectId('632f214ab763ee36b2407777'),
            'email': 'cbchoi@example.com',
            'hashed_password': '$2b$12$2tTNtFUdYJ0N5mOr9dZH8uC.q3T6Q9Rq3E52Mj8cTzUN/rguHpBnq',
            'spaces': {'632f2162b763ee36b2407778':'Editor'},
            'userid': 'cbchoi'},]
    await db['users'].insert_many(data)

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://cbchoi:winter23@localhost:27017")

db = client["simulverse"]
loop = client.get_io_loop()
loop.run_until_complete(do_insert(db))
