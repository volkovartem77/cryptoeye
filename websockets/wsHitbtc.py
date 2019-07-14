# import sys
# sys.path.append(PROJECT_PATH)
import json
import time
import traceback

import websocket

from config import SYMBOLS
from utils_cache import set_tick
from utils_general import format_symbol
from utils_log import err_log, log

NAME = 'Hitbtc'


def on_message(ws, message):
    # print(message)
    message = json.loads(message)

    if 'method' in message:
        if message['method'] == 'ticker':
            data = message['params']
            symbol = format_symbol(data['symbol'].replace('USD', 'USDT'))
            set_tick(NAME, symbol, json.dumps({
                'bid': data['bid'],
                'ask': data['ask'],
                'timestamp': int(time.time() * 1000)
            }))
            # print(NAME, symbol, json.dumps(data))
            # if symbol == 'LTC_BTC':
            #     print(json.dumps({
            #         'bid': data['bid'],
            #         'ask': data['ask'],
            #         'timestamp': int(time.time() * 1000)
            #     }))


def on_error(ws, error):
    log(f'ws{NAME}: {error}')


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('### opened ###')

    for symbol in SYMBOLS:
        ws.send(json.dumps({
            "method": "subscribeTicker",
            "params": {
                "symbol": symbol.replace('_', '').replace('USDT', 'USD'),
                "id": 123
            }
        }))
        log(f'ws{NAME} subscribe {symbol}')


if __name__ == "__main__":
    try:
        while True:
            log(f'ws{NAME}: start')

            ws = websocket.WebSocketApp(
                "wss://api.hitbtc.com/api/2/ws",
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
