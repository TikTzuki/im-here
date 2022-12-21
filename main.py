import asyncio
import os
import traceback

import netifaces as ni
from motor.motor_asyncio import (
    AsyncIOMotorClient
)

DATABASE_URL = 'mongodb+srv://tik:Ld201199@cluster0.bh9kt.mongodb.net/?retryWrites=true&w=majority'
mongo_connect = AsyncIOMotorClient(DATABASE_URL)
mongo_db = mongo_connect.get_database("test")


async def run():
    coll = mongo_db["running_device"]
    d = {"name": os.getenv("NAME", "raspi")}
    for interface in ni.interfaces():
        try:
            d.update({interface: ni.ifaddresses(interface)[ni.AF_INET]})
        except:
            continue

    await coll.insert_one(d)


async def main():
    while True:
        try:
            await run()
            print("done run")
            await asyncio.sleep(60 * 5)
        except KeyboardInterrupt:
            return
        except Exception as e:
            traceback.print_exc()
            continue


loop = mongo_connect.get_io_loop()
loop.run_until_complete(main())
