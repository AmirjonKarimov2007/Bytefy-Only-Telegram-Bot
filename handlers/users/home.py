from loader import db,bot,dp
from aiogram.types import Message,Update,CallbackQuery

from keyboards.inline.pages_keyboard import home_keyboard
@dp.message_handler(text='✅Boshlash')
@dp.callback_query_handler(text='home', state='*')
async def home_page(update: Update):
    try:
        await update.answer(cache_time=1)
    except:
        pass
    if isinstance(update, Message):
        home_btn = await home_keyboard(update.from_user.id)

        await update.answer("<b>Bo'limni Tanlang!</b>", reply_markup=home_btn)
    elif isinstance(update, CallbackQuery):
        home_btn = await home_keyboard(update.from_user.id)

        try:
            await update.answer(cache_time=1)
        except:
            pass
        try:
            await update.message.edit_text("<b>Bo'limni Tanlang!</b>", reply_markup=home_btn)
        except Exception as e:
            await update.message.answer("<b>Bo'limni Tanlang!</b>", reply_markup=home_btn)
