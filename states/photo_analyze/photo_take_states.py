from aiogram.fsm.state import State, StatesGroup

class PhotoTaker(StatesGroup):
    waiting_for_photo = State()