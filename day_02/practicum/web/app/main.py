from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo:dbdb@localhost:27017")
db = client["simulverse"]

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    contents = "<h1> Hello, World </h1>\n"
    cursor = db['users'].find({})
    for document in await cursor.to_list(length=100):
        contents += f"<h2>{document['email']}</h2>"
    
    return contents
