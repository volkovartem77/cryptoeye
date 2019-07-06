import math
import threading
import time
from statistics import mean

from config import TICK_EXPIRATION_TIME, SYMBOLS, EXCHANGES, MIN_PROFIT, EXCHANGE_PAIRS, STATS_DIFF_TIMEOUT, \
    MONITORING_ACCURACY
from utils_cache import get_tick, calc_diff, init_count, make_stats_diff
from utils_log import log, excel_log


def make_diff():
    while True:
        time.sleep(STATS_DIFF_TIMEOUT)
        make_stats_diff()


def stats(ex_pair, symbol, spikes):
    Id = (ex_pair + symbol).replace('_', '').lower()
    mean_extremum = round(mean(list(math.fabs(x) for x in spikes)), 3)
    excel_log({
        "Id": Id,
        "Exchange pair": ex_pair,
        "Symbol": symbol,
        "Mean extremum": str(mean_extremum),
        "Frequency": str(len(spikes))
    })
    print(ex_pair, symbol, str(mean_extremum), str(len(spikes)), spikes)


def check_timestamp(data):
    return False if int(time.time() * 1000 - data['timestamp']) > TICK_EXPIRATION_TIME * 1000 else True


def is_ready(exchanges):
    for exchange in exchanges:
        for symbol in SYMBOLS:
            tick = get_tick(exchange, symbol)
            if tick is None or not check_timestamp(tick):
                return False
    return True


def launch(ex_pair, symbol):
    exchangeA = ex_pair.split('_')[0]
    exchangeB = ex_pair.split('_')[1]
    log(f'{ex_pair} {symbol} thread started...')

    feeA = EXCHANGES[exchangeA]['trading_fee']
    feeB = EXCHANGES[exchangeB]['trading_fee']
    min_diff = (feeA + feeB) * 2 + MIN_PROFIT

    spikes = []
    max_spike = 0
    min_spike = 0

    while True:
        time.sleep(MONITORING_ACCURACY)
        diff = calc_diff(exchangeA, exchangeB, symbol)
        if diff > min_diff and diff > max_spike:
            max_spike = diff
            while True:
                time.sleep(MONITORING_ACCURACY)
                diff = calc_diff(exchangeA, exchangeB, symbol)
                if diff > min_diff and diff > max_spike:
                    max_spike = diff
                    log(ex_pair + ' ' + symbol + ' ' + str(diff))
                if diff <= 0:
                    spikes.append(max_spike)
                    # stats(ex_pair, symbol, spikes)
                    max_spike = 0
                    break

        if diff < -min_diff and diff < min_spike:
            min_spike = diff
            while True:
                time.sleep(MONITORING_ACCURACY)
                diff = calc_diff(exchangeA, exchangeB, symbol)
                if diff < -min_diff and diff < min_spike:
                    min_spike = diff
                    log(ex_pair + ' ' + symbol + ' ' + str(diff))
                if diff >= 0:
                    spikes.append(min_spike)
                    # stats(ex_pair, symbol, spikes)
                    min_spike = 0
                    break


def launch_thread(ex_pair, symbol):
    while True:
        log(f'{ex_pair} {symbol} thread loading...')
        while not is_ready([ex_pair.split('_')[0], ex_pair.split('_')[1]]):
            time.sleep(5)
        launch(ex_pair, symbol)


if __name__ == '__main__':
    try:
        # monitor
        init_count()
        for pair in EXCHANGE_PAIRS:
            for s in SYMBOLS:
                th = threading.Thread(target=launch_thread, kwargs={"ex_pair": pair, "symbol": s})
                th.start()

        # make stats
        th_stats = threading.Thread(target=make_diff)
        th_stats.start()
    except KeyboardInterrupt:
        exit()
