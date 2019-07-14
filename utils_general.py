import datetime
import math
import traceback

from config import SYMBOLS
from utils_log import err_log


def normalize_symbol(asset_1, asset_2):
    side = 'SELL'
    symbol = asset_1 + '_' + asset_2
    if symbol not in SYMBOLS:
        symbol = asset_2 + '_' + asset_1
        side = 'BUY'
    return symbol, side


def round_dwn(value, param=1):
    return int(value) if param == 0 else math.floor(value * math.pow(10, param)) / math.pow(10, param)


def date_ts(timestamp=0):
    if timestamp == 0:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')


def format_symbol(symbol):
    try:
        symbol = symbol.replace('-', '').replace('/', '').replace('_', '').upper()
        for s in SYMBOLS:
            if symbol == s.replace('_', ''):
                return s
    except (TypeError, KeyError):
        err_log(traceback.format_exc(), symbol)


# print(format_symbol('ETHBTC'))
# print(format_symbol('ETH-BTC'))
# print(format_symbol('ETH/BTC'))
# print(format_symbol('ETH_BTC'))
# print(format_symbol('eth_btc'))
# print(format_symbol('ethbtc'))