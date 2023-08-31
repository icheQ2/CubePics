# -*- coding: utf-8 -*-

import numpy
import math


def identification(r_pic, g_pic, b_pic):
    DISTANCE = numpy.zeros((6, 1), 'float')
    SOURCE = numpy.array([r_pic, g_pic, b_pic])
    CUBEC = numpy.array([
        [11, 11, 175],
        [28, 224, 28],
        [221, 24, 24],
        [242, 145, 24],
        [250, 250, 127],
        [250, 247, 247]
    ])  # b, g, r, o, y, w
    # CUBEC_converted = numpy.zeros((6, 3), 'float')
    #
    # SOURCE_converted = rgb_to_xyz(SOURCE)
    # for i in range(6):
    #     CUBEC_converted[i] = rgb_to_xyz(CUBEC[i])
    for i in range(6):
        DISTANCE[i] = math.sqrt((CUBEC[i][0] - SOURCE[0]) ** 2 +
                                (CUBEC[i][1] - SOURCE[1]) ** 2 +
                                (CUBEC[i][2] - SOURCE[2]) ** 2)

    if DISTANCE.min() == DISTANCE[0]:
        fill = (35, 76, 155)  # blue
    elif DISTANCE.min() == DISTANCE[1]:
        fill = (34, 120, 59)  # green
    elif DISTANCE.min() == DISTANCE[2]:
        fill = (158, 45, 49)  # red
    elif DISTANCE.min() == DISTANCE[3]:
        fill = (186, 92, 41)  # orange
    elif DISTANCE.min() == DISTANCE[4]:
        fill = (186, 179, 47)  # yellow
    else:
        fill = (146, 171, 193)  # white

    return fill


def rgb_to_xyz(RGB):
    SOURCE = RGB / 255
    XYZ = numpy.zeros((1, 3), 'float')

    D50 = numpy.array([
        [0.4360747, 0.3850649, 0.1430804],
        [0.2225045, 0.7168786, 0.0606169],
        [0.0139322, 0.0971045, 0.7141733]
    ])

    D65 = numpy.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])

    RGB2XYZ = SOURCE * D65

    for i in range(3):
        XYZ[0][i] = RGB2XYZ[i][0] + RGB2XYZ[i][1] + RGB2XYZ[i][2]

    return XYZ


# def rgb_to_lab(RGB):
#     XYZ = rgb_to_xyz(RGB)
#     LAB = numpy.zeros((1, 3), 'float')
#     F = numpy.zeros((1, 3), 'float')
#
#     e = 0.008856
#     k = 903.3
#
#     for i in range(3):
#         if XYZ[0][i] > e:
#             F[0][i] = pow(XYZ[0][i], 1/3)
#         else:
#             F[0][i] = ((k * XYZ[0][i]) + 16) / 116
#
#     LAB[0][0] = 116 * F[0][1] - 16
#     LAB[0][1] = 500 * (F[0][0] - F[0][1])
#     LAB[0][2] = 200 * (F[0][1] - F[0][2])
#
#     return LAB

# b = (0, 0, 255)
# g = (0, 128, 0)
# r = (255, 0, 0)
# o = (255, 165, 0)
# y = (255, 255, 0)
# w = (255, 255, 255)

# https://ru.stackoverflow.com/questions/881403/Сравнить-два-цвета-rgb-и-определить-похожи-ли-они
