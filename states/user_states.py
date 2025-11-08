from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    choose_category = State()
    choose_product = State()


class OrderStates(StatesGroup):
    name = State()
    phone_number = State()
    pickup_type = State()
    location = State()
    payment_type = State()
    pickup_location = State()
    detail = State()
