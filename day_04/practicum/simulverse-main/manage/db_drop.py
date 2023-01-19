from instance import config
import motor.motor_asyncio
import asyncio

async def do_drop(cli):
    cli.drop_database('simulverse')

client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URL)

loop = client.get_io_loop()
loop.run_until_complete(do_drop(client))
