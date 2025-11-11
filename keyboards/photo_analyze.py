from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

photo_analyze_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Cancel', callback_data='back_to_menu')
        ],
    ],
)