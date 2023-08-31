# -*- coding: utf-8 -*-

import paths
import draw
import statusbar
import timing
import colors
import botconfig
import numpy
import telebot
from PIL import Image

bot = telebot.TeleBot(botconfig.token)

def run(project, cube_height, cube_width, chat_id, message_id):
    cube_pixels = 99
    tile_pixels = int(cube_pixels / 3)
    pixels_in_tile = tile_pixels ** 2

    t = 0
    t_max = cube_width * cube_height

    path = f'../projects/{project}/'
    image = Image.open(f'{path}/image.png')

    paths.create(path)

    prepared = image.resize((cube_width * cube_pixels, cube_height * cube_pixels), Image.ANTIALIAS)

    C = numpy.zeros((cube_height, cube_width), 'object')
    T = numpy.zeros((3, 3), 'object')

    cubed = Image.new('RGBA', (cube_pixels, cube_pixels), (0, 0, 0, 0))
    res_cubed = Image.new('RGBA', (cube_pixels, cube_pixels), (0, 0, 0, 0))
    mid_result = Image.new('RGBA', (cube_width * cube_pixels, cube_height * cube_pixels), (0, 0, 0, 0))
    result = Image.new('RGBA', (cube_width * cube_pixels, cube_height * cube_pixels), (0, 0, 0, 0))

    cubes_progress_id = message_id + 2
    bot.send_message(chat_id, statusbar.cubes(t, t_max))
    previous_t = t
    step_t = t_max / 11

    for h in range(cube_height):
        for w in range(cube_width):
            C[h, w] = prepared.crop(
                (w * cube_pixels, h * cube_pixels, w * cube_pixels + cube_pixels, h * cube_pixels + cube_pixels))
            C[h, w].save(f'{path}cropped/cube {h+1}-{w+1}.png')
            for i in range(3):
                for j in range(3):
                    T[i, j] = C[h, w].crop(
                        (j * tile_pixels, i * tile_pixels, j * tile_pixels + tile_pixels, i * tile_pixels + tile_pixels))
                    rgb_values = list(T[i, j].getdata())
                    r = 0
                    g = 0
                    b = 0
                    for p in range(pixels_in_tile):
                        r = r + rgb_values[p][0]
                        g = g + rgb_values[p][1]
                        b = b + rgb_values[p][2]
                    r = round(r / pixels_in_tile)
                    g = round(g / pixels_in_tile)
                    b = round(b / pixels_in_tile)
                    tile_mid = Image.new('RGB', (tile_pixels, tile_pixels), (r, g, b))
                    cubed.paste(tile_mid, (j * tile_pixels, i * tile_pixels))
                    color_res = colors.identification(r, g, b)
                    tile_res = Image.new('RGB', (tile_pixels, tile_pixels), color_res)
                    res_cubed.paste(tile_res, (j * tile_pixels, i * tile_pixels))

            draw.borders(cubed, cube_pixels)
            draw.borders(res_cubed, cube_pixels)
            cubed.save(f'{path}/cubed/cube {h + 1}-{w + 1}.png')
            res_cubed.save(f'{path}/result/cube {h + 1}-{w + 1}.png')
            mid_result.paste(cubed, (w * cube_pixels, h * cube_pixels))
            result.paste(res_cubed, (w * cube_pixels, h * cube_pixels))
            t += 1
            if t >= previous_t + step_t:
                bot.edit_message_text(chat_id=chat_id, text=statusbar.cubes(t, t_max), message_id=cubes_progress_id)
                previous_t = t

    mid_result.save(f'{path}/source.png')
    result.save(f'{path}/result.png')
    result_name = f'{timing.current()[0]} {project} ({cube_height}x{cube_width})'
    time = f'{timing.current()[1]}'
    result.save(f'../projects/archive/img/{result_name}.png')
    paths.archive(path, project, result_name)
    bot.delete_message(chat_id=chat_id, message_id=cubes_progress_id)

    return [result_name, time]
