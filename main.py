from pymongo import InsertOne
from sanic import Sanic
from sanic.response import text, html, json
import json
import requests, asyncio, aiohttp
import motor.motor_asyncio, pymongo


config_file = open("innovatech/config.json")
config = json.load(config_file)


app = Sanic(name="InnovaTech")
db_url = f"mongodb+srv://{config['MONGODB_USERNAME']}:{config['MONGODB_PASSWORD']}@cluster0.jd36ygh.mongodb.net/?retryWrites=true&w=majority"
db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
db = db_client["Smartphones"]


welcome_html_page = open("innovatech/welcome.html", "r")


async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def get_url(url, headers):
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url=url, headers=headers)
        return result


@app.get("/")
async def welcome(request):

    """
    Extracted database into JSON file from the API DeviceSpecs
    """

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

    """
    Inserted data to the database
    """

    # with open("smartphones_data.json", "r") as f:
    #     data = json.load(f)
    # merged_data : dict = {}
    # for jsonobj in data:
    #     merged_data.update(jsonobj)
    # with open("smartphones_data2.json", "w") as f:
    #     json.dump(modified_data, f, indent=4)
    # return text("Success")

    # with open("smartphones_data.json") as f:
    #     file_data = json.load(f)
    #     async with await db_client.start_session() as s:
    #         for jsonobj in file_data:
    #             await db.get_collection("Smartphones").insert_one(jsonobj, session=s)
    #     return text("Success")

    test_questions = {
        "What is your budget?": [">10,000", "10,000-15,000", "15,000-20,000", "20,000-30,000", "30,000-40,000"],
        "What is your age group?": ["13-18", "18-30", "30-60", "60+"],
        "What is your screentime?": ["<1hr", "1-2hrs", "2-6hrs", "6+hrs"],
        "Do you care about how your phone looks?": ["Yes", "No"],
        "How many photos do you click in a day?": ["Not everyday", "1-2", "2-10", "10+"],
        "Which screen size do you prefer?": ["<5.5inches", "5-6inches", "6+inches"],
        "How much storage is sufficient according to you?": ["32GB", "64GB", "128GB", "256GB"],
        "What are your basic needs?": ["Messaging and Calls", "Gaming", "Photography"],
        "How much RAM is sufficient according to your needs?": ["2GB", "4GB", "6GB", "6GB+"]
    }

    
    return html(str(welcome_html_page.read()))


if __name__ == '__main__':
    app.run(host="localhost", port=6969)
