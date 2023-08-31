# -*- coding: utf-8 -*-

from enum import Enum
from resources import botconfig

token = botconfig.token
users = {botconfig.user1, botconfig.user2, botconfig.user3}

states_db = './databases/b_db1.vdb'
name_db = './databases/b_db2.vdb'
height_db = './databases/b_db3.vdb'
width_db = './databases/b_db4.vdb'
depth_db = './databases/b_db5.vdb'
page_db = './databases/b_db6.vdb'

filenames_db = './databases/a_db1.vdb'
aname_db = './databases/a_db2.vdb'
asize_db = './databases/a_db3.vdb'
adate_db = './databases/a_db4.vdb'

class States(Enum):
    MENU = "0"
    OLD_ENTER_DEPTH = '1'
    OLD_ENTER_CHOICE = '2'
    NEW_CHOOSE_SETTINGS = '3'
    NEW_ENTER_NAME = '4'
    NEW_ENTER_HEIGHT = '5'
    NEW_ENTER_WIDTH = '6'
    NEW_SEND_PIC = '7'


def loadlist(depth):
    loadlist = []
    for i in range(1, depth+1):
        loadlist.append(f'load_{i}')
    return loadlist
