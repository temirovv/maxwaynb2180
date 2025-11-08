from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError

from loader import dp, ADMIN, baza
from states.admin_states import CategoryStates, ConfirmationStates, \
    DeleteCategoryStates, SendAdStates
from keyboards.inline.admin_menu_kb import yes_or_no_kb, categories_kb



@dp.message(F.text=='/add_category', F.from_user.id.in_({ADMIN}))
async def add_category_command_handler(message: Message, state: FSMContext):
    await message.answer("Kategoriya nomini kiriting")
    await state.set_state(CategoryStates.name)


@dp.message(CategoryStates.name, F.from_user.id.in_({ADMIN}))
async def add_category_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data({'name': name})
    await message.answer(f"name: {name}\nbazaga saqlaymi?", 
                         reply_markup=yes_or_no_kb())
    await state.set_state(ConfirmationStates.confirm_category)


@dp.callback_query(ConfirmationStates.confirm_category, F.data == 'no')
async def deny_saving_category_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Operatsiya rad etildi!")
    await call.message.delete()
    await state.clear()

@dp.callback_query(ConfirmationStates.confirm_category, F.data == 'yes')
async def deny_saving_category_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    if name:
        baza.add_category(name)
        await call.answer("Category added successfully!")
    else:
        await call.answer("Category name is empty!")

    await call.message.delete()
    await state.clear()
    
    
# DELETE CATEGORIES
@dp.message(F.text == '/delete_categories', F.from_user.id.in_({ADMIN}))
async def delete_category_command_handler(message: Message, state: FSMContext):
    await message.answer("O'chirmoqchi bo'lgan kategoriyangizni tanlang",
                         reply_markup=categories_kb())
    await state.set_state(DeleteCategoryStates.delete_category)
    

@dp.callback_query(DeleteCategoryStates.delete_category)
async def delete_category_callback_handler(call: CallbackQuery, state: FSMContext):
    category_id = call.data
    await state.update_data({'category_id': category_id})
    category_name = baza.get_category_by_id(category_id)
    await call.message.answer(
        f"{category_name} ni o'chirmoqchimisiz?",
        reply_markup=yes_or_no_kb()
    )
    await call.message.delete()
    await state.set_state(DeleteCategoryStates.confirm_delete)

@dp.callback_query(DeleteCategoryStates.confirm_delete, F.data == 'no')
async def cancelling_delete_category(call: CallbackQuery, state: FSMContext):
    await call.answer("Operation cancelled!")
    await state.clear()
    await call.message.delete()

@dp.callback_query(DeleteCategoryStates.confirm_delete, F.data == 'yes')
async def cancelling_delete_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_id = data.get("category_id")
    baza.delete_category(category_id)
    await state.clear()
    await call.answer("category has been deleted")
    await call.message.delete()


@dp.message(F.text == '/send_ad', F.from_user.id.in_({ADMIN}))
async def send_ad_command_handler(message: Message, state: FSMContext):
    await message.answer("reklama xabarini yuboring")
    await state.set_state(SendAdStates.ad)


@dp.message(SendAdStates.ad, F.from_user.id.in_({ADMIN}))
async def send_ad_handler(message: Message, state: FSMContext):
    await message.answer("Shu reaklamani jo'nataymi?")
    await message.send_copy(chat_id=message.from_user.id, reply_markup=yes_or_no_kb())


@dp.callback_query(SendAdStates.ad, F.from_user.id.in_({ADMIN}), F.data == 'no')
async def cancelling_ad_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Reklama jo'natish bekor qilindi")
    await call.message.delete()
    await state.clear()

@dp.callback_query(SendAdStates.ad, F.from_user.id.in_({ADMIN}),
                    F.data == 'yes')
async def cancelling_ad_handler(call: CallbackQuery, state: FSMContext):
    users = baza.select_users_tg_id()
    message = call.message
    blocked_chat_count = 0
    for user in users:
        try:
            await message.send_copy(chat_id=user[0],
                                     reply_markup=ReplyKeyboardRemove())
        except TelegramForbiddenError:
            blocked_chat_count += 1
            print(f"{user} botni bloklagan")

    await call.message.answer(
        f"{blocked_chat_count} ta user botni bloklagan")
    await call.answer("Reklama jo'natildi")
    await call.message.delete()
    await state.clear()