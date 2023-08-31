# -*- coding: utf-8 -*-

import datetime


def current():
    now = datetime.datetime.now()

    Y = now.year

    if len(str(now.month)) == 1:
        M = f'0{now.month}'
    else:
        M = now.month

    if len(str(now.day)) == 1:
        D = f'0{now.day}'
    else:
        D = now.day

    if len(str(now.hour)) == 1:
        h = f'0{now.hour}'
    else:
        h = now.hour

    if len(str(now.minute)) == 1:
        m = f'0{now.minute}'
    else:
        m = now.minute

    if len(str(now.second)) == 1:
        s = f'0{now.second}'
    else:
        s = now.second

    time1 = f'{Y}-{M}-{D} {h}-{m}-{s}'
    time2 = f'{D}.{M}.{Y} {h}:{m}:{s}'
    return [time1, time2]
