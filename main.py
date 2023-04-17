from pymongo import InsertOne
from sanic import Sanic
from sanic.response import text, html, json
import json
import requests, asyncio, aiohttp
import motor.motor_asyncio, pymongo


config_file = open("config.json")
config = json.load(config_file)


app = Sanic(name="InnovaTech")
db_url = f"mongodb+srv://{config['MONGODB_USERNAME']}:{config['MONGODB_PASSWORD']}@cluster0.jd36ygh.mongodb.net/?retryWrites=true&w=majority"
db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
db = db_client["Smartphones"]["Smartphones"]


async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def get_url(url, headers):
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url=url, headers=headers)
        return result


@app.get("/")
async def welcome(request):
    # data : dict = {}
    # url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-models-by-brandname/Samsung"
    # headers = {
    #     "X-RapidAPI-Key": config["RAPID_API_KEY"],
    #     "X-RapidAPI-Host": "mobile-phone-specs-database.p.rapidapi.com"
    # }
    # page_no = 1
    # for i in range(1, 76):
    #     url = f"https://api.device-specs.io/api/smartphones?pagination[page]={i}&pagination[pageSize]=35&populate=*"
    #     headers = {
    #         "Authorization": f"Bearer {config['DEVICE_SPECS_API_TOKEN']}"
    #     }
    #     response = await get_url(url=url, headers=headers)
    #     page_no += 1
    #     response = json.loads(response)
    #     with open("smartphones_data.json", "a") as f:
    #         json.dump(response, f, indent=4)

        # data.update(response)

    with open("smartphones_data.json") as f:
        file_data = json.load(f)
        await db.insert_one(file_data)

    return text("Success")


if __name__ == '__main__':
    app.run(host="localhost", port=6969)
