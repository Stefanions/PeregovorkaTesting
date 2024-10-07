from datetime import datetime, timedelta

from aiogram.types import (KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder


#Клавиатура меню
menu = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = 'Записаться', callback_data='action_book')], 
                                        [InlineKeyboardButton(text = 'Отменить запись', callback_data='action_cancel')],

                                        [InlineKeyboardButton(text = 'Просмотреть', callback_data='action_check')]])
#Клавиатура календарь
async def make_calendar(date):
    calendar_make = InlineKeyboardBuilder()
    #cur_date = datetime.now()
    cur_date = date
    calendar_make.button(text = '⬆️', callback_data='calendar_up_but')
    for i in range(6):
        date = cur_date + timedelta(days=i)
        formatted_date = date.strftime("%d.%m.%y")
        calendar_make.button(text = formatted_date, callback_data='choice_date')
    calendar_make.button(text = '⬇️', callback_data='calendar_down_but')
    calendar_make.button(text = 'На главную', callback_data='in_main')
    calendar_make.adjust(1)
    calendar = calendar_make.as_markup()
    return calendar
