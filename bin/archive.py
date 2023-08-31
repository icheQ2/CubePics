import telebot
import os
import botconfig
import archivedb
import numoji


bot = telebot.TeleBot(botconfig.token)


def add_new(filename, name, size, date):
    last = archivedb.get_filename(50)
    path = '../projects/archive/'
    try:
        os.remove(os.path.join(f'{path}img/', f'{last}.png'))
        os.remove(os.path.join(f'{path}zip/', f'{last}.zip'))
    except:
        pass

    for i in range(49):
        row = 50 - i
        archivedb.set_filename(row, archivedb.get_filename(row - 1))
        archivedb.set_name(row, archivedb.get_name(row - 1))
        archivedb.set_size(row, archivedb.get_size(row - 1))
        archivedb.set_date(row, archivedb.get_date(row - 1))
    archivedb.set_filename(1, filename)
    archivedb.set_name(1, name)
    archivedb.set_size(1, size)
    archivedb.set_date(1, date)


def get_old(page):
    archive = ''
    for row in range((page * 5 - 5), page * 5):
        name = archivedb.get_name(row + 1)
        size = archivedb.get_size(row + 1)
        date = archivedb.get_date(row + 1)
        command = f'/load\_{row + 1}'
        archive = archive + f'{numoji.processing(row + 1)}\n*{name}* ({size})\n{date}\n{command}\n\n'
    return archive


def download(row, chat_id):
    filename = archivedb.get_filename(row)
    img = open(f'../projects/archive/img/{filename}.png', 'rb')
    zip = open(f'../projects/archive/zip/{filename}.zip', 'rb')
    bot.send_photo(chat_id, img)
    bot.send_document(chat_id, zip)
