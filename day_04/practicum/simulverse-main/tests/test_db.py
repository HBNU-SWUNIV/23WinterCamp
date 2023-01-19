from app.core.instance import config
from app.core.models.database import db_manager

import asyncio

def test_db_connect():
    async def do_insert():
        await db_manager.client.list_database_names()

    db_manager.init_manager(config.MONGODB_URL, "simulverse")

    loop = db_manager.client.get_io_loop()
    loop.run_until_complete(do_insert())

from app.core.schemas.user_model import UserInDB
from app.core.libs.utils import get_password_hash
from fastapi.encoders import jsonable_encoder

def test_setup_db():
    db_manager.init_manager(config.MONGODB_URL, "simulverse")
    
    async def do_drop():
        await db_manager.get_collection('users').drop()

    async def do_insert():
        await do_drop()
        user = UserInDB()
        user.userid = 'cbchoi'
        user.email = 'cbchoi@example.com'
        user.disabled = False
        user.hashed_password = get_password_hash('cbchoi')
        document = jsonable_encoder(user)
        result = await db_manager.get_collection('users').insert_one(document)
         
        result = await db_manager.get_user_by_email('cbchoi')
        assert result.userid == user.userid

    loop = db_manager.client.get_io_loop()
    loop.run_until_complete(do_insert())