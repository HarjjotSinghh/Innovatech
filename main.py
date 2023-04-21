from pymongo import InsertOne
from sanic import Sanic
from sanic.response import text, html, json
import json
import requests, asyncio, aiohttp
import motor.motor_asyncio, pymongo
from flask import Flask, render_template
import pprint
from amazon_paapi import AmazonApi
from bs4 import BeautifulSoup



config_file = open("innovatech/config.json")
config = json.load(config_file)


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


db_url = f"mongodb+srv://{config['MONGODB_USERNAME']}:{config['MONGODB_PASSWORD']}@cluster0.jd36ygh.mongodb.net/?retryWrites=true&w=majority"
db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
db = db_client["Smartphones"]


amazon = AmazonApi(config["AMAZON_API_ACCESS_KEY"], config["AMAZON_API_SECRET_ACCESS_KEY"], country='IN', tag="harjjotsinghh-21")

# welcome_html_page = open("innovatech/welcome.html", "r")

test_questions = {
        "What is your budget?": [">10,000", "10,000-15,000", "15,000-20,000", "20,000-30,000", "30,000-40,000", "40,000-70,000", "70,000-1,00,000"],
        "What is your age group?": ["13-18", "18-30", "30-60", "60+"],
        "What is your screentime?": ["<4hrs", "4-6hrs", "6-8hrs", "8-10hrs", "10+hrs"],
        "Do you care about how your phone looks?": ["Yes", "No"],
        "How often do use your phone's camera?": ["Not that much", "Sometimes", "Frequently", "All the time"],
        "What screen size do you prefer?": ["<5.5inches", "5-6inches", "6+inches"],
        "How much storage is sufficient for you?": ["64GB", "128GB", "256GB", "512GB+"],
        "What do you typically do on your smartphone on daily basis?": ["Messaging and Calling", "Gaming", "Photography", "Videography"],
        "How much RAM is sufficient according to your needs?": ["4GB", "6GB", "8GB+"]
    }


async def fetch(session, url, headers = None):
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def get_url(url, headers = None):
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url=url, headers=headers)
        return result
    
async def get_data(length = None):
    cursor = db["Smartphones"].find()
    data = await cursor.to_list(length=length)
    return data


@app.get("/")
async def welcome():

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

    """
    Extracted Smartphones Names
    """

    # data = await get_data(74)
    # data_ = []
    
    # for i in range(75):
    #     for j in data[i-1]["data"]:
    #         data_.append(j["name"])
    
    # smartphones_names: dict = {}

    # for name in data_:
    #     smartphones_names.update({name: ""})

    # with open("./innovatech/smartphones_names.json", "w") as f:
    #     json.dump(data_, f, indent=4)

    """
    Removed duplicates and removed preowned phones
    """

    # smartphones_names : list = json.load(open("./innovatech/smartphones_names.json", "r"))
    
    # for i in list(smartphones_names):
    #     if "PreOwned" in i:
    #         smartphones_names.remove(i)

    # smartphones_names = [i for n, i in enumerate(smartphones_names) if i not in smartphones_names[:n]]

    # with open("./innovatech/smartphones_names.json", "w") as f:
    #     json.dump(smartphones_names, f, indent=4)

    smartphones_names : list = json.load(open("./innovatech/smartphones_names.json", "r"))
    battery_sizes = []

    for name in smartphones_names[0:20]:
        url = f"https://www.gsmarena.com/{name.lower().replace(' ', '_')}-reviews.php3"

        response = await get_url(url)
        soup = BeautifulSoup(response, 'html.parser')
        try:
            battery_elem = soup.find('td', string='Battery').find_next_sibling('td')
            battery_text = battery_elem.get_text(strip=True)

            battery_size = int(battery_text.split()[0])
            battery_sizes.append(battery_size)
        except:
            battery_sizes.append(None)


    return render_template("welcome.html", data=battery_sizes)


if __name__ == '__main__':  
    
    app.run(host="localhost", port=6969)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(welcome())
    finally:
        loop.close()
