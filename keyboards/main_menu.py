from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Photo Analyze', callback_data='photo_analyze'),
            InlineKeyboardButton(text='Build Meal', callback_data='build_meal')
        ],

        [
            InlineKeyboardButton(text='Meal Report', callback_data='meal_report'),
            InlineKeyboardButton(text='Personal Info', callback_data='personal_info')
        ],
    ],

)