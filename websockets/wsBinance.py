# import sys
# sys.path.append(PROJECT_PATH)
import json
import time

import websocket

from config import SYMBOLS
from utils_cache import set_tick
from utils_general import format_binance_symbol
from utils_log import log

NAME = 'Binance'


def on_message(ws, message):
    # print(message)

    if 'ticker' in json.loads(message)['stream']:
        data = json.loads(message)['data']
        symbol = format_binance_symbol(data['s'])
        set_tick(NAME, symbol, json.dumps({
            'bid': data['b'],
            'ask': data['a'],
            'timestamp': int(time.time() * 1000)
        }))
        # print(NAME, symbol, json.dumps(data))


def on_error(ws, error):
    log(f'ws{NAME}: {error}')


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('### opened ###')

    for symbol in SYMBOLS:
        log(f'{NAME} subscribe {symbol}')


if __name__ == "__main__":
    try:
        while True:
            log(f'ws{NAME}: start')

            subs = '/'.join(list(s.replace('_', '').lower() + '@ticker' for s in SYMBOLS))

            ws = websocket.WebSocketApp(
                f"wss://stream.binance.com:9443/stream?streams={subs}",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close)

            ws.run_forever()

            log(f'ws{NAME}: restart')
            time.sleep(1)
    except KeyboardInterrupt:
        exit()