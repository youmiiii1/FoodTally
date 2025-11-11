from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

build_meal_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Photo Build', callback_data='photo_build'),
            InlineKeyboardButton(text='Shop Helper', callback_data='shop_helper')
        ],
        [
            InlineKeyboardButton(text='To menu', callback_data='to_menu')
        ],
    ],
)