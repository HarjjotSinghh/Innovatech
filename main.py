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


    filter = {
        "battery": {"$gt": battery_gt, "$lt": battery_lt},
        "price": {"$gt": price_gt, "$lt": price_lt},
        "main_camera": {"$gt": main_camera_gt, "$lt": main_camera_lt},
        "display_size": {"$gt": display_size_gt, "$lt": display_size_lt},
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
        other_best_smartphones =  [sorted(best_smartphones, key=lambda x: x["price"])][0][1:4]
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


@app.get("/get_started")
async def welcome():
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

@app.route("/")
async def home():
    return render_template("mobihunt.html")

if __name__ == '__main__':
    
    app.run(host="localhost", port=6969)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(welcome())
    finally:
        loop.close()
