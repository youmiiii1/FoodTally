from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove
from keyboards.personal_info import personal_info, male_or_female, choose_goal
from keyboards.main_menu import main_menu_keyboard
from texts.main_menu import main_menu_text
from texts.personal_information.personal_info import personal_info_menu
from texts.personal_information.add_info import (enter_age,
                                                 enter_height,
                                                 enter_goal,
                                                 enter_gender,
                                                 enter_weight,
                                                 wrong_age, age_not_int,
                                                 wrong_height,
                                                 height_not_float,weight_not_float, wrong_weight,
                                                 wrong_gender, gender_not_f_or_m, goal_not_in_list,
                                                 wrong_goal, close_personal_info_state)
from states.personal_info.add_info_states import ProfileSetup
from database.personal_info import new_user, create_pool, user_exists, change_user_info, user_personal_info

router = Router()

@router.callback_query(F.data == 'personal_info')
async def personal_info_handler(call, db_pool):
    telegram_id = call.from_user.id
    formated_personal_info = await user_personal_info(db_pool, telegram_id)
    await call.message.edit_text(f"{personal_info_menu}{formated_personal_info}", reply_markup=personal_info)
    await call.answer()

# States for personal_info/add_info
@router.callback_query(F.data == 'add_info')
async def add_info_handler(call, state):
    await state.set_state(ProfileSetup.waiting_for_age)
    await call.message.answer(enter_age)
    await call.answer()

# Age state handler
@router.message(ProfileSetup.waiting_for_age)
async def process_age(message, state):
    try:
        age = int(message.text)

        if 10 <= age <= 100:
            await state.update_data(age=age)
            await state.set_state(ProfileSetup.waiting_for_height)
            await message.answer(enter_height)

        else:
            await message.answer(wrong_age)

    except ValueError:
        await message.answer(age_not_int)

# Height state handler
@router.message(ProfileSetup.waiting_for_height)
async def process_height(message, state):
    try:
        height = float(message.text)

        if 40 <= height <= 300:
            await state.update_data(height=height)
            await state.set_state(ProfileSetup.waiting_for_weight)
            await message.answer(enter_weight)

        else:
            await message.answer(wrong_height)

    except ValueError:
        await message.answer(height_not_float)

# Weight state handler
@router.message(ProfileSetup.waiting_for_weight)
async def process_weight(message, state):
    try:
        weight = float(message.text)

        if 30<= weight <=150:
            await state.update_data(weight=weight)
            await state.set_state(ProfileSetup.waiting_for_gender)
            await message.answer(enter_gender, reply_markup=male_or_female)

        else:
            await message.answer(wrong_weight)

    except ValueError:
        await message.answer(weight_not_float)

# Gender state handler
@router.message(ProfileSetup.waiting_for_gender)
async def process_gender(message, state):
    try:
        gender = str(message.text.upper())

        if gender in ('M','F'):
            await state.update_data(gender=gender)
            await state.set_state(ProfileSetup.waiting_for_goal)
            await message.answer(enter_goal, reply_markup = choose_goal)

        else:
            await message.answer(wrong_gender)

    except ValueError:
        await message.answer(gender_not_f_or_m)

# Goal / Telegram_id state handler
@router.message(ProfileSetup.waiting_for_goal)
async def process_goal(message, state, db_pool):
    try:
        goal = str(message.text.strip().lower())

        if goal in ('lose weight', 'maintain', 'gain muscle'):
            await state.update_data(goal=goal)

            data = await state.get_data()

            telegram_id = message.from_user.id
            age = data['age']
            height = data['height']
            weight = data['weight']
            gender = data['gender']
            goal = data['goal']

            if await user_exists(db_pool, telegram_id):
                await change_user_info(db_pool, telegram_id, age, height, weight, gender, goal)
                await state.clear()
                await message.answer(close_personal_info_state, reply_markup=ReplyKeyboardRemove())

                formated_personal_info = await user_personal_info(db_pool, telegram_id)
                await message.answer(f"{personal_info_menu}{formated_personal_info}", reply_markup=personal_info)

            else:
                await new_user(db_pool, telegram_id, age, height, weight, gender, goal)
                await state.clear()
                await message.answer(close_personal_info_state, reply_markup=ReplyKeyboardRemove())
                await message.answer(personal_info_menu, reply_markup=personal_info)

        else:
            await message.answer(wrong_goal)

    except ValueError:
        await message.answer(goal_not_in_list)

# Button 'Change personal' information
@router.callback_query(F.data == 'change_info')
async def change_info_handler(call, state):
    await state.set_state(ProfileSetup.waiting_for_age)
    await call.message.answer(enter_age)
    await call.answer()

# Button back to menu
@router.callback_query(F.data == 'cancel')
async def to_menu_handler(call):
    await call.message.edit_text(main_menu_text, reply_markup=main_menu_keyboard)
    await call.answer()