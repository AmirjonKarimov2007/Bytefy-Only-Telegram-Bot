from aiogram.dispatcher.filters.state import State, StatesGroup


class PAGES_STATES(StatesGroup):
    PAGES_STATES_SERVICES= State()
    PAGES_STATES_WORKS= State()
    PAGES_STATES_CONTACT= State()


class application(StatesGroup):
    fullname= State()
    phone_number = State()  
    