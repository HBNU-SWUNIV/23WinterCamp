from ..app.core.instance import config
from ..app.core.models.database import db_manager

import asyncio

def test_db_connect():
    async def do_insert():
        await db_manager.client.list_database_names()

    db_manager.init_manager(config.MONGODB_URL, "simulverse")

    loop = db_manager.client.get_io_loop()
    loop.run_until_complete(do_insert())

test_db_connect()