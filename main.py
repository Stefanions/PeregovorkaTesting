import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from app.config import TOKEN
from datetime import datetime, timedelta, date

import app.keyboard as kb

print("комит в новой ветке")

bot = Bot(token = TOKEN)
dp = Dispatcher()

class st(StatesGroup):
    st_book = State()
    st_cancel = State()
    st_check = State()

#Приветственное сообщение
@dp.message(CommandStart())
async def hi(message: Message):
    await message.answer('Приветствую, данный бот предназначен для оптимизации работы переговорной.', reply_markup=kb.menu)

#Главное меню
@dp.callback_query(F.data.startswith('action_'))
async def handle_action(callback_query: CallbackQuery, state: FSMContext):
    action = callback_query.data.split('_')[1]
    if action == 'book':
        await callback_query.message.edit_text('Ты в бронировании', reply_markup = await kb.make_calendar(datetime.now()))
        await state.set_state(st.st_book)
        await callback_query.answer()
    elif action == 'cancel':
        await callback_query.message.edit_text('Ты в отмене', reply_markup = await kb.make_calendar(datetime.now()))
        await state.set_state(st.st_cancel)
        await callback_query.answer()
    elif action == 'check':
        await callback_query.message.edit_text('Ты в просмотре', reply_markup = await kb.make_calendar(datetime.now()))
        await state.set_state(st.st_check)
        await callback_query.answer()

#Поймать возвращение в главное меню
@dp.callback_query(F.data == 'in_main')
async def handle_action(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text('Главное меню.', reply_markup = kb.menu)
    await state.clear()

#Кнопка вверх календарь
@dp.callback_query(F.data == 'calendar_up_but')
async def handle_action(callback_query: CallbackQuery, state: FSMContext):
    keyboard = callback_query.message.reply_markup.inline_keyboard
    parsed_date = datetime.strptime(keyboard[1][0].text, "%d.%m.%y")
    await callback_query.message.edit_text('Выберите дату.', reply_markup = await kb.make_calendar((parsed_date - timedelta(days=6)).date()))

#Кнопка вниз календарь
@dp.callback_query(F.data == 'calendar_down_but')
async def handle_action(callback_query: CallbackQuery, state: FSMContext):
    keyboard = callback_query.message.reply_markup.inline_keyboard
    parsed_date = datetime.strptime(keyboard[1][0].text, "%d.%m.%y")
    await callback_query.message.edit_text('Выберите дату.', reply_markup = await kb.make_calendar((parsed_date + timedelta(days=6)).date()))

#Обработка выбора даты, для брони
@dp.callback_query(st.st_book, F.data == 'choice_date')
async def handle_action(callback_query: CallbackQuery, state: FSMContext):
    print('asdsdad')
    await callback_query.answer("st_book")

#Обработка выбора даты, для отмены
@dp.callback_query(F.data == 'choice_date', st.st_cancel)
async def handle_action(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("st_cancel")
    
#Обработка выбора даты, для просмотра
@dp.callback_query(F.data == 'choice_date', st.st_check)
async def handle_action(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("st_check")



async def main() -> None:
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')