from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

personal_info = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Add information', callback_data='add_info'),
            InlineKeyboardButton(text='Change information', callback_data='change_info')
        ],
        [
            InlineKeyboardButton(text='To menu', callback_data='cancel')
        ],
    ],
)

male_or_female = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'F'),
            KeyboardButton(text = 'M')
        ],
    ],
    resize_keyboard=True
)

choose_goal = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Lose weight'),
            KeyboardButton(text = 'Maintain'),
            KeyboardButton(text = 'Gain muscle')
        ],
    ],
    resize_keyboard=True
)