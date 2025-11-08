from aiogram.fsm.state import State, StatesGroup


class CategoryStates(StatesGroup):
    name = State()


class ProductStates(StatesGroup):
    name = State()
    wieght = State()
    ingredients = State()
    photo = State()
    price = State()
    category_id = State()


class ConfirmationStates(StatesGroup):
    confirm_category = State()


class DeleteCategoryStates(StatesGroup):
    delete_category = State()
    confirm_delete = State()
    

class AddProductStates(StatesGroup):
    category_id = State()
    name = State()
    weight = State()
    ingredients = State()
    photo = State()
    price = State()
    confirm_saving = State()


class SendAdStates(StatesGroup):
    ad = State()
    confirm_ad = State()
