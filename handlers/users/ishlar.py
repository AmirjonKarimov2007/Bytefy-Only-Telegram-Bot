from aiogram import types 
from loader import db,dp,bot
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton
from data.config import ADMINS
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

ADMINS = [int(i) for i in ADMINS] 
# from aiogram.dispatcher.filters.state import State, StatesGroup
user_selected_services = {
    # Example user_id: [service_ids]
}

from keyboards.inline.pages_keyboard import create_online_offline_markup,works_services
@dp.callback_query_handler(lambda c: c.data in ['order'], state='*')
async def choose_service_type(call: types.CallbackQuery):
    markup = await create_online_offline_markup()
    await call.message.edit_text("Ish turini tanlang:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'Offline', state='*')
async def show_offline_services(callback_query: CallbackQuery):
    new_markup = await works_services()
    await callback_query.message.edit_text("Offline xizmatlar ro'yxati:", reply_markup=new_markup)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith('offline:select_servic:'), state='*')
async def handle_service_selection(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    service_id = str(callback_query.data.split(':')[2])
    
    if user_id not in user_selected_services:
        user_selected_services[user_id] = []

    
    if service_id in user_selected_services[user_id]:
        user_selected_services[user_id].remove(service_id)

    else:
        user_selected_services[user_id].append(service_id)
        # print(user_selected_services)

    new_markup = await works_services(user_selected_services[user_id])
    
    try:
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=new_markup)
    except MessageNotModified:
        pass  
    await bot.answer_callback_query(callback_query.id)
from pdf_generator import create_pdf
@dp.callback_query_handler(lambda c: c.data == 'finalize_selection', state='*')
async def handle_finalize_selection(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    selected_services = user_selected_services.get(user_id, [])
    services = {}

    # Agar hech qanday xizmat tanlanmagan bo'lsa, xabar chiqaring
    if not selected_services:
        await bot.send_message(callback_query.message.chat.id, "Hali xizmat tanlamadingiz")
        await bot.answer_callback_query(callback_query.id)
        return

    # Xizmatlarni lug'atga qo'shing
    for i, service in enumerate(selected_services, 1):
        services[i] = {"name": service}

    # PDF yaratish va foydalanuvchiga xizmatlar ro'yxatini yuborish
    pdf_path = rf"invoyslar/{callback_query.from_user.id}.pdf"
    pdf = await create_pdf(pdf_path, services, callback_query.from_user.first_name, callback_query.from_user.last_name, "Amirjon Karimov")
    with open(pdf_path, 'rb') as pdf_file:
        await bot.send_document(
            chat_id=callback_query.message.chat.id,
            document=pdf_file,
            caption=f"{callback_query.from_user.first_name} bu sizning invoysingiz.\n\nIltimos uni ehtiyot qiling"
        )
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=await works_services())


    user_selected_services[callback_query.from_user.id] = []

