from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
import aioredis
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(description="Indexer Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/leaderboard")
async def get_leaderboard(days: int = 1):
    return {"leaderboard": "This is the leaderboard"}


async def get_redis():
    return aioredis.from_url(
        os.getenv("REDIS_URL"),
    )


async def get_data():
    redis = await get_redis()
    data_1 = requests.get("https://api.quickindexer.xyz/leaderboard/?days=1").json()
    data_7 = requests.get("https://api.quickindexer.xyz/leaderboard/?days=7").json()
    data_30 = requests.get("https://api.quickindexer.xyz/leaderboard/?days=30").json()
    data_from_api = [data_1, data_7, data_30]

    Leaderboard_data = {
        "1": data_from_api[0],
        "7": data_from_api[1],
        "30": data_from_api[2],
    }
    await redis.set("leaderboard_data", json.dumps(Leaderboard_data))
    await redis.close()
