from aiogram.dispatcher.filters.state import State, StatesGroup

class users_states(StatesGroup):
    homepage = State()
    locked   = State()
