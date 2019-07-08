import json
import time
import traceback
from collections import Counter

from config import DATABASE, EXCHANGE_PAIRS, SYMBOLS, MIN_PROFIT, EXCHANGES
from utils_log import err_log, excel_diff_log


def get_tick(exchange, symbol):
    try:
        tick = DATABASE.get(exchange + ':' + symbol)
        return json.loads(json.loads(tick)) if tick is not None else tick
    except TypeError:
        err_log(traceback.format_exc(), exchange + ':' + symbol)


def set_tick(exchange, symbol, data):
    try:
        DATABASE.set(exchange + ':' + symbol, json.dumps(data))
    except TypeError:
        err_log(traceback.format_exc(), symbol)


def init_count():
    for ex_pair in EXCHANGE_PAIRS:
        for symbol in SYMBOLS:
            set_count(ex_pair, symbol, {})


def init_points():
    for ex_pair in EXCHANGE_PAIRS:
        for symbol in SYMBOLS:
            set_points(ex_pair, symbol, [])


def get_count(ex_pair, symbol):
    try:
        count = DATABASE.get(ex_pair + ':' + symbol)
        return json.loads(count) if count is not None else count
    except TypeError:
        err_log(traceback.format_exc(), ex_pair + ':' + symbol)


def set_count(ex_pair, symbol, values):
    try:
        DATABASE.set(ex_pair + ':' + symbol, json.dumps(values))
    except TypeError:
        err_log(traceback.format_exc(), symbol)


def update_count(ex_pair, symbol, value):
    try:
        values = get_count(ex_pair, symbol)
        if str(value) in values:
            values.update({str(value): values[str(value)] + 1})
        else:
            values.update({value: 1})
        set_count(ex_pair, symbol, values)
    except TypeError:
        err_log(traceback.format_exc(), symbol)


def get_points(ex_pair, symbol):
    try:
        points = DATABASE.get(ex_pair + ':' + symbol + 'POINTS')
        return json.loads(points) if points is not None else points
    except TypeError:
        err_log(traceback.format_exc(), ex_pair + ':' + symbol)


def set_points(ex_pair, symbol, points):
    try:
        DATABASE.set(ex_pair + ':' + symbol + 'POINTS', json.dumps(points))
    except TypeError:
        err_log(traceback.format_exc(), symbol)


def update_points(ex_pair, symbol, point):
    try:
        points = get_points(ex_pair, symbol)
        points.append(point)
        set_points(ex_pair, symbol, points)
    except TypeError:
        err_log(traceback.format_exc(), symbol)


def add_point(exchangeA, exchangeB, symbol, point):
    points = get_points(exchangeA + '_' + exchangeB, symbol)
    if points is None or not points:
        update_points(exchangeA + '_' + exchangeB, symbol, point)
    else:
        last_diffA = points[-1][0]
        last_diffB = points[-1][1]
        if point[0] != last_diffA or point[1] != last_diffB:
            print(exchangeA + '_' + exchangeB, symbol, point)
            update_points(exchangeA + '_' + exchangeB, symbol, point)


def calc_diff(exchangeA, exchangeB, symbol):
    tickA = get_tick(exchangeA, symbol)
    tickB = get_tick(exchangeB, symbol)
    diffA = round((float(tickA['bid']) / float(tickB['ask']) * 100) - 100, 1)
    diffB = round((float(tickB['bid']) / float(tickA['ask']) * 100) - 100, 1)
    diff = max(diffA, diffB)
    update_count(f'{exchangeA}_{exchangeB}', symbol, diff)
    # add_point(exchangeA, exchangeB, symbol, [diffA, diffB, int(time.time() * 1000)])
    return diff


def make_stats_diff():
    data = {}
    for ex_pair in EXCHANGE_PAIRS:
        for symbol in SYMBOLS:
            diffs = get_count(ex_pair, symbol)
            if diffs:
                data.update({ex_pair + ':' + symbol: diffs})
    if data:
        excel_diff_log(data)


# init_count()
# print(get_count("Binance_Bibox", 'ETH_BTC'))
# update_count("Binance_Bibox", 'ETH_BTC', 0.005)
# print(get_count("Binance_Bibox", 'ETH_BTC'))
# update_count("Binance_Bibox", 'ETH_BTC', 0.003)
# print(get_count("Binance_Bibox", 'ETH_BTC'))
# update_count("Binance_Bibox", 'ETH_BTC', 0.003)
# print(get_count("Binance_Bibox", 'ETH_BTC'))
# calc_diff("Binance", "Bibox", 'ETH_BTC')
# print(get_count("Binance_Bibox", 'ETH_BTC'))
# calc_diff("Binance", "Bibox", 'ETH_BTC')
# print(get_count("Binance_Bibox", 'ETH_BTC'))

# import time
# init_count()
# for x in range(100 * 2):
#     calc_diff("Binance", "Bibox", 'ETH_BTC')
#     time.sleep(.3)
# diffs = get_count("Binance_Bibox", 'ETH_BTC')
# print(len(diffs), diffs)
# make_stats_diff()

# for ex_pair in EXCHANGE_PAIRS:
#     for symbol in SYMBOLS:
#         diffs = get_count(ex_pair, symbol)
#         print(diffs)

# init_points()
# print(get_points("Binance_Bibox", 'ETH_BTC'))
# add_point("Binance", "Bibox", 'ETH_BTC', [-0.21, -0.19, 1562418112958])
# print(get_points("Binance_Bibox", 'ETH_BTC'))
# add_point("Binance", "Bibox", 'ETH_BTC', [-0.28, -0.05, 1562418113254])
# print(get_points("Binance_Bibox", 'ETH_BTC'))
# add_point("Binance", "Bibox", 'ETH_BTC', [-0.28, -0.05, 1562418113254])
# print(get_points("Binance_Bibox", 'ETH_BTC'))
# add_point("Binance_Bibox", 'ETH_BTC', [-0.12, -0.2, 1562418113263])
# print(get_points("Binance_Bibox", 'ETH_BTC'))
