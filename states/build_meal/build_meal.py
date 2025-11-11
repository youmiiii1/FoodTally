from aiogram.fsm.state import State, StatesGroup

class ShopHelpState(StatesGroup):
    waiting_for_list_product = State()