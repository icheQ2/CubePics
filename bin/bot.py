# -*- coding: utf-8 -*-

import botconfig
import botdb
import botkb
import telebot
import time
import os
import algo
import paths
import archive
import numoji
from PIL import Image


bot = telebot.TeleBot(botconfig.token)


@bot.message_handler(func=lambda message: message.chat.id not in botconfig.users)
def echo(message):
   bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    if message.chat.id in botconfig.users:
        bot.send_message(message.chat.id, 'Работаем!')
        bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.MENU.value)
        botdb.set_depth(message.chat.id, '0')
        botdb.set_page(message.chat.id, '1')


@bot.message_handler(func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.MENU.value)
def main_menu(message):
    if message.text == botkb.main_kb(1):
        bot.send_message(message.chat.id, 'Выбери с помощью кнопок снизу глубину архива, который хочешь выгрузить\n'
                                          'Я могу вывести от 5 до 50 последних проектов.', reply_markup=botkb.depth_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.OLD_ENTER_DEPTH.value)
    elif message.text == botkb.main_kb(2):
        name = botdb.get_name(message.chat.id)
        h = botdb.get_height(message.chat.id)
        w = botdb.get_width(message.chat.id)
        bot.send_message(message.chat.id, 'Приступаем к созданию!')
        bot.send_message(message.chat.id, 'Ты хочешь создать проект с последними настройками или задашь их заново?')
        bot.send_message(message.chat.id, 'Просто напомню, что они были такими:\n'
                                          f'*"{name}" {h}x{w}*', reply_markup=botkb.settings_kb(0), parse_mode='Markdown')
        botdb.set_state(message.chat.id, botconfig.States.NEW_CHOOSE_SETTINGS.value)
    else:
        bot.send_message(message.chat.id, 'Я не понимаю, используй готовые кнопки!', reply_markup=botkb.main_kb(0))
        return


@bot.message_handler(func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.OLD_ENTER_DEPTH.value)
def showing_project_list(message):
    if message.text == botkb.depth_kb(5):
        bot.send_message(message.chat.id, 'Перезагрузились, начинаем заново!')
        bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.MENU.value)
        botdb.set_depth(message.chat.id, '0')
        botdb.set_page(message.chat.id, '1')
    elif message.text == botkb.depth_kb(1):
        depth = 5
    elif message.text == botkb.depth_kb(2):
        depth = 10
    elif message.text == botkb.depth_kb(3):
        depth = 25
    elif message.text == botkb.depth_kb(4):
        depth = 50
    else:
        bot.send_message(message.chat.id, 'Я не понимаю, используй готовые кнопки!', reply_markup=botkb.depth_kb(0))
        return
    botdb.set_depth(message.chat.id, str(depth))
    bot.send_message(message.chat.id, f'Вот тебе список из {depth} последних проектов:')
    botdb.set_page(message.chat.id, '1')
    page_text = f'_Страница {botdb.get_page(message.chat.id)}/{round(int(botdb.get_depth(message.chat.id)) / 5)}_'
    bot.send_message(message.chat.id, archive.get_old(int(botdb.get_page(message.chat.id))) + page_text, reply_markup=botkb.archive_kb(), parse_mode='Markdown')
    bot.send_message(message.chat.id, 'Какой проект скачиваем? Жми на ссылки выше.', reply_markup=botkb.zip_kb(0))
    botdb.set_state(message.chat.id, botconfig.States.OLD_ENTER_CHOICE.value)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'prev':
        if int(botdb.get_page(call.message.chat.id)) != 1:
            botdb.set_page(call.message.chat.id, str(int(botdb.get_page(call.message.chat.id)) - 1))
            page_text = f'_Страница {botdb.get_page(call.message.chat.id)}/{round(int(botdb.get_depth(call.message.chat.id)) / 5)}_'
            bot.edit_message_text(chat_id=call.message.chat.id, text=archive.get_old(int(botdb.get_page(call.message.chat.id))) + page_text, message_id=call.message.message_id, reply_markup=botkb.archive_kb(), parse_mode='Markdown')
        else:
            return
    elif call.data == 'next':
        if int(botdb.get_page(call.message.chat.id)) != int(botdb.get_depth(call.message.chat.id)) / 5:
            botdb.set_page(call.message.chat.id, str(int(botdb.get_page(call.message.chat.id)) + 1))
            page_text = f'_Страница {botdb.get_page(call.message.chat.id)}/{round(int(botdb.get_depth(call.message.chat.id)) / 5)}_'
            bot.edit_message_text(chat_id=call.message.chat.id, text=archive.get_old(int(botdb.get_page(call.message.chat.id))) + page_text, message_id=call.message.message_id, reply_markup=botkb.archive_kb(), parse_mode='Markdown')
        else:
            return


@bot.message_handler(commands=botconfig.loadlist(50))
def cmd_load(message):
    if botdb.get_state(message.chat.id) == botconfig.States.OLD_ENTER_CHOICE.value:
        depth = botdb.get_depth(message.chat.id)
        loadlist = botconfig.loadlist(int(depth))
        if message.text[1:] not in loadlist:
            return
        else:
            n = int(message.text[6:])
            bot.send_message(message.chat.id, f'Выгружаю {numoji.processing(n)} архив!')
            archive.download(n, message.chat.id)
            time.sleep(3)
            bot.send_message(message.chat.id, 'Я готов к новому заданию!')
            bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
            botdb.set_state(message.chat.id, botconfig.States.MENU.value)
            botdb.set_depth(message.chat.id, '0')
            botdb.set_page(message.chat.id, '1')
    else:
        return


@bot.message_handler(func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.OLD_ENTER_CHOICE.value)
def downloading_project(message):
    if message.text == botkb.zip_kb(1):
        bot.send_message(message.chat.id, 'Перезагрузились, начинаем заново!')
        bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.MENU.value)
        botdb.set_depth(message.chat.id, '0')
        botdb.set_page(message.chat.id, '1')
    else:
        return


@bot.message_handler(func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.NEW_CHOOSE_SETTINGS.value)
def choosing_settings(message):
    if message.text == botkb.settings_kb(3):
        bot.send_message(message.chat.id, 'Перезагрузились, начинаем заново!')
        bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.MENU.value)
        botdb.set_depth(message.chat.id, '0')
        botdb.set_page(message.chat.id, '1')
    elif message.text == botkb.settings_kb(1):
        name = botdb.get_name(message.chat.id)
        h = botdb.get_height(message.chat.id)
        w = botdb.get_width(message.chat.id)
        bot.send_message(message.chat.id, 'Окей, формируем картинку со следующими параметрами:\n'
                                          f'*"{name}" {h}x{w}*', parse_mode='Markdown')
        bot.send_message(message.chat.id, 'Скидывай фотку', reply_markup=botkb.pic_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.NEW_SEND_PIC.value)
    elif message.text == botkb.settings_kb(2):
        bot.send_message(message.chat.id, 'Ну хорошо, давай определимся с именем проекта.', reply_markup=botkb.name_kb(0, message.chat.id))
        botdb.set_state(message.chat.id, botconfig.States.NEW_ENTER_NAME.value)
    else:
        bot.send_message(message.chat.id, 'Я не понимаю, используй готовые кнопки!', reply_markup=botkb.settings_kb(0))
        return


@bot.message_handler(func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.NEW_ENTER_NAME.value)
def entering_name(message):
    if message.text == botkb.name_kb(2):
        bot.send_message(message.chat.id, 'Перезагрузились, начинаем заново!')
        bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.MENU.value)
        botdb.set_depth(message.chat.id, '0')
        botdb.set_page(message.chat.id, '1')
    else:
        botdb.set_name(message.chat.id, message.text)
        bot.send_message(message.chat.id, 'Имя зафиксировали, теперь размеры.\n'
                                          'Сколько кубов в высоту?', reply_markup=botkb.height_kb(0, message.chat.id))
        botdb.set_state(message.chat.id, botconfig.States.NEW_ENTER_HEIGHT.value)


@bot.message_handler(func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.NEW_ENTER_HEIGHT.value)
def entering_height(message):
    if message.text == botkb.height_kb(2):
        bot.send_message(message.chat.id, 'Перезагрузились, начинаем заново!')
        bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.MENU.value)
        botdb.set_depth(message.chat.id, '0')
        botdb.set_page(message.chat.id, '1')
    elif not message.text.isdigit():
        bot.send_message(message.chat.id, 'Мне нужно число!')
        return
    elif int(message.text) < 5:
        bot.send_message(message.chat.id, 'Маловато будет, давай сделаем больше 5!')
        return
    elif int(message.text) > 50:
        bot.send_message(message.chat.id, 'Многовато будет, давай сделаем меньше 50!')
        return
    else:
        botdb.set_height(message.chat.id, int(message.text))
        bot.send_message(message.chat.id, 'Принято! Теперь ширина.', reply_markup=botkb.width_kb(0, message.chat.id))
        botdb.set_state(message.chat.id, botconfig.States.NEW_ENTER_WIDTH.value)


@bot.message_handler(func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.NEW_ENTER_WIDTH.value)
def entering_width(message):
    if message.text == botkb.width_kb(2):
        bot.send_message(message.chat.id, 'Перезагрузились, начинаем заново!')
        bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.MENU.value)
        botdb.set_depth(message.chat.id, '0')
        botdb.set_page(message.chat.id, '1')
    elif not message.text.isdigit():
        bot.send_message(message.chat.id, 'Мне нужно число!')
        return
    elif int(message.text) < 5:
        bot.send_message(message.chat.id, 'Маловато будет, давай сделаем больше 5!')
        return
    elif int(message.text) > 50:
        bot.send_message(message.chat.id, 'Многовато будет, давай сделаем меньше 50!')
        return
    else:
        botdb.set_width(message.chat.id, int(message.text))
        name = botdb.get_name(message.chat.id)
        h = botdb.get_height(message.chat.id)
        w = botdb.get_width(message.chat.id)
        bot.send_message(message.chat.id, 'Принято! Формируем картинку со следующими параметрами:\n'
                                          f'*{name} {h}x{w}*', parse_mode='Markdown')
        bot.send_message(message.chat.id, 'Скидывай фотку', reply_markup=botkb.pic_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.NEW_SEND_PIC.value)


@bot.message_handler(func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.NEW_SEND_PIC.value)
def sending_photo(message):
    if message.text == botkb.pic_kb(1):
        bot.send_message(message.chat.id, 'Перезагрузились, начинаем заново!')
        bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
        botdb.set_state(message.chat.id, botconfig.States.MENU.value)
        botdb.set_depth(message.chat.id, '0')
        botdb.set_page(message.chat.id, '1')
    else:
        bot.send_message(message.chat.id, 'Мне нужна фотография!', reply_markup=botkb.pic_kb(0))
        return


@bot.message_handler(content_types=['photo'],
                     func=lambda message: botdb.get_state(message.chat.id) == botconfig.States.NEW_SEND_PIC.value)
def sending_photo(message):
    name = botdb.get_name(message.chat.id)
    h = botdb.get_height(message.chat.id)
    w = botdb.get_width(message.chat.id)
    project_path = f'../projects/{name}/'
    photos_path = f'../projects/'

    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = photos_path + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    photo = Image.open(f'{photos_path}{file_info.file_path}')
    os.mkdir(project_path)
    photo.save(f'{project_path}/image.png')
    paths.clear(photos_path + '/photos/')
    bot.send_message(message.chat.id, 'Отлично! Подожди чуть-чуть.')

    result = algo.run(name, int(h), int(w), message.chat.id, message.message_id)
    result_name = result[0]
    result_time = result[1]
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

    archive.add_new(result_name, name, f'{h}x{w}', result_time)
    bot.send_message(message.chat.id, f'Готово! Материалы для скачивания ниже.')
    archive.download(1, message.chat.id)

    paths.remove(project_path)
    time.sleep(3)
    bot.send_message(message.chat.id, 'Я готов к новому заданию!')
    bot.send_message(message.chat.id, 'Вращайте барабан (жмите кнопки снизу)', reply_markup=botkb.main_kb(0))
    botdb.set_state(message.chat.id, botconfig.States.MENU.value)
    botdb.set_depth(message.chat.id, '0')
    botdb.set_page(message.chat.id, '1')


if __name__ == '__main__':
    bot.infinity_polling()
