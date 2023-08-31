# -*- coding: utf-8 -*-

import botconfig
from vedis import Vedis


def get_filename(row):
    with Vedis(botconfig.filenames_db) as db:
        try:
            return db[row].decode()
        except KeyError:
            return '-'


def set_filename(row, value):
    with Vedis(botconfig.filenames_db) as db:
        try:
            db[row] = value
            return True
        except:
            return False


def get_name(row):
    with Vedis(botconfig.aname_db) as db:
        try:
            return db[row].decode()
        except KeyError:
            return '-'


def set_name(row, value):
    with Vedis(botconfig.aname_db) as db:
        try:
            db[row] = value
            return True
        except:
            return False


def get_size(row):
    with Vedis(botconfig.asize_db) as db:
        try:
            return db[row].decode()
        except KeyError:
            return '-'


def set_size(row, value):
    with Vedis(botconfig.asize_db) as db:
        try:
            db[row] = value
            return True
        except:
            return False


def get_date(row):
    with Vedis(botconfig.adate_db) as db:
        try:
            return db[row].decode()
        except KeyError:
            return '-'


def set_date(row, value):
    with Vedis(botconfig.adate_db) as db:
        try:
            db[row] = value
            return True
        except:
            return False
