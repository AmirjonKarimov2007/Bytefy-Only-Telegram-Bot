from loader import db,bot,dp
from aiogram import types
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from magic_filter import F
from keyboards.inline.pages_keyboard import services_keyboard,service_keyboard,package_keyboard
from states.pages_state import PAGES_STATES,application
from aiogram.dispatcher import FSMContext

from aiogram.utils.exceptions import MessageNotModified

@dp.callback_query_handler(text="services", state='*')
async def services(call: types.CallbackQuery):
    try:
        await call.answer(cache_time=1)
    except:
         await call.answer(cache_time=1)

    markup = await services_keyboard()
    new_text = "<b>Xizmatlarimiz Haqida Malumot olishingiz mumkin!</b>"

    if call.message.text != new_text or call.message.reply_markup != markup:
        try:
            await call.message.edit_text(text=new_text, reply_markup=markup)
        except MessageNotModified:
            pass  
    else:
        await call.answer("Message is already up to date.", show_alert=False)

@dp.callback_query_handler(text_contains='service:',state='*')
async def service_packages(call: types.CallbackQuery):
    try:
        await call.answer(cache_time=1)
    except:
         await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    id = data[1]
    services = await db.select_all_services(id=int(id))
    markup = await service_keyboard(services)

    service = await db.select_service(id=int(id))

    text = f"<b><a href=\"{service[0]['photo']}\">{service[0]['fullname']}ning Tarif rejalari! </a></b>\n\n"
    text+=f"<b>{service[0]['description']}</b>\n\n"
    for servis in services:
        text+=f"<b>🔰{servis[0]['fullname']}: {servis[0]['price']}💲\n</b>"

    text+=f"\n<b>Bizning Kanal:👉 @Euro_Asia_Project_Rasmiy</b>"
    
    await call.message.edit_text(text=text,reply_markup=markup)


@dp.callback_query_handler(text_contains='packages:',state='*')
async def service_packages(call: types.CallbackQuery):
    try:
        await call.answer(cache_time=1)
    except:
         await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    id = data[1]
    service_id = data[2]
    service = await db.select_all_services(service_id=int(service_id),iid=int(id))
    name = await db.select_service(id=int(service_id))
    service_name = name[0]['fullname']
    for servis in service:
        package_name = servis[0]['fullname']
    text = f"<b><a href='{name[0]['photo']}'>{service_name} Xizmatimizning {package_name} paketi</a></b>\n\n"
    text += f"<b>▪️Qulayliklar</b>\n"
    text +=f"<b>{servis[0]['description']}</b>\n"
    text+=f"\n<b>Bizning Kanal:👉 @Euro_Asia_Project_Rasmiy</b>"
    package_id = iid=int(id)
    markup = await package_keyboard(service_id,package_id)
    await call.message.edit_text(text=text,reply_markup=markup)

@dp.callback_query_handler(text_contains='info:',state='*')
async def buy(call: types.CallbackQuery,state: FSMContext):
    try:
        await call.answer(cache_time=1)
    except:
         await call.answer(cache_time=1)

    data = call.data.rsplit(":")
    service_id = data[2]
    package_id = data[4]
    service = await db.select_service(id=int(service_id))
    service_package = await db.select_all_services(service_id=int(service_id),iid=int(package_id))
    await state.update_data({'service_id': {int(service_id)}})

    service_name = service[0]['fullname']
    package = service_package[0][0]['fullname']
    await state.update_data({'package': {package}})
    text = f"🪪Iltimos adminlar siz bilan bog'lanishi uchun ismingizni yuboring."
    await call.message.edit_reply_markup()
    await call.message.delete()
    await call.message.answer(text=text)

    await application.fullname.set()
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
@dp.message_handler(state=application.fullname)
async def get_name(message: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="☎️Yuborish",request_contact=True))

    try:
        if message.text:
            await state.update_data({'fullname': {message.text}})
            await message.answer("<b>😊Katta raxmat\n☎️Endi telefon raqamingizni jo'nating.</b>",reply_markup=keyboard)
            await application.phone_number.set()
        else:
            await message.answer("❌Iltimos ismingizni yuboring!", reply_markup=ReplyKeyboardRemove())
            await application.fullname.set()
    except:
        await state.finish()
        await message.answer("Iltimos Ariza boshidan boshlang,xatolik yuzaga keldi.", reply_markup=ReplyKeyboardRemove())
from data.config import ADMINS
@dp.message_handler(state=application.phone_number, content_types=types.ContentType.CONTACT)
async def phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    username = message.from_user.username

    data = await state.get_data()
    name = str(next(iter(data.get('fullname'))))
    service_id = data.get('service_id')
    package = str(next(iter(data.get('package'))))
    service_id = int(next(iter(service_id)))  
    keyboard = await services_keyboard()
    id = 1443915256
    try:
        await db.add_requests(name=name, username=str(username),
                              user_id=int(user_id), phone_number=phone_number,
                              service_id=int(service_id), selected_package=package)
        await message.answer("<b>✅ Arizangiz qabul qilindi\n</b>", reply_markup=ReplyKeyboardRemove())
        await message.answer("<b>👤 Adminlarimiz tez orada siz bilan bog'lanishadi</b>",reply_markup=keyboard)
        msg = f"<b>👋 Assalomu Aleykum Xurmatli admin, sizga <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a> tomonidan yangi ariza mavjud.</b>\n\n"
        msg += f"<b>👤Arizaching ismi:{name}</b>\n"
        msg += f"<b>🆔ID:{user_id}</b>\n"
        msg += f"<b>🔰Username: @{username}</b>\n"
        msg += f"<b>📞Telefon Raqam:{phone_number}</b>\n"
        msg += f"<b>☑️Xizmat_ID:{service_id}</b>\n"
        msg += f"<b>💸Xizmt Turi:{package}</b>\n"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text=f"Bog'lanish",url=f"tg://user?id={user_id}"))
        markup.add(InlineKeyboardButton(text=f"ID orqali",url=f"t.me/{username}"))
        for admin in ADMINS:
            await bot.send_message(chat_id=admin,text=msg,reply_markup=markup)

        await state.finish()
    except Exception as e:
        await message.answer(f"{e}")






    

















# from data.product import python_book, ds_praktikum,  FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
# @dp.callback_query_handler(text="product:book")
# async def book_invoice(call: types.CallbackQuery):
#     await bot.send_invoice(chat_id=call.from_user.id,
#                            **python_book.generate_invoice(),
#                            payload="123456798965")
#     await call.answer(text='tolov amalga oshdi')

# @dp.shipping_query_handler()
# async def choose_shipping(query: types.ShippingQuery):
#     if query.shipping_address.country_code != "UZ":
#         await bot.answer_shipping_query(shipping_query_id=query.id,
#                                         ok=False,
#                                         error_message="Chet elga yetkazib bera olmaymiz")
#     elif query.shipping_address.city.title() == "tashkent":
#         await bot.answer_shipping_query(shipping_query_id=query.id,
#                                         shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
#                                         ok=True)
#     else:
#         await bot.answer_shipping_query(shipping_query_id=query.id,
#                                         shipping_options=[REGULAR_SHIPPING],
#                                         ok=True)

# from data.config import ADMINS
# @dp.pre_checkout_query_handler()
# async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
#                                         ok=True)
#     await bot.send_message(chat_id=pre_checkout_query.from_user.id,
#                            text="Xaridingiz uchun rahmat!")
#     await bot.send_message(chat_id=ADMINS[0],
#                            text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
#                                 f"ID: {pre_checkout_query.id}\n"
#                                 f"Telegram user: {pre_checkout_query.from_user.first_name}\n"                                
#                                 f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}")