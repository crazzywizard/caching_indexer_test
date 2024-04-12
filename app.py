from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import json
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
app.add_middleware(GZipMiddleware, minimum_size=1000)

async def get_redis():
    return aioredis.from_url(
        os.getenv("REDIS_URL"),
    )


@app.on_event("startup")
async def startup():
    print("App started")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/leaderboard")
async def get_leaderboard(days: int = 1):
    redis = await get_redis()
    values = await redis.get("leaderboard_data")
    if values:
        data = json.loads(values)
        if str(days) in data:
            return data[str(days)]
