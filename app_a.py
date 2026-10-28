import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import database

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
TABLE = "games_a"

logging.basicConfig(
    filename="gamesync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    logging.info("Application A started")
    yield


app = FastAPI(title="GameSync A", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_key(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/games")
def get_games():
    try:
        return database.get_games(TABLE)
    except Exception as error:
        logging.error("Could not load games: %s", error)
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/games")
def add_game(game: dict, x_api_key: str = Header()):
    check_key(x_api_key)

    if not isinstance(game.get("title"), str) or not game["title"].strip():
        raise HTTPException(status_code=422, detail="Title is required")

    if not isinstance(game.get("genre"), str) or not game["genre"].strip():
        raise HTTPException(status_code=422, detail="Genre is required")

    try:
        added = database.add_game(TABLE, game)

        if not added:
            return {"message": "Game already exists", "game": game}

        logging.info("Added game: %s", game.get("title"))
        return {"message": "Game added", "game": game}

    except Exception as error:
        logging.error("Could not add game: %s", error)
        raise HTTPException(status_code=500, detail="Database error")

@app.post("/receive")
def receive_game(game: dict, x_api_key: str = Header()):
    check_key(x_api_key)

    if not isinstance(game.get("title"), str) or not game["title"].strip():
        raise HTTPException(status_code=422, detail="Title is required")

    if not isinstance(game.get("genre"), str) or not game["genre"].strip():
        raise HTTPException(status_code=422, detail="Genre is required")

    try:
        added = database.add_game(TABLE, game)

        if not added:
            logging.warning(
                "Conflict: game already exists - %s", game.get("title")
            )
            return {"message": "Conflict detected"}

        logging.info("Received game: %s", game.get("title"))
        return {"message": "Received"}

    except Exception as error:
        logging.error("Could not receive game: %s", error)
        raise HTTPException(status_code=500, detail="Database error")

@app.post("/sync")
def sync_games():
    try:
        games = database.get_games(TABLE)

        with httpx.Client(timeout=5) as client:
            for game in games:
                response = client.post(
                    "http://127.0.0.1:8001/receive",
                    json=game,
                    headers={"x-api-key": API_KEY}
                )
                response.raise_for_status()

        logging.info("Synchronization completed")
        return {"message": "Synced to B", "count": len(games)}

    except httpx.HTTPError as error:
        logging.error("Synchronization failed: %s", error)
        raise HTTPException(
            status_code=502,
            detail="Could not synchronize with application B"
        )
    except Exception as error:
        logging.error("Synchronization failed: %s", error)
        raise HTTPException(status_code=500, detail="Database error")