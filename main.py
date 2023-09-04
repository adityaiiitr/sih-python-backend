from fastapi import FastAPI

app = FastAPI()

# Example route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
@app.get("/sentiment_en")
def sentiment(text):
    t1 = TextBlob(text)
    sent = t1.polarity
    if sent<0:
        em = "Negative"
    elif sent==0:
        em = "Neutral"
    else:
        em = "Postive"
    return (em,sent)
