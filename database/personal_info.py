from init import close_pool, create_pool
from utils.formatted_text import user_personal_info_formatted

"""
goal - 'lose_weight', 'maintain', 'gain_muscle'
gender - 'f', 'm'
"""
async def create_table_users_info(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users_info(
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE,
        age SMALLINT,
        height SMALLINT,
        weight NUMERIC(5,2),
        gender VARCHAR(1),
        goal VARCHAR(20))""")

# Adding user to database
async def new_user(pool, telegram_id, age, height, weight, gender, goal):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO users_info
        (telegram_id, age, height, weight, gender, goal) 
        VALUES
        ($1, $2, $3, $4, $5, $6)
        """, telegram_id, age, height, weight, gender, goal)

# Changed user info
async def change_user_info(pool, telegram_id, age, height, weight, gender, goal):
    async with pool.acquire() as conn:
        await conn.execute("""
        UPDATE users_info
        SET age=$1, height=$2, weight=$3, gender=$4, goal=$5
        WHERE telegram_id = $6;
        """, age, height, weight, gender, goal, telegram_id)

# Check if user already in database
async def user_exists(pool, telegram_id):
    async with pool.acquire() as conn:
        result = await conn.fetchval("""SELECT telegram_id FROM users_info WHERE telegram_id = $1""", telegram_id)
    return result is not None

# Taking user personal info from database
async def user_personal_info(pool, telegram_id):
    async with pool.acquire() as conn:
        result = await conn.fetchrow("""
        SELECT age, height, weight, gender, goal 
        FROM users_info WHERE telegram_id = $1
         """, telegram_id)
        return await user_personal_info_formatted(result)

