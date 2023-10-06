from fastapi import FastAPI, Depends, HTTPException, Security, Query
from bson import ObjectId
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel
from textblob import TextBlob

from dotenv import load_dotenv
import os

load_dotenv() 

from fastapi.security.api_key import APIKeyHeader

api_key = APIKeyHeader(name="Authorization")
TOKEN_1 = os.getenv("TOKEN_1")
TOKEN_2 = os.getenv("TOKEN_2")

def authenticate_api_key(api_key: str = Security(api_key)):
    if api_key == TOKEN_1 or api_key == TOKEN_2:
        return api_key
    raise HTTPException(status_code=403, detail="API Key not valid")

from db import createConnection
collection = createConnection("aditya")
pib_collection = createConnection("piblink")


app = FastAPI()

# Example route
@app.get("/")
def read_root(api_key: str = Depends(authenticate_api_key)):
    return {"message": "Hello, World!"}


class SentimentRequest(BaseModel):
    text:str

@app.post("/analyze_sentiment")
async def analyze_sentiment(request: SentimentRequest):
    text = request.text
    t1 = TextBlob(text)
    polarity = t1.sentiment.polarity

    if polarity < 0:
        sentiment = "Negative"
    elif polarity == 0:
        sentiment = "Neutral"
    else:
        sentiment = "Positive"

    responseBody = {"text":text,"sentiment": sentiment, "polarity": polarity}

    inserted_item = collection.insert_one(responseBody)
    # print(inserted_item)
    # print(type(inserted_item))

    return {"success":True, "id":str(inserted_item.inserted_id),"text":text,"sentiment": sentiment, "polarity": polarity}

from scraper import scrapeLink
class ScraperRequest(BaseModel):
    query:str
    lang:str='en'
@app.post("/scrape_news_link")
async def scrape_news_link(request: ScraperRequest):
    response = scrapeLink(query=request.query,lang=request.lang)
    return {"success":True, "result":response}

@app.get("/pib_news")
def pIB_news_link(
    start_date: str = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    start_time: str = Query(None, description="Start time for filtering (HH:MM:SS)"),
    end_time: str = Query(None, description="End time for filtering (HH:MM:SS)")
):
    pib_collection = createConnection("piblink")

    filter_query = {}
    if start_date:
        filter_query["timestamp.date"] = {"$gte": start_date}
    if end_date:
        filter_query["timestamp.date"] = {"$lte": end_date}
    if start_time:
        filter_query["timestamp.time"] = {"$gte": start_time}
    if end_time:
        filter_query["timestamp.time"] = {"$lte": end_time}

    data = pib_collection.find(filter_query)

    json_array = []

    for document in data:
        document_id = str(document['_id'])
        title = document.get('title', '')
        url = document.get('url', '')
        timestamp = document.get('timestamp', '')
        lang = document.get('lang', '') 
        json_object = {
            'id': document_id,
            'title': title,
            'url': url,
            'timestamp': timestamp,
            'lang':lang
        }
        json_array.append(json_object)

    return JSONResponse(content=json_array)
