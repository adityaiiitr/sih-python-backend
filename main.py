from fastapi import FastAPI, Depends, HTTPException, Security, Query
from bson import ObjectId
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel
from textblob import TextBlob

from dotenv import load_dotenv
import os

load_dotenv() 

month_map = {
    "JAN": "01",
    "FEB": "02",
    "MAR": "03",
    "APR": "04",
    "MAY": "05",
    "JUN": "06",
    "JUL": "07",
    "AUG": "08",
    "SEP": "09",
    "OCT": "10",
    "NOV": "11",
    "DEC": "12",
}

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
    published_from: str = Query(None, description="Start date for filtering Ex: 09-Sep-2023-12-00 "),
    published_to: str = Query(None, description="End date for filtering Ex: 10-Sep-2023-12-00"),
):
    if published_from and published_to:
        published_from = published_from.replace(published_from[3:6], month_map[published_from[3:6].upper()])
        published_to = published_to.replace(published_to[3:6], month_map[published_to[3:6].upper()])
        published_from=published_from.replace("-"," ")
        published_to=published_to.replace("-"," ")
    elif published_from:
        published_from = published_from.replace(published_from[3:6], month_map[published_from[3:6].upper()])
        published_from=published_from.replace("-"," ")

    elif published_to:
        published_to = published_to.replace(published_to[3:6], month_map[published_to[3:6].upper()])
        published_to=published_to.replace("-"," ")

    pib_collection = createConnection("piblinkv3")
    # {"publishedAt": {"$gte": "09 Sep 2023 12:00"}}
    filter_query = {}
    if published_from and published_to:
        filter_query["publishedAt"] = {
            "$gte": published_from,
            "$lte": published_to
        }
    elif published_from:
        filter_query["publishedAt"] = {"$gte": published_from}
    elif published_to:
        filter_query["publishedAt"] = {"$lte": published_to}


    data = pib_collection.find(filter_query)

    json_array = []

    for document in data:
        document_id = str(document['_id'])
        title = document.get('title', '')
        prid = document.get('prid', '')
        ministry = document.get('ministry', '')
        pibnodal = document.get('pibnodal', '')
        content = document.get('content', '')
        publishedAt = document.get('publishedAt', '')

        
# title
# content
# ministry
# pibnodal
# publishedAt
# prid


        json_object = {
            'id': document_id,
            'title': title,
            'content': content,
            'ministry': ministry,
            'pibnodal': pibnodal,
            'publishedAt': publishedAt,
            'prid': prid

        }
        json_array.append(json_object)

    return JSONResponse(content=json_array)
