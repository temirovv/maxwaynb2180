from pathlib import Path

from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext

from loader import dp, ADMIN, baza, bot
from states.admin_states import AddProductStates
from keyboards.inline.admin_menu_kb import categories_kb, yes_or_no_kb


@dp.message(F.text=='/add_product', F.from_user.id.in_({ADMIN}))
async def add_product_handler(message: Message, state: FSMContext):
    await message.answer("Qaysi kategoriyaga mahsulot qo'shmoqchisiz?",
                          reply_markup=categories_kb())
    await state.set_state(AddProductStates.category_id)


@dp.callback_query(AddProductStates.category_id,  F.from_user.id.in_({ADMIN}))
async def getting_category_id_handler(call: CallbackQuery, state: FSMContext):
    category_id = call.data
    # Statega saqlash
    await state.update_data({"category_id": category_id})  
    # keyingi qadam
    await call.message.answer("FastFood nomini kiriting:")
    await call.answer("Done!", cache_time=60)
    await call.message.delete() # xabarni o'chirish
    await state.set_state(AddProductStates.name)


@dp.message(AddProductStates.name,  F.from_user.id.in_({ADMIN}))
async def add_product_name(message: Message, state: FSMContext):
    product_name = message.text
    # Statega saqlash
    await state.update_data({"product_name": product_name})
    await message.answer("FastFood vaznini kiriting: (grammda)")
    await state.set_state(AddProductStates.weight)


@dp.message(AddProductStates.weight,  F.from_user.id.in_({ADMIN}))
async def add_product_weight(message: Message, state: FSMContext):
    weight = message.text
    # Statega saqlash
    await state.update_data({"weight": weight})
    await message.answer("Ingredientlarni kiriting , m-n(Original Sendvich, Naggets qutisi, 0,3 L Coca Cola 2 ta. Tanlovga ko'ra 2 ta sous.)")
    await state.set_state(AddProductStates.ingredients)


@dp.message(AddProductStates.ingredients,  F.from_user.id.in_({ADMIN}))
async def add_product_ingredietns(message: Message, state: FSMContext):
    ingredients = message.text
    # Statega saqlash
    await state.update_data({"ingredients": ingredients})
    await message.answer("Rasmini yuboring!")

    await state.set_state(AddProductStates.photo)


@dp.message(
        AddProductStates.photo,  
        F.from_user.id.in_({ADMIN}), 
        F.content_type.in_({'photo',}))
async def add_product_ingredietns(message: Message, state: FSMContext):
    base_dir = Path(__file__).resolve().parents[1]        
    upload_dir = base_dir / "images" / "products"
    upload_dir.mkdir(parents=True, exist_ok=True)

    # 2) Telegram faylini olish
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    # 3) Faqat fayl nomini oling (masalan: "file_1.jpg")
    filename = Path(file.file_path).name
    dest_path = upload_dir / filename
    print(f'{dest_path=}')
    print(f'{filename=}')
    # 4) Yuklab saqlash
    # aiogram v3:
    await bot.download(file, destination=dest_path)

    # 5) Statega saqlash 
    await state.update_data(photo=str(dest_path.relative_to(base_dir)))
    await message.answer("✅ Rasm saqlandi.")
    await message.answer("Narxini yuboring:")
    await state.set_state(AddProductStates.price)

@dp.message(
        AddProductStates.price,  
        F.from_user.id.in_({ADMIN}))
async def add_product_ingredietns(message: Message, state: FSMContext):
    price = message.text
    await state.update_data({"price": price})
    await message.answer(
        "Kiritilgan ma'lumotlar to'g'rimi?",
        reply_markup=yes_or_no_kb()
    )
    await state.set_state(AddProductStates.confirm_saving)


@dp.callback_query(AddProductStates.confirm_saving, F.data == 'no', F.from_user.id.in_({ADMIN}))
async def cancel_saving_product(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer("Operation cancelled")
    await call.message.delete()


@dp.callback_query(AddProductStates.confirm_saving, F.data == 'yes', F.from_user.id.in_({ADMIN}))
async def cancel_saving_product(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)

    # saving logic
    category_id = data.get("category_id")
    product_name = data.get("product_name")
    ingredients = data.get("ingredients")
    photo = data.get("photo")
    weight = data.get("weight")
    price = data.get("price")

    baza.add_product(
        name=product_name,
        weight=int(weight),
        ingredients=ingredients,
        photo=photo,
        price=float(price),
        category_id=int(category_id)
    )

    # clearing states
    await state.clear()
    await call.answer("Products has been saved!")
    await call.message.delete()