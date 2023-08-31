# -*- coding: utf-8 -*-

from telebot import types
import botdb


def archive_kb():
    next_button = types.InlineKeyboardButton(text="➡", callback_data="next")
    prev_button = types.InlineKeyboardButton(text="⬅", callback_data="prev")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(prev_button, next_button)
    return keyboard


def main_kb(ret):
    button1 = '🗂 Архив'
    button2 = '✏ Создание'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row(button1, button2)
    if ret == 1:
        return button1
    elif ret == 2:
        return button2
    elif ret == 0:
        return markup


def depth_kb(ret):
    button1 = '5️⃣'
    button2 = '1️⃣0️⃣'
    button3 = '2️⃣5️⃣'
    button4 = '5️⃣0️⃣'
    button5 = '❌ Сброс'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row(button1, button2, button3, button4)
    markup.add(button5)
    if ret == 1:
        return button1
    elif ret == 2:
        return button2
    elif ret == 3:
        return button3
    elif ret == 4:
        return button4
    elif ret == 5:
        return button5
    elif ret == 0:
        return markup


def zip_kb(ret):
    button1 = '❌ Сброс'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(button1)
    if ret == 1:
        return button1
    elif ret == 0:
        return markup


def settings_kb(ret):
    button1 = '♻ Последние'
    button2 = '🆕 Заново'
    button3 = '❌ Сброс'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row(button1, button2)
    markup.add(button3)
    if ret == 1:
        return button1
    elif ret == 2:
        return button2
    elif ret == 3:
        return button3
    elif ret == 0:
        return markup


def name_kb(ret, user=0):
    button1 = botdb.get_name(user)
    button2 = '❌ Сброс'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(button1)
    markup.add(button2)
    if ret == 1:
        return button1
    elif ret == 2:
        return button2
    elif ret == 0:
        return markup


def height_kb(ret, user=0):
    button1 = botdb.get_height(user)
    button2 = '❌ Сброс'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(button1)
    markup.add(button2)
    if ret == 1:
        return button1
    elif ret == 2:
        return button2
    elif ret == 0:
        return markup


def width_kb(ret, user=0):
    button1 = botdb.get_width(user)
    button2 = '❌ Сброс'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(button1)
    markup.add(button2)
    if ret == 1:
        return button1
    elif ret == 2:
        return button2
    elif ret == 0:
        return markup


def pic_kb(ret):
    button1 = '❌ Сброс'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(button1)
    if ret == 1:
        return button1
    elif ret == 0:
        return markup
