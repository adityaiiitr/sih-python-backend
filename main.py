from fastapi import FastAPI

app = FastAPI()

# Example route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
