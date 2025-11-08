from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from loader import dp, baza, bot
from keyboards.default.user_menu_kb import make_categories_menu,\
      make_products_menu, \
      make_plus_minus_menu, get_main_menu
from states.user_states import UserStates
from keyboards.inline.cart_menu import get_user_cart


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Xush kelibsiz!",
        reply_markup=get_main_menu()
    )
    tg_id = message.from_user.id
    if not baza.check_user(tg_id=tg_id):
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        baza.add_user(tg_id, first_name, last_name, username)
    

@dp.message(F.text == "Menyu")
async def menyu_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Kategoriyalardan birini tanlang!",
        reply_markup=make_categories_menu()
    )
    await state.set_state(UserStates.choose_category)


@dp.message(UserStates.choose_category, F.text == '◀️ Orqaga')
async def back_to_main_menu_handler(message: Message, state: FSMContext):
    await message.answer("Bosh menyu", reply_markup=get_main_menu())
    await state.clear()


@dp.message(UserStates.choose_category)
async def choose_category_handler(message: Message, state: FSMContext):
    category = message.text
    result = baza.check_category(category)
    if result:
        await message.answer(
            f"{category} lardan birini tanlang!",
            reply_markup=make_products_menu(category)
        )
        await state.set_state(UserStates.choose_product)
    else:
        await message.answer("Tugmalardan birini bosing!")


@dp.message(UserStates.choose_product, F.text == '◀️ Orqaga')
async def back_to_category_handler(message: Message, state: FSMContext):
    await message.answer('Kategoriyalardan birini tanlang!', reply_markup=make_categories_menu())
    await state.set_state(UserStates.choose_category)


@dp.message(UserStates.choose_product)
async def choose_product_handler(message: Message, state: FSMContext):
    product_name = message.text
    result = baza.check_product(product_name)

    if result:
        data = baza.select_product_by_name(product_name)
        p_id, name, weight, ingredients, photo, price, category_id = data
        text = f"""{name}\nvazni{weight} gr\ntarkibi: {ingredients}\nnarxi: {price} so'm"""
        file = FSInputFile(path=photo)
        print(f"{data}=")
        user_id = message.from_user.id
        data = {
                'p_id': p_id,
                'count': 1,
                'text': text,
                'photo': photo,
                'price': price
        }
        await state.update_data(
            {user_id: data}
        )
        await message.answer_photo(
            photo=file, 
            caption=text,
            reply_markup=make_plus_minus_menu(p_id=p_id)    
        )
    else:
        await message.answer("Tugmalardan birini bosing!")


@dp.callback_query(UserStates.choose_product, F.data == 'plus')
async def plust_cart_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    user_data = data.get(user_id)
    text = user_data.get("text")
    p_id = user_data.get('p_id')
    count = user_data.get('count')
    count += 1

    await call.message.edit_reply_markup(
        reply_markup=make_plus_minus_menu(p_id=p_id, count=count) 
    )
    user_data.update({'count': count})
    
    await state.update_data({user_id: user_data})


@dp.callback_query(UserStates.choose_product, F.data == 'add_to_cart')
async def add_to_cart(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    user_data = data.get(user_id)
    p_id = user_data.get('p_id')
    count = user_data.get('count')
    price = user_data.get('price')
    total_price = count * price
    print(total_price)
    baza.add_to_cart(
        user_id, p_id, total_price, count
    )
    
    await state.clear()
    await call.answer("Mahsulot savatga qo'shildi")
    await call.message.answer('Bosh menyu',reply_markup=get_main_menu())
    await call.message.delete()


@dp.message(F.text == "Savatcha")
async def cart_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    menu, exists = get_user_cart(user_id)
    if exists:

        await message.answer(
            text="Savatingizda...",
            reply_markup=menu
        )
    else:
        await message.answer('Savatingiz hozircha bo\'sh')

@dp.callback_query(F.data.startswith('cart_item_delete'))
async def cart_item_delete_handler(call: CallbackQuery):
    data = call.data.split('.')
    cart_id = int(data[-1])
    baza.delete_cart_item(cart_id)
    await call.answer('O\'chirildi')

    user_id = call.from_user.id
    menu, exists = get_user_cart(user_id)
    if exists:
        await call.message.edit_reply_markup(reply_markup=menu)
    else:
        await call.message.answer('savatingizda hech narsa qolmadi')
        await call.message.delete()


@dp.callback_query(F.data == 'clear_cart')
async def clear_cart_handler(call: CallbackQuery):
    user_id = call.from_user.id
    baza.clear_user_cart(user_id)
    await call.answer("Savatingiz tozalandi!")
    await call.message.delete()


