import datetime
import os

from config import EXCEL_LOG_PATH, ERR_LOG_PATH, LOG_PATH, EXCEL_DIFF_LOG_PATH


def log(text, symbol=''):
    file = open(LOG_PATH, "a")
    dt = datetime.datetime.now().replace(microsecond=0).isoformat().replace('T', ' ')
    file.write(dt + ' ' + symbol + ' ' + text + '\n')
    file.close()
    print(dt + ' ' + symbol + ' ' + text)


def err_log(text, symbol=''):
    file = open(ERR_LOG_PATH, "a")
    dt = datetime.datetime.now().replace(microsecond=0).isoformat().replace('T', ' ')
    file.write(dt + ' ' + symbol + '\n' + text + '\n')
    file.close()
    print(dt + ' ' + symbol + '\n' + text)


def excel_log(data):
    mark = data['Id']
    if os.path.exists(EXCEL_LOG_PATH) is False:
        header = ''
        for column in list(data.keys()):
            header += column + ';'
        f = open(EXCEL_LOG_PATH, "a")
        f.write(header + '\n')
        f.close()

    line = ''
    for column in list(data.keys()):
        line += data[column] + ';'
    if line != '':
        ff = open(EXCEL_LOG_PATH, 'r')
        old_data = ff.readlines()
        myindex = len(old_data)
        for x in old_data:
            if mark in x:
                myindex = old_data.index(x)
        if myindex == len(old_data):
            old_data.append(line + '\n')
        else:
            old_data[myindex] = line + '\n'

        f = open(EXCEL_LOG_PATH, "w")
        f.writelines(old_data)
        f.close()


def excel_diff_log(data):
    header = ';'
    header += ';'.join(list(data.keys()))
    rows = []
    for ex_pair in data:
        rows.extend(list(data[ex_pair].keys()))
    rows = sorted(float(x) for x in list(set(rows)))

    lines = [header]
    for row in rows:
        values = [str(row)]
        for ex_pair in data:
            if str(row) in data[ex_pair]:
                values.append(str(data[ex_pair][str(row)]))
            else:
                values.append('0')
        lines.append(';'.join(values))

    f = open(EXCEL_DIFF_LOG_PATH, 'w')
    f.writelines(list(x + '\n' for x in lines))
    f.close()


# excel_diff_log({'Binance_Bibox:ETH_BTC': {-0.02: 53, 0.0: 38, -0.03: 41, -0.01: 50, 0.01: 18},
#                 'Binance_Bibox:ETH_USDT': {-0.04: 25, 0.0: 25, -0.03: 25, -0.06: 25, 0.07: 25}})

# excel_diff_log({'Binance_Bibox:ETH_BTC': {-0.02: 3, 0.0: 8, -0.13: 1, 0.01: 1},
#                 'Binance_Bibox:ETH_USDT': {-0.12: 5, 0.0: 25, -0.05: 2, 0.07: 25}})
