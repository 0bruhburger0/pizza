#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


# Время доставки
quickly = InlineKeyboardButton('Как можно быстрее', callback_data='quickly')
full = InlineKeyboardMarkup(row_width=1).add(quickly)
one_h = InlineKeyboardButton('Через 1ч', callback_data='1h')
two_h = InlineKeyboardButton('Через 2ч', callback_data='2h')
three_h = InlineKeyboardButton('Через 3ч', callback_data='3h')
full.row(one_h, two_h, three_h)


# Контакт
markup_request2 = KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
full_m = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(markup_request2)


# Оплата
online = InlineKeyboardButton('Онлайн (-5%)', callback_data='online')
offline = InlineKeyboardButton('При получении', callback_data='offline')
pays = InlineKeyboardMarkup(row_width=2).add(online, offline)


# Подтверждение и изменение
cofirm = InlineKeyboardButton('Подтвердить', callback_data='cofirm')
edit = InlineKeyboardButton('Изменить', callback_data='edit')
info_for_ofline = InlineKeyboardMarkup(row_width=2).add(cofirm, edit)

cofirm_on = InlineKeyboardButton('Подтвердить', callback_data='cofirm_on')
edit_on = InlineKeyboardButton('Изменить', callback_data='edit_on')
info_for_online = InlineKeyboardMarkup(row_width=2).add(cofirm_on, edit_on)


# Размер
size_20 = InlineKeyboardButton('40 см', callback_data='40sm')
size_40 = InlineKeyboardButton('20 см', callback_data='20sm')
all_size = InlineKeyboardMarkup(row_width=2).add(size_40, size_20)
