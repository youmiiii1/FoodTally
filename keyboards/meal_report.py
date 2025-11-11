from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

meal_report_menu = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text='Photo Report', callback_data='photo_report'),
            InlineKeyboardButton(text= 'Write Report', callback_data='write_report')
        ],
        [
            InlineKeyboardButton(text='Get records', callback_data='get_records')
        ],
        [
            InlineKeyboardButton(text='To menu', callback_data='to_menu')
        ],
    ],
)

