from fastapi import FastAPI, Depends, HTTPException, Security

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

app = FastAPI()

# Example route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


class SentimentRequest(BaseModel):
    text:str

@app.post("/analyze_sentiment")
async def analyze_sentiment(request: SentimentRequest, api_key: str = Depends(authenticate_api_key)):
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