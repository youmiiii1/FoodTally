import asyncio
import requests
from config import WEB_HOOK_URL
from init import bot
from aiogram import Router, F
from datetime import datetime, timezone
from keyboards.build_meal import build_meal_menu
from keyboards.photo_analyze import photo_analyze_keyboard
from states.build_meal.build_meal import ShopHelpState
from states.photo_analyze.photo_take_states import PhotoTaker
from database.meal_report import show_product_list
from texts.build_meal import build_meal_menu_text, shop_helper_run, web_hook_sent, photo_build_button

router = Router()

@router.callback_query(F.data == "build_meal")
async def build_meal_handler(call):
    await call.message.edit_text(build_meal_menu_text, reply_markup=build_meal_menu)
    await call.answer()

@router.callback_query(F.data == "photo_build")
async def photo_build_handler(call, state):
    await state.set_state(PhotoTaker.waiting_for_photo)

    await state.update_data(mode='build')
    current_time = datetime.now(timezone.utc).isoformat()
    await state.update_data(time=current_time)

    msg = await call.message.edit_text(photo_build_button, reply_markup=photo_analyze_keyboard)
    await state.update_data(msg_id=msg.message_id)
    await state.update_data(chat_id=msg.chat.id)

    await call.answer()

@router.callback_query(F.data == "shop_helper")
async def shop_helper_handler(call, state, db_pool):
    await call.message.answer(shop_helper_run)
    await state.set_state(ShopHelpState.waiting_for_list_product)

    telegram_id = call.from_user.id
    await state.update_data(
        telegram_id=telegram_id,
        msg_id=call.message.message_id,
        chat_id=call.message.chat.id
    )

    product_list = await show_product_list(db_pool, telegram_id)
    await state.update_data(
        product_list=product_list,
        operation="shop"
    )

    await call.answer()

    data = await state.get_data()
    chat_id = data.get('chat_id')

    json_pack = {
        "product_list": product_list,
        "chat_id": chat_id,
        "operation": "shop"
    }

    await asyncio.sleep(2)

    # Sending request by webhook to make.com
    try:
        resp = requests.post(WEB_HOOK_URL, json=json_pack, timeout=10)
        if resp.status_code == 200:
            await call.message.answer(web_hook_sent)

            data = await state.get_data()
            msg_id = data.get('msg_id')
            chat_id = data.get('chat_id')

            if chat_id and msg_id:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        else:
            await call.message.answer(f"Error: {resp.status_code}")

    except Exception as e:
        await call.message.answer(f"Sent request error: {e}")

    finally:
        await state.clear()