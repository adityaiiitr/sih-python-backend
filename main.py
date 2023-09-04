from fastapi import FastAPI

from pydantic import BaseModel
from textblob import TextBlob

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