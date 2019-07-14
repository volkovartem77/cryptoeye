# import sys
# sys.path.append(PROJECT_PATH)
import gzip
import json
import time
import traceback

import websocket

from config import SYMBOLS
from utils_cache import set_tick
from utils_general import format_symbol
from utils_log import err_log, log

NAME = 'Huobi'


def on_message(ws, message):
    message = json.loads(gzip.decompress(message).decode('utf-8'))
    # print(message)

    if 'ping' in message:
        ws.send(json.dumps({"pong": int(time.time() * 1000)}))
    if 'ch' in message:
        ch = message['ch']
        if 'market.' in ch and '.depth.step0' in ch:
            symbol = format_symbol(ch.replace('market.', '').replace('.depth.step0', '').upper())
            if 'tick' in message:
                data = message['tick']
                set_tick(NAME, symbol, json.dumps({
                    'bid': data['bids'][0][0],
                    'ask': data['asks'][0][0],
                    'timestamp': int(time.time() * 1000)
                }))
                # print(NAME, symbol, json.dumps(data))
                # if symbol == 'LTC_BTC':
                #     print(json.dumps({
                #         'bid': data['bids'][0][0],
                #         'ask': data['asks'][0][0],
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
            "sub": "market.{}.depth.step0".format(symbol.lower().replace('_', '')),
            "id": "id1"
        }))
        log(f'ws{NAME} subscribe {symbol}')


if __name__ == "__main__":
    try:
        while True:
            log(f'ws{NAME}: start')

            ws = websocket.WebSocketApp(
                "wss://api.huobi.pro/ws",
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
