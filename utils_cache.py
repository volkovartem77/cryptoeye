import json
import traceback
from collections import Counter

from config import DATABASE, EXCHANGE_PAIRS, SYMBOLS
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


def calc_diff(exchangeA, exchangeB, symbol):
    tickA = get_tick(exchangeA, symbol)
    tickB = get_tick(exchangeB, symbol)
    min_ask = min(float(tickA['ask']), float(tickB['ask']))
    max_bid = max(float(tickA['bid']), float(tickB['bid']))
    diff = round((max_bid / min_ask * 100) - 100, 2)
    update_count(f'{exchangeA}_{exchangeB}', symbol, diff)
    return diff


def make_stats_diff():
    data = {}
    for ex_pair in EXCHANGE_PAIRS:
        for symbol in SYMBOLS:
            diffs = get_count(ex_pair, symbol)
            if diffs:
                if '-0.0' in diffs:
                    n = diffs['-0.0']
                    diffs.pop('-0.0')
                    diffs.update({'0.0': n})
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
