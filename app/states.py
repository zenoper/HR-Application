from aiogram.fsm.state import StatesGroup, State


class FormStates(StatesGroup):
    waiting_for_template = State()
    waiting_for_data = State()
