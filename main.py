from pymongo import InsertOne
from sanic import Sanic
from sanic.response import text, html, json
import json
import requests, asyncio, aiohttp
import motor.motor_asyncio, pymongo
from flask import Flask, render_template, request
import pprint
from amazon_paapi import AmazonApi
from bs4 import BeautifulSoup
import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import re


config_file = open("innovatech/config.json")
config = json.load(config_file)


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SERVER_NAME'] = 'localhost:6969'
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = 'http'
app.app_context().push()


db_url = f"mongodb+srv://{config['MONGODB_USERNAME']}:{config['MONGODB_PASSWORD']}@cluster0.jd36ygh.mongodb.net/?retryWrites=true&w=majority"
db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
db = db_client["Smartphones"]


amazon = AmazonApi(config["AMAZON_API_ACCESS_KEY"], config["AMAZON_API_SECRET_ACCESS_KEY"], country='IN', tag="harjjotsinghh-21")

# welcome_html_page = open("innovatech/welcome.html", "r")

fake_space = chr(0x00002800)
test_questions = {  
        "What is your budget?": [">10,000", "10,000-20,000", "20,000-30,000", "30,000-40,000", "40,000-70,000", "70,000+"],
        "What is your age group?": ["13-18", "18-30", "30-60", "60+"],
        "What is your screentime?": ["<4hrs", "4-8hrs", "8-12hrs", "12+hrs"],
        "Do you care about how your phone looks?": ["Yes", "No"],
        "How often do use your phone's camera?": [f"Not{fake_space}that{fake_space}much", "Sometimes", "Frequently", f"All{fake_space}the{fake_space}time"],
        "What screen size do you prefer?": ["<6inches", "6-6.4inches", "6.4+inches"],
        "How much storage is sufficient for you?": ["32GB", "64GB", "128GB", "256GB", "512GB+"],
        "What do you typically do on your smartphone on daily basis?": [f"Messaging{fake_space}and{fake_space}Calling", "Gaming", "Photography", "Videography"],
        "How much RAM is sufficient according to your needs?": ["2GB", "4GB", "6GB", "8GB+"]
    }
user_data = {}


async def get_smartphone_recommendation(user_data : dict):

    # df = pd.DataFrame(data)

    # features = df[["battery", "display_size", "main_camera", "internal_memory"]]
    # target = df["modelname"]
    # features_train, features_test, target_train, target_test = train_test_split(features, target, test_size=0.2)

    # clf = DecisionTreeClassifier()
    # clf.fit(features_train, target_train)
    # accuracy = clf.score(features_test, target_test)
    # prediction = clf.predict([[
    #     battery,
    #     user_data["What screen size do you prefer?"],
    #     main_camera,
    #     user_data["How much RAM is sufficient according to your needs?"],
    # ]])


    # required_properties = [
    #     "battery",
    #     "body_build",
    #     "colors", 
    #     "display_size", 
    #     "main_camera", 
    #     "internal_memory", 
    #     "modelname",
    #     "price",
    #     "gpu",
    #     "cpu"
    # ]
    # battery = ""
    # requirements = {
    #     "battery",
    #     "body_build",
    #     "colors", 
    #     "display_size", 
    #     "main_camera", 
    #     "internal_memory", 
    #     "modelname",
    #     "price",
    #     "gpu",
    #     "cpu"
    # }

    smartphone_recommendations = []

    battery_gt = 0
    battery_lt = 0
    main_camera_gt = 0
    main_camera_lt = 0
    price_gt = 0
    price_lt = 0
    display_size_gt = 0
    display_size_lt = 0
    rom_gt = 0
    rom_lt = 0
    ram_gt = 0
    ram_lt = 0

    if list(user_data.values())[0] == "<10,000":
        price_gt = 0
        price_lt = 10000
    elif list(user_data.values())[0] == "10,000-20,000":
        price_gt = 0
        price_lt = 20000
    elif list(user_data.values())[0] == "20,000-30,000":
        price_gt = 0
        price_lt = 30000
    elif list(user_data.values())[0] == "30,000-40,000":
        price_gt = 0
        price_lt = 40000
    elif list(user_data.values())[0] == "40,000-70,000":
        price_gt = 0
        price_lt = 70000
    elif list(user_data.values())[0] == "70,000+":
        price_gt = 0
        price_lt = 700000

    if list(user_data.values())[2] == "<4hrs":
        battery_gt = 2000
        battery_lt = 5000
    elif list(user_data.values())[2] == "4-8hrs":
        battery_gt = 2000
        battery_lt = 5500
    elif list(user_data.values())[2] == "8-12hrs":
        battery_gt = 3000
        battery_lt = 6000
    elif list(user_data.values())[2] == "12+hrs":
        battery_gt = 4000
        battery_lt = 10000

    if list(user_data.values())[4] == f"Not{fake_space}that{fake_space}much":
        main_camera_gt = 2
        main_camera_lt = 33
    elif list(user_data.values())[4] == "Sometimes":
        main_camera_gt = 5
        main_camera_lt = 65
    elif list(user_data.values())[4] == "Frequently":
        main_camera_gt = 10
        main_camera_lt = 111
    elif list(user_data.values())[4] == f"All{fake_space}the{fake_space}time":
        main_camera_gt = 40
        main_camera_lt = 200
    
    if list(user_data.values())[5] == "<6inches":
        display_size_gt = 0.0
        display_size_lt = 6.0
    elif list(user_data.values())[5] == "6-6.4inches":
        display_size_gt = 6.0
        display_size_lt = 6.4
    elif list(user_data.values())[5] == "6.4+inches":
        display_size_gt = 6.4
        display_size_lt = 20.0
    

    if list(user_data.values())[6] == "64GB":
        rom_gt = 64
        rom_lt = 64
    elif list(user_data.values())[6] == "32GB":
        rom_gt = 32
        rom_lt = 32
    elif list(user_data.values())[6] == "128GB":
        rom_gt = 128
        rom_lt = 128
    elif list(user_data.values())[6] == "256GB":
        rom_gt = 256
        rom_lt = 256
    elif list(user_data.values())[6] == "512GB+":
        rom_gt = 512
        rom_lt = 4000
    
    if list(user_data.values())[8] == "4GB":
        ram_gt = 4
        ram_lt = 4
    elif list(user_data.values())[8] == "6GB":
        ram_gt = 6
        ram_lt = 6
    elif list(user_data.values())[8] == "2GB":
        ram_gt = 2
        ram_lt = 2
    elif list(user_data.values())[8] == "8GB+":
        ram_gt = 8
        ram_lt = 50

    # print(ram_gt, ram_lt, rom_gt, rom_lt)
    
    # my_function = """
    #     function() {
    #         for (var i = 0; i < this.internall_memory.length; i++) {
    #             var obj = this.internall_memory[i];
    #             if (obj.Storage == {rom} && obj.RAM == {ram}) {
    #                 return true;
    #             }
    #         }
    #         return false;
    #     }
    # """.format(rom=rom_gt, ram=ram_gt)

    filter = {
        "battery": {"$gt": battery_gt, "$lt": battery_lt},
        "price": {"$gt": price_gt, "$lt": price_lt},
        "main_camera": {"$gt": main_camera_gt, "$lt": main_camera_lt},
        "display_size": {"$gt": display_size_gt, "$lt": display_size_lt},
        # "internall_memory": { "$elemMatch": { 
        #                                     "Storage": {"$gt": rom_gt, "$lt": rom_lt},
        #                                     "RAM": {"$gt": ram_gt, "$lt": rom_lt} 
        #                                     }
        #                     }
        # "internall_memory": { 
        #                         "Storage": {"$gt": rom_gt, "$lt": rom_lt},
        #                         "RAM": {"$gt": ram_gt, "$lt": rom_lt} 
        #                     }
    }

    required_data = await (db["Smartphones"].find(filter)).to_list(length=None)
    best_smartphones = []

    for i in required_data:
        for j in i["internall_memory"]:
            if j["Storage"] <= rom_lt and j["Storage"] >= rom_gt and j["RAM"] <= ram_lt and j["RAM"] >= ram_gt:
                best_smartphones.append(i)
    
    best_smartphones_names = [x["modelname"] for x in best_smartphones]
    try:
        best_smartphone_ = [sorted(best_smartphones, key=lambda x: x["price"])][0][0]
    except IndexError:
        best_smartphone_ = None
    try:
        other_best_smartphones =  [sorted(best_smartphones, key=lambda x: x["price"])][0][1:6]
    except IndexError:
        other_best_smartphones = None
    RAM=ram_gt
    Storage=rom_gt
    
    return [best_smartphone_, other_best_smartphones,RAM,Storage]


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

    
    # battery_sizes = []

    # for name in smartphones_names[0:20]:
    #     url = f"https://www.gsmarena.com/{name.lower().replace(' ', '_')}-reviews.php3"

    #     response = await get_url(url)
    #     soup = BeautifulSoup(response, 'html.parser')
    #     try:
    #         battery_elem = soup.find('td', string='Battery').find_next_sibling('td')
    #         battery_text = battery_elem.get_text(strip=True)

    #         battery_size = int(battery_text.split()[0])
    #         battery_sizes.append(battery_size)
    #     except:
    #         battery_sizes.append(None)

    # data = await get_url(url="https://api-mobilespecs.azharimm.dev/v2/apple_iphone_12_pro_max-10237", headers=None)

    # data = []

    """
    Trying to scrape data from gsmarena
    """

    # for name in smartphones_names[0:10]:

    #     name_url = name.replace(' ', '-')
    #     url = f'https://www.gsmarena.com/res.php3?sSearch={name_url}&idMaker=0'
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     search_result = soup.find('div', class_='makers').find('a')

    #     if search_result:
    #         link = 'https://www.gsmarena.com/' + search_result['href']
    #         data.append(f'{name}: {link}')
    #     else:
    #         data.append(f'{name}: Not found')

    """
    Removed discontinued phones from database
    """

    # path = "C:\Everything Else\Innovatech\Innovatech\smartphone-specs-scraper-main\scraped_data"
    # dir_list = sorted(os.listdir(path))
    # files_to_be_removed = []
    # data_ = {}
    # for file in dir_list:
    #     with open(f"./Innovatech/smartphone-specs-scraper-main/scraped_data/{file}") as f:
    #         data_ = json.load(f)
    #         data.append(data_)
    #         # print(data_["launch_status"])
    #         if not "available" in data_["launch_status"].lower():
    #             files_to_be_removed.append(file)
                
    # for file in files_to_be_removed:
    #     os.remove(f"{path}\{file}")
    #     print(f"Removed {file}")

    """
    Entering finalised data into mongoDB
    """

    # path = "C:\Everything Else\Innovatech\Innovatech\smartphone-specs-scraper-main\scraped_data"
    # dir_list = sorted(os.listdir(path))
    # # files_to_be_removed = []

    # for file in dir_list:
    #     with open(f"./Innovatech/smartphone-specs-scraper-main/scraped_data/{file}") as f:

    #         file_data = json.load(f)
            # main_camera = file_data["main_camera"]
            # match1 = re.search(r'(\d+)\s*MP', main_camera)
            # display_size = file_data["display_size"]
            # match2 = re.search(r'(\d+(\.\d+)?)', display_size)

            # if match2:
            #     number1 = float(match2.group(1))
            #     file_data["display_size"] = number1
            #     print(number1)
            #     with open(f"./Innovatech/smartphone-specs-scraper-main/scraped_data/{file}", "w") as f_:
            #         json.dump(file_data, f_, indent=4)
            #         print(file)
            # else:
            #     print("No match", file)

            # async with await db_client.start_session() as s:
            #     await db.get_collection("Smartphones").insert_one(file_data, session=s)
            #     print(f"Inserted {file}")                 
           
            # try:
            #     if isinstance(file_data["price"], int) and file_data["price"] > 100000:
            #         file_data["price"] = int(file_data["price"]) / 100
            #     elif isinstance(file_data["price"], str):
            #         if file_data["price"].isnumeric():
            #             if int(file_data["price"]) > 100000:
            #                 file_data["price"] = int(file_data["price"]) / 100
            #         else:
            #             print(file)
            # except ValueError:
            #     continue

            # with open(f"./Innovatech/smartphone-specs-scraper-main/scraped_data/{file}", "w") as f_:
            #         json.dump(file_data, f_, indent=4)
            #         print(file)
            
            # internal_memory = file_data["internal_memory"]
            # internal_memory_list = []
            # for substring in internal_memory.split(", "):
            #     substring = substring.strip()
            #     storage, ram = substring.split(" ")[0:2]
            #     storage = int(storage[:-2])
            #     ram = int(ram[:-2])
            #     internal_memory_list.append({"Storage": storage, "RAM": ram})
            # file_data["internall_memory"] = internal_memory_list
            # with open(f"./Innovatech/smartphone-specs-scraper-main/scraped_data/{file}", "w") as f_:
            #     json.dump(file_data, f_, indent=4)

    #         data.append(file)
    #         if "$" in file_data["price"]:
    #             match = re.search(r'\d+\.\d+', file_data["price"])
    #             if match:
    #                 price = match.group()
    #                 file_data["price"] = str(int(float(price) * 82))
    #                 print(price)
    #                 with open(f"./Innovatech/smartphone-specs-scraper-main/scraped_data/{file}", "w") as f_:
    #                     json.dump(file_data, f_)
    #             if not match:
    #                 print(file)
    #                 files_to_be_removed.append(file)

    #         elif "about" and not "inr" in file_data["price"].lower():
    #             match = re.search(r'\d+', file_data["price"])
    #             if match:
    #                 price = match.group()
    #                 file_data["price"] = str(int(float(price) * 91))
    #                 print(price)
    #                 with open(f"./Innovatech/smartphone-specs-scraper-main/scraped_data/{file}", "w") as f_:
    #                     json.dump(file_data, f_)
    #             if not match:
    #                 print(file)
    #                 files_to_be_removed.append(file)            
    
    # for file in files_to_be_removed:
    #     os.remove(f"{path}\{file}")
    #     print(f"Removed {file}")
    with app.app_context():
        return render_template("welcome.html", questions=test_questions)

@app.route('/get_user_data', methods=['POST'])
async def get_user_data():
    global user_data
    user_data = json.loads(request.form['javascript_data'])
    return user_data

@app.route("/result")
async def result():
    await asyncio.sleep(0.3)
    data = await get_smartphone_recommendation(user_data)
    return render_template("result.html", user_data=user_data, data=data)

@app.route("/tech_news")
async def tech_news():
    return render_template("Tech News.html")


if __name__ == '__main__':
    
    app.run(host="localhost", port=6969)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(welcome())
    finally:
        loop.close()
