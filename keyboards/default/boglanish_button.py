from aiogram import types
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton
from loader import dp

home = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="✅Boshlash")
    ],],
    resize_keyboard=True
)

check = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅Ha"),
            KeyboardButton(text="❌Yo'q")
        ],
    ],
    resize_keyboard=True
)
