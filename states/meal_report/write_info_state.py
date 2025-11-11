from aiogram.fsm.state import State, StatesGroup

class WriteInfoStates(StatesGroup):
    waiting_for_dish_name = State()
    waiting_for_calories_estimated = State()
    waiting_for_protein_g = State()
    waiting_for_fat_g = State()
    waiting_for_carbs_g = State()
    waiting_for_balance_assessment = State()
