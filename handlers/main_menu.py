from aiogram import Router
from aiogram.filters import CommandStart
from keyboards.main_menu import main_menu_keyboard
from texts.main_menu import main_menu_text

router = Router()
user_last_message = {}

@router.message(CommandStart())
async def menu_handler(message):
    user_id = message.from_user.id

    if user_id in user_last_message:
        try:                                # message.chat.id — chat where the message should be deleted
            await message.bot.delete_message(message.chat.id, user_last_message[user_id])
        except:
            pass

    sent = await message.answer(main_menu_text, reply_markup=main_menu_keyboard)
    user_last_message[user_id] = sent.message_id # Save the new menu message_id (so we can delete it next time /start is pressed)

