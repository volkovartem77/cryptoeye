# import sys
# sys.path.append(PROJECT_PATH)
import json
import time
import traceback

import requests
import websocket

from utils_cache import set_tick
from utils_log import err_log, log

from config import SYMBOLS

NAME = 'Bitmart'


def get_precision(symbol):
    try:
        responce = requests.get('https://openapi.bitmart.com/v2/symbols_details')
        for s in responce.json():
            if s['id'] == symbol:
                return s['price_max_precision']
    except (TypeError, KeyError):
        err_log(traceback.format_exc())


def on_message(ws, message):
    # print(message)
    message = json.loads(message)
    if 'subscribe' in message and message['subscribe'] == 'depth':
        symbol = message['symbol']
        data = message['data']
        bid = data['buys'][0]['price']
        ask = data['sells'][0]['price']

        set_tick(NAME, symbol, json.dumps({
            'bid': bid,
            'ask': ask,
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
        precision = get_precision(symbol)
        if precision is not None:
            ws.send(json.dumps({
                "subscribe": "order",
                "symbol": f"{symbol}",
                "precision": precision
            }))
            log(f'ws{NAME} subscribe {symbol}')


if __name__ == "__main__":
    try:
        while True:
            # log(f'ws{NAME}: loads')
            # load_symbols_info()

            log(f'ws{NAME}: start')

            ws = websocket.WebSocketApp(
                "wss://openws.bitmart.com",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close)

            ws.run_forever()

            log(f'ws{NAME}: restart')
            time.sleep(1)
    except KeyboardInterrupt:
        exit()
    except:
        err_log(traceback.format_exc())
