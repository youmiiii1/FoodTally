import logging
from fastapi import Request
from aiogram.types import Update

from init import app, bot, dp, create_pool, close_pool
from handlers import main_menu, personal_info, photo_analyze, meal_report, build_meal
from database.meal_report import create_table_meal_report, new_report
from database.personal_info import create_table_users_info
from keyboards.main_menu import main_menu_keyboard
from texts.main_menu import main_menu_text
from config import WEBHOOK_URL_RAIL


# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    filemode='a',
    filename='logs.txt',
    format="%(asctime)s %(levelname)s %(message)s"
)


# ============================================================
# 1. MAKE.COM endpoints
# ============================================================

@app.post("/make_record")
async def make_record(request: Request):
    try:
        data = await request.json()

        chat_id = int(data["chat_id"])
        dish_name = str(data["dish_name"])
        calories_estimated = int(data["calories_estimated"])
        protein_g = float(data["protein_g"])
        fat_g = float(data["fat_g"])
        carbs_g = float(data["carbs_g"])
        balance_assessment = str(data["balance_assessment"])
        products_list = str(data["products_list"])

        await bot.send_message(
            chat_id,
            f"<b>🍽 {dish_name}</b>\n"
            f"──────────────────────\n"
            f"  • <b>Calories:</b> {calories_estimated} kcal\n"
            f"  • <b>Protein:</b> {protein_g} g\n"
            f"  • <b>Fat:</b> {fat_g} g\n"
            f"  • <b>Carbohydrates:</b> {carbs_g} g\n\n"
            f"<i>💬 {balance_assessment}</i>",
            parse_mode="HTML",
        )

        pool = await create_pool()
        await new_report(
            pool, chat_id, dish_name, calories_estimated,
            protein_g, fat_g, carbs_g, balance_assessment, products_list
        )
        await pool.close()

        await bot.send_message(chat_id, main_menu_text, reply_markup=main_menu_keyboard)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}


@app.post("/make_reply")
async def make_reply(request: Request):
    try:
        data = await request.json()

        chat_id = int(data["chat_id"])
        dish_name = str(data["dish_name"])
        calories_estimated = int(data["calories_estimated"])
        protein_g = float(data["protein_g"])
        fat_g = float(data["fat_g"])
        carbs_g = float(data["carbs_g"])
        balance_assessment = str(data["balance_assessment"])

        await bot.send_message(
            chat_id,
            f"<b>🍽 {dish_name}</b>\n"
            f"<code>────────────────────────────</code>\n"
            f"📊 <b>Nutritional Value:</b>\n"
            f"  • Calories: <b>{calories_estimated}</b> kcal\n"
            f"  • Protein: <b>{protein_g}</b> g\n"
            f"  • Fat: <b>{fat_g}</b> g\n"
            f"  • Carbohydrates: <b>{carbs_g}</b> g\n\n"
            f"💬 <i>{balance_assessment}</i>",
            parse_mode="HTML",
        )

        await bot.send_message(chat_id, main_menu_text, reply_markup=main_menu_keyboard)
        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}


@app.post("/make_build")
async def make_build(request: Request):
    try:
        data = await request.json()

        chat_id = int(data["chat_id"])
        dish_name = str(data["dish_name"])
        calories_estimated = int(data["calories_estimated"])
        protein_g = float(data["protein_g"])
        fat_g = float(data["fat_g"])
        carbs_g = float(data["carbs_g"])
        cook_process = str(data["cook_process"])

        await bot.send_message(
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
            parse_mode="HTML",
        )

        await bot.send_message(chat_id, main_menu_text, reply_markup=main_menu_keyboard)
        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}


@app.post("/make_shop_help")
async def make_shop_help(request: Request):
    try:
        data = await request.json()

        chat_id = int(data["chat_id"])
        product_list = str(data["product_list"])

        await bot.send_message(
            chat_id,
            f"<b>🛒 Grocery list:</b>\n"
            f"<code>────────────────────────────</code>\n"
            f"{product_list}",
            parse_mode="HTML",
        )

        await bot.send_message(chat_id, main_menu_text, reply_markup=main_menu_keyboard)
        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}


# ============================================================
# 2. TELEGRAM WEBHOOK ENDPOINT
# ============================================================

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}


# ============================================================
# 3. STARTUP / SHUTDOWN
# ============================================================

@app.on_event("startup")
async def on_startup():
    print("🚀 Bot startup (WEBHOOK MODE)")

    pool = await create_pool()
    dp['db_pool'] = pool

    await create_table_meal_report(pool)
    await create_table_users_info(pool)

    # Register routers
    dp.include_routers(
        main_menu.router,
        personal_info.router,
        photo_analyze.router,
        meal_report.router,
        build_meal.router,
    )

    # Установка Webhook
    webhook_full_url = f"{WEBHOOK_URL_RAIL}/webhook"
    await bot.delete_webhook()
    await bot.set_webhook(webhook_full_url)

    print(f"Webhook installed → {webhook_full_url}")


@app.on_event("shutdown")
async def on_shutdown():
    print("🛑 Shutdown...")

    await bot.delete_webhook()

    pool = dp.get('db_pool')
    if pool:
        await close_pool(pool)

    print("Webhook removed. DB pool closed.")

