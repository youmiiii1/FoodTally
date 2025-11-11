import requests
import asyncio
from init import bot
from aiogram import Router, F
from config import WEB_HOOK_URL
from texts.photo_analyze import (photo_analyze_menu, bot_took_photo, web_hook_sent_photo)
from texts.main_menu import main_menu_text
from keyboards.photo_analyze import photo_analyze_keyboard
from keyboards.main_menu import main_menu_keyboard
from states.photo_analyze.photo_take_states import PhotoTaker
from database.personal_info import user_personal_info


router = Router()

@router.callback_query(F.data == 'back_to_menu')
async def cancel_button_handler(call):
    await call.message.edit_text(main_menu_text, reply_markup=main_menu_keyboard)
    await call.answer()

@router.callback_query(F.data == 'photo_analyze')
async def photo_analyze_handler(call, state):
    await state.set_state(PhotoTaker.waiting_for_photo)
    await state.update_data(mode='analyze')

    msg = await call.message.edit_text(photo_analyze_menu, reply_markup=photo_analyze_keyboard)
    await state.update_data(msg_id=msg.message_id)
    await state.update_data(chat_id=msg.chat.id)

    await call.answer()

# Taking photo from user and sending by web-hook to make.com
@router.message(PhotoTaker.waiting_for_photo, F.photo)
async def photo_handler(message, state, db_pool):
    await message.answer(bot_took_photo)

    file_id = message.photo[-1].file_id

    data = await state.get_data()
    mode = data.get("mode", "analyze")
    time = data.get("time", None)

    user_info = await user_personal_info(db_pool, message.from_user.id)

    json_pack = {
        "fileId": file_id,
        "chat_id": message.chat.id,
        "operation": mode,
        'time': time,
        'user_info': user_info
    }

    await asyncio.sleep(2)

    # Sending request by webhook to make.com
    try:
        resp = requests.post(WEB_HOOK_URL, json=json_pack, timeout=10)
        if resp.status_code == 200:
            await message.answer(web_hook_sent_photo)

            data = await state.get_data()
            msg_id = data['msg_id']
            chat_id = data['chat_id']

            if chat_id and msg_id:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)

        else:
            await message.answer(f"Error: {resp.status_code}")

    except Exception as e:
        await message.answer(f"Sent request error: {e}")

    finally:
        await state.clear()

