from fastapi import FastAPI
from uvicorn import run
from dotenv import load_dotenv
from app.routes import mongo

load_dotenv()

app = FastAPI()

app.include_router(mongo.router, prefix="/mongo", tags=["mongo_agent"])


@app.get("/")
async def root():
    return {"message": "Fast API App is running!"}


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
