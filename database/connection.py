import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DB_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT NOT NULL,
            rank TEXT NOT NULL,
            is_player BOOLEAN DEFAULT FALSE,
            class TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            exp INTEGER DEFAULT 0,
            exp_to_next_level INTEGER DEFAULT 100,
            hp INTEGER,
            attack INTEGER,
            magic_attack INTEGER,
            defense INTEGER,
            speed INTEGER,
            mana INTEGER,
            gold INTEGER DEFAULT 0,
            raids_completed INTEGER DEFAULT 0,
            awaken_attempts INTEGER DEFAULT 0
        )
    ''')
    await conn.close()

async def get_connection():
    return await asyncpg.connect(DB_URL)
