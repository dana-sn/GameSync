import json
import psycopg2
from psycopg2.extras import Json

import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "gamesync",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD")

}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games_a (
                    id SERIAL PRIMARY KEY,
                    game_data JSONB NOT NULL UNIQUE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games_b (
                    id SERIAL PRIMARY KEY,
                    game_data JSONB NOT NULL UNIQUE
                )
            """)

def get_games(table):
    if table not in ("games_a", "games_b"):
        raise ValueError("Invalid table name")
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT game_data FROM {table} ORDER BY id"
            )
            return [row[0] for row in cursor.fetchall()]

def add_game(table, game):
    if table not in ("games_a", "games_b"):
        raise ValueError("Invalid table name")
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {table} (game_data)
                VALUES (%s)
                ON CONFLICT (game_data) DO NOTHING
                RETURNING id
                """,
                (Json(game),)
            )
            return cursor.fetchone() is not None