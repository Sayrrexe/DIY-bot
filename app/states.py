from aiogram.fsm.state import State, StatesGroup


class QuestionsFsm(StatesGroup):
    user = State()
    color = State()
    form = State()
    additives = State()