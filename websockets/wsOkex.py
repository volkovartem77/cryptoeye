# import sys
# sys.path.append(PROJECT_PATH)
import gzip
import json
import time
import zlib

import websocket

from config import SYMBOLS
from utils_cache import set_tick
from utils_log import log

NAME = 'Okex'


def inflate(data):
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return json.loads(inflated)


def on_message(ws, message):
    message = inflate(message)
    # print(message)
    if 'table' in message:
        if message['table'] == 'spot/depth5':
            data = message['data'][0]
            symbol = data['instrument_id'].replace('-', '_')
            set_tick(NAME, symbol, json.dumps({
                'bid': data['bids'][0][0],
                'ask': data['asks'][0][0],
                'timestamp': int(time.time() * 1000)
            }))
            # print(NAME, symbol, json.dumps(data))


def on_error(ws, error):
    error = gzip.decompress(error).decode()
    log(f'ws{NAME}: {error}')


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('### opened ###')

    data = []
    for symbol in SYMBOLS:
        data.append(f"spot/depth5:{symbol.replace('_', '-')}")
        log(f'{NAME} subscribe {symbol}')
    ws.send(json.dumps({
        "op": "subscribe",
        "args": data
    }))


if __name__ == "__main__":
    try:
        while True:
            log(f'ws{NAME}: start')
            ws = websocket.WebSocketApp(
                "wss://real.okex.com:10442/ws/v3",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close)

            ws.run_forever()

            log(f'ws{NAME}: restart')
            time.sleep(1)
    except KeyboardInterrupt:
        exit()
