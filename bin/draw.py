# -*- coding: utf-8 -*-

from PIL import ImageDraw


def borders(cube, cube_pixels):
    out_color = (255, 71, 202)
    in_color = (0, 0, 0)

    if cube_pixels > 350:
        width = 12
    elif cube_pixels > 250:
        width = 10
    elif cube_pixels > 150:
        width = 6
    else:
        width = 4

    if cube_pixels > 250:
        error = 4
    else:
        error = 2

    format_cube = ImageDraw.Draw(cube)

    # внутренние вертикальные
    format_cube.line((cube_pixels / 3 - 1, 0, cube_pixels / 3 - 1, cube_pixels), fill=in_color, width=width)
    format_cube.line((cube_pixels / 3 * 2 - 1, 0, cube_pixels / 3 * 2 - 1, cube_pixels), fill=in_color, width=width)
    # внутренние горизонтальные
    format_cube.line((0, cube_pixels / 3 - 1, cube_pixels, cube_pixels / 3 - 1), fill=in_color, width=width)
    format_cube.line((0, cube_pixels / 3 * 2 - 1, cube_pixels, cube_pixels / 3 * 2 - 1), fill=in_color, width=width)
    # внешние вертикальные
    format_cube.line((0, 0, 0, cube_pixels), fill=out_color, width=width-1)
    format_cube.line((cube_pixels - error, 0, cube_pixels - error, cube_pixels), fill=out_color, width=int(width / 2))
    # внешние горизонтальные
    format_cube.line((0, 0, cube_pixels, 0), fill=out_color, width=width-1)
    format_cube.line((0, cube_pixels - error, cube_pixels, cube_pixels - error), fill=out_color, width=int(width / 2))
    return cube
