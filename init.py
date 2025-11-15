import asyncpg
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN_BOT, host, db_password, db_user, db_name, port

#Init FastAPI, Bot and Dispatcher
app = FastAPI()
bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=MemoryStorage())

# Database create pool 'Getting pool back so we can use it to execute or fetch in any request'
async def create_pool():
    pool = await asyncpg.create_pool(
        host = host,
        database = db_name,
        password = db_password,
        port = port,
        user = db_user,
        ssl = 'require'
    )
    return pool

# Database close pool
async def close_pool(pool):
    await pool.close()