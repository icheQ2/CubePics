# -*- coding: utf-8 -*-

import botconfig
from vedis import Vedis


def get_state(user_id):
    with Vedis(botconfig.states_db) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return botconfig.States.MENU.value


def set_state(user_id, value):
    with Vedis(botconfig.states_db) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def get_name(user_id):
    with Vedis(botconfig.name_db) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return '-'


def set_name(user_id, value):
    with Vedis(botconfig.name_db) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def get_height(user_id):
    with Vedis(botconfig.height_db) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return '-'


def set_height(user_id, value):
    with Vedis(botconfig.height_db) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def get_width(user_id):
    with Vedis(botconfig.width_db) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return '-'


def set_width(user_id, value):
    with Vedis(botconfig.width_db) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def get_depth(user_id):
    with Vedis(botconfig.depth_db) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return '0'


def set_depth(user_id, value):
    with Vedis(botconfig.depth_db) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def get_page(user_id):
    with Vedis(botconfig.page_db) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return '1'


def set_page(user_id, value):
    with Vedis(botconfig.page_db) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False
