# import sys
# sys.path.append(PROJECT_PATH)
import base64
import gzip
import json
import time

import websocket

from config import SYMBOLS
from utils_cache import set_tick
from utils_log import log

NAME = 'Bibox'


def on_message(ws, message):
    # print(message)
    if type(json.loads(message)) is list and 'channel' in json.loads(message)[0]:
        if 'ticker' in json.loads(message)[0]['channel']:
            data = gzip.decompress(base64.b64decode(json.loads(message)[0]['data']))
            data = json.loads(data)
            set_tick(NAME, data['pair'], json.dumps({
                'bid': data['buy'],
                'ask': data['sell'],
                'timestamp': int(time.time() * 1000)
            }))
            # print(NAME, data['pair'], json.dumps(data))


def on_error(ws, error):
    log(f'ws{NAME}: {error}')


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('### opened ###')

    for symbol in SYMBOLS:
        ws.send(json.dumps({
            "event": "addChannel",
            "channel": "bibox_sub_spot_{}_ticker".format(symbol)
        }))
        log(f'{NAME} subscribe {symbol}')


if __name__ == "__main__":
    try:
        while True:
            log(f'ws{NAME}: start')
            ws = websocket.WebSocketApp(
                "wss://push.bibox.com/",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close)

            ws.run_forever()

            log(f'ws{NAME}: restart')
            time.sleep(1)
    except KeyboardInterrupt:
        exit()
