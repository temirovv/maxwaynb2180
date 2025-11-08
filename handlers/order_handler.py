import re

from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from loader import dp, baza, bot
from states.user_states import OrderStates
from keyboards.inline.order_menu import get_pickup_type_kb


@dp.callback_query(F.data == 'order_')
async def order_handler(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ismingizni kiriting!")
    await state.set_state(OrderStates.name)


@dp.message(OrderStates.name)
async def order_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data({'name': name})
    
    await message.answer("telefon raqamingizni kiriting")
    await state.set_state(OrderStates.phone_number)


@dp.message(OrderStates.phone_number)
async def order_phone_number_handler(
    message: Message, state: FSMContext):
    text = message.text
    pattern = r'^(?:\+?998[\s\-]?)?(?:\(?\d{2}\)?[\s\-]?)?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
    pattern = re.compile(pattern)
    if bool(pattern.match(text)):
        await state.update_data({'phone_number': text})
        await state.set_state(OrderStates.pickup_type)
        await message.answer("Yetkazib berish turini tanlang",
                             reply_markup=get_pickup_type_kb())
    else:
        await message.answer('noto\'g\'ri raqam kiritdingiz')
        await message.answer('qayta urinib ko\'ring')


@dp.callback_query(OrderStates.pickup_type)
async def order_pickup_type_handler(call: CallbackQuery, state: FSMContext):
    pickup_type = call.data
    if pickup_type == 'yetkazib_berish':
        pass
    elif pickup_type == 'olib_ketish':
        pass
    await call.answer("Tugadi shotgacha edi")
    await state.clear()