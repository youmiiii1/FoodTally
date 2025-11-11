import logging
import asyncio
from fastapi import Request
from handlers import *
from init import app, bot, dp, create_pool, close_pool
from database.meal_report import create_table_meal_report, new_report
from database.personal_info import create_table_users_info
from keyboards.main_menu import main_menu_keyboard
from texts.main_menu import main_menu_text

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

        # Getting and formating from make.com as string
        chat_id = int(data.get("chat_id"))
        dish_name = str(data.get("dish_name"))
        calories_estimated = int(data.get("calories_estimated"))
        protein_g = float(data.get("protein_g"))
        fat_g = float(data.get("fat_g"))
        carbs_g = float(data.get("carbs_g"))
        balance_assessment = str(data.get("balance_assessment"))
        products_list = str(data.get("products_list"))

        result = await bot.send_message(
            chat_id,
            f"<b>🍽 {dish_name}</b>\n"
            f"──────────────────────\n"
            f"  • <b>Calories:</b> {calories_estimated} kcal\n"
            f"  • <b>Protein:</b> {protein_g} g\n"
            f"  • <b>Fat:</b> {fat_g} g\n"
            f"  • <b>Carbohydrates:</b> {carbs_g} g\n\n"
            f"<i>💬 {balance_assessment}</i>",
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
        await new_report(pool, chat_id, dish_name, calories_estimated, protein_g, fat_g, carbs_g, balance_assessment, products_list)
        await pool.close()

        await bot.send_message(chat_id, main_menu_text, reply_markup=main_menu_keyboard)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# Catching http post request from make.com (From Photo analyze)
@app.post("/make_reply")
async def make_reply(request: Request):
    try:
        data = await request.json()

        # Getting and formating from make.com as string
        chat_id = int(data.get("chat_id"))
        dish_name = str(data.get("dish_name"))
        calories_estimated = int(data.get("calories_estimated"))
        protein_g = float(data.get("protein_g"))
        fat_g = float(data.get("fat_g"))
        carbs_g = float(data.get("carbs_g"))
        balance_assessment = str(data.get("balance_assessment"))

        result = await bot.send_message(
            chat_id,
            f"<b>🍽 {dish_name}</b>\n"
            f"<code>────────────────────────────</code>\n"
            f"📊 <b>Nutritional Value:</b>\n"
            f"  • Calories: <b>{calories_estimated}</b> kcal\n"
            f"  • Protein: <b>{protein_g}</b> g\n"
            f"  • Fat: <b>{fat_g}</b> g\n"
            f"  • Carbohydrates: <b>{carbs_g}</b> g\n\n"
            f"💬 <i>{balance_assessment}</i>",
            parse_mode="HTML"
        )

        await bot.send_message(chat_id, main_menu_text, reply_markup=main_menu_keyboard)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# Catching http post request from make.com (From Build Meal)
@app.post("/make_build")
async def make_reply(request: Request):
    try:
        data = await request.json()

        # Getting and formating from make.com as string
        chat_id = int(data.get("chat_id"))
        dish_name = str(data.get("dish_name"))
        calories_estimated = int(data.get("calories_estimated"))
        protein_g = float(data.get("protein_g"))
        fat_g = float(data.get("fat_g"))
        carbs_g = float(data.get("carbs_g"))
        cook_process = str(data.get("cook_process"))

        result = await bot.send_message(
            chat_id,
            f"<b>🍽 {dish_name}</b>\n"
            f"<code>────────────────────────────</code>\n"
            f"📊 <b>Nutritional Value:</b>\n"
            f"  • Calories: <b>{calories_estimated}</b> kcal\n"
            f"  • Protein: <b>{protein_g}</b> g\n"
            f"  • Fat: <b>{fat_g}</b> g\n"
            f"  • Carbohydrates: <b>{carbs_g}</b> g\n\n"
            f"👩‍🍳 <b>Cooking Process:</b>\n"
            f"<i>{cook_process}</i>",
            parse_mode="HTML"
        )

        await bot.send_message(chat_id, main_menu_text, reply_markup=main_menu_keyboard)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# Catching http post request from make.com (From Shop Helper)
@app.post("/make_shop_help")
async def make_reply(request: Request):
    try:
        data = await request.json()

        # Getting and formating from make.com as string
        chat_id = int(data.get("chat_id"))
        product_list = str(data.get("product_list"))

        result = await bot.send_message(
            chat_id,
            f"<b>🛒 Grocery list:</b>\n"
            f"<code>────────────────────────────</code>\n"
            f"{product_list}",
            parse_mode="HTML"
        )

        await bot.send_message(chat_id, main_menu_text, reply_markup=main_menu_keyboard)

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