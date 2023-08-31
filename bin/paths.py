# -*- coding: utf-8 -*-

import os
import shutil


def clear(path):
    file_list = os.listdir(path)
    for file in file_list:
        os.remove(os.path.join(path, file))


def remove(path):
    shutil.rmtree(path)


def create(path):
    folder_list = ['cropped', 'cubed', 'result']

    try:
        os.remove(os.path.join(path, 'result.png'))
    except FileNotFoundError:
        pass

    try:
        os.remove(os.path.join(path, 'source.png'))
    except FileNotFoundError:
        pass

    for folder in folder_list:
        directory = path + folder
        try:
            os.mkdir(directory)
        except FileExistsError:
            clear(directory)


def archive(path, project, result_name):
    bin_path = f'../bin/{project}.zip'
    zip_path = f'../projects/archive/zip/'
    shutil.make_archive(project, 'zip', path)
    shutil.move(bin_path, f'{zip_path}{project}.zip')
    os.renames(f'{zip_path}{project}.zip', f'{zip_path}{result_name}.zip')
