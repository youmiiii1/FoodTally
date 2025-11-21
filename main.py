import logging
import asyncio
from fastapi import Request
from handlers import *
from init import app, bot, dp, create_pool, close_pool
from database.meal_report import create_table_meal_report, new_report
from database.personal_info import create_table_users_info
from keyboards.main_menu import main_menu_keyboard
from texts.main_menu import main_menu_text
from utils.formatted_text import make_record_formatted, make_reply_formatted, make_build_formatted, make_shop_help_formatted

# Logging to logs.txt
logging.basicConfig(level=logging.INFO,
                    filemode='a',
                    filename='logs.txt',
                    format="%(asctime)s %(levelname)s %(message)s")

# Catching http post request from make.com (From Meal Report)
@app.post("/make_record")
async def make_reply(request: Request):
    try:
        data = await request.json()
        formatted = await make_record_formatted(data)

        result = await bot.send_message(
            chat_id=formatted["chat_id"],
            text=formatted["text"],
            parse_mode="HTML"
        )

        # Timeless connection pool only for this request
        """
        Why is this needed? 
        We cannot reuse the global connection pool created by `create_pool()` inside a FastAPI POST request handler,
        because it may not be available or properly initialized in this async context.
        Therefore, we create a new temporary pool for this specific request instead.
        """
        pool = await create_pool()
        await new_report(
            pool,
            formatted["chat_id"],
            formatted["dish_name"],
            formatted["calories_estimated"],
            formatted["protein_g"],
            formatted["fat_g"],
            formatted["carbs_g"],
            formatted["balance_assessment"],
            formatted["products_list"]
        )
        await pool.close()

        await bot.send_message(formatted["chat_id"], main_menu_text, reply_markup=main_menu_keyboard)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# Catching http post request from make.com (From Photo analyze)
@app.post("/make_reply")
async def make_reply(request: Request):
    try:
        data = await request.json()
        formatted = await make_reply_formatted(data)


        result = await bot.send_message(
            chat_id=formatted["chat_id"],
            text=formatted["text"],
            parse_mode="HTML"
        )

        await bot.send_message(formatted["chat_id"], main_menu_text, reply_markup=main_menu_keyboard)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# Catching http post request from make.com (From Build Meal)
@app.post("/make_build")
async def make_reply(request: Request):
    try:
        data = await request.json()
        formatted = await make_build_formatted(data)

        result = await bot.send_message(
            chat_id=formatted["chat_id"],
            text=formatted["text"],
            parse_mode="HTML"
        )

        await bot.send_message(formatted["chat_id"], main_menu_text, reply_markup=main_menu_keyboard)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# Catching http post request from make.com (From Shop Helper)
@app.post("/make_shop_help")
async def make_reply(request: Request):
    try:
        data = await request.json()
        formatted = await make_shop_help_formatted(data)

        result = await bot.send_message(
            chat_id=formatted["chat_id"],
            text=formatted["text"],
            parse_mode="HTML"
        )

        await bot.send_message(formatted["chat_id"], main_menu_text, reply_markup=main_menu_keyboard)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# Creating pool for Database everytime program running
@dp.startup.register
async def on_startup(bot: bot):
    pool = await create_pool()
    dp['db_pool'] = pool

    await create_table_meal_report(pool)
    await create_table_users_info(pool)

# Closing pool for Database everytime program stoping
@dp.shutdown.register
async def on_shutdown(bot: bot):
    pool = dp.get('db_pool')

    if pool:
        await close_pool(pool)

# Init our routers from handles so they work
async def init_bot():
    dp.include_routers(main_menu.router, personal_info.router, photo_analyze.router, meal_report.router, build_meal.router)

    await dp.start_polling(bot)

# Starter
async def main():
    task_1 = asyncio.create_task(init_bot())

    await task_1

if __name__ == '__main__':
    asyncio.run(main())