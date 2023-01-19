from instance import config
import motor.motor_asyncio
from bson import ObjectId

from passlib.context import CryptContext
import pprint

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gepassword_hash(password):
    return pwd_context.hash(password)

async def do_check(db, collections:list):
    for item in collections:
        print(f"============= {item}")
        cursor = db[item].find({})
        for document in await cursor.to_list(length=100):
            pprint.pprint(document)

async def do_insert(db):
    data = [{'_id': ObjectId('632f214ab763ee36b2407777'),
            'email': 'cbchoi@example.com',
            'hashed_password': '$2b$12$2tTNtFUdYJ0N5mOr9dZH8uC.q3T6Q9Rq3E52Mj8cTzUN/rguHpBnq',
            'spaces': {'632f2162b763ee36b2407778':'Editor'},
            'userid': 'cbchoi'},
            {'_id': ObjectId('632f214ab763ee36b2407778'),
            'email': 'c@c.c',
            'hashed_password': '$2b$12$2tTNtFUdYJ0N5mOr9dZH8uC.q3T6Q9Rq3E52Mj8cTzUN/rguHpBnq',
            'spaces': {},
            'userid': 'cbchoi2'},
            {'_id': ObjectId('632f214ab763ee36b2407770'),
            'email': 'd@d.d',
            'hashed_password': '$2b$12$2tTNtFUdYJ0N5mOr9dZH8uC.q3T6Q9Rq3E52Mj8cTzUN/rguHpBnq',
            'spaces': {},
            'userid': 'cbchoi2'},
            ]

    await db['users'].insert_many(data)
    #db['space']
    data = {'_id':ObjectId('632f2162b763ee36b2407778'),'creator':ObjectId('632f214ab763ee36b2407777'), 'explain': 'seni and jaiyun', 'name': 'N4@417','scenes': {'632f2186b763ee36b240777b': '1234',
            '632f21a1b763ee36b2407785': '11421'}, 'viewers': {'632f214ab763ee36b2407777': 'Editor'}}
    await db['spaces'].insert_one(data)
    
    #db['scenes']
    data = [{'_id': ObjectId('632f2186b763ee36b240777b'),'image_id': ObjectId('632f2186b763ee36b2407779'),
                'links':[ObjectId('632f2186b763ee36b2407771'),ObjectId('632f2186b763ee36b2407772'),] , 'name': '1234'},
            {'_id': ObjectId('632f21a1b763ee36b2407785'), 'image_id': ObjectId('632f21a1b763ee36b240777c'),
                'links':[ObjectId('632f2186b763ee36b2407773'),] , 'name': '11421'}]

    await db['scenes'].insert_many(data)

    #db['links']
    data = [{'_id': ObjectId('632f2186b763ee36b2407771'), 'target_id':ObjectId('632f21a1b763ee36b2407785'), 'x':'0', 'y':'1', 'z':'-6', 'yaw':'0', 'pitch':"0", "roll":"0"}, 
            {'_id': ObjectId('632f2186b763ee36b2407772'), 'target_id':ObjectId('632f21a1b763ee36b2407785'), 'x':'0', 'y':'1', 'z':'-6', 'yaw':'0', 'pitch':"0", "roll":"0"},
            {'_id': ObjectId('632f2186b763ee36b2407773'), 'target_id':ObjectId('632f2186b763ee36b240777b'), 'x':'0', 'y':'1', 'z':'-6', 'yaw':'0', 'pitch':"0", "roll":"0"}]
    await db['links'].insert_many(data)

client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URL)

db = client["simulverse"]
db.drop_collection('users')
db.drop_collection('spaces')
db.drop_collection('scenes')
db.drop_collection('links')

loop = client.get_io_loop()
loop.run_until_complete(do_insert(db))
loop.run_until_complete(do_check(db, ['users', 'space', 'scenes', 'links']))

'''
async def do_delete_scene(db):
    await db['scenes'].delete_one({'_id':ObjectId('632f21a1b763ee36b2407785')})
    await db['links'].delete_many({'target_id':ObjectId('632f21a1b763ee36b2407785')})
    pass

async def do_delete_scenes(db, _id):
    await db['scenes'].delete_one({'_id':ObjectId(_id)})
    await db['links'].delete_many({'target_id':ObjectId(_id)})
    pass

async def do_delete_space(db):
    result = await db['space'].find_one({'_id':ObjectId('632f2162b763ee36b2407778')})
    for scene in result['scenes']:
        await do_delete_scenes(db, scene)
    await db['space'].delete_one({'_id':ObjectId('632f2162b763ee36b2407778')})

print("===== after")
loop.run_until_complete(do_delete_scene(db))
loop.run_until_complete(do_delete_space(db))
loop.run_until_complete(do_check(db, ['space', 'scenes', 'links']))


db.drop_collection('space')
db.drop_collection('scenes')
db.drop_collection('links')
'''