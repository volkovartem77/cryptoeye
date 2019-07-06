import json

import redis

PROJECT_PATH = '/home/kusko/PyProjects/CryptoEye/'
PROJECT_FOLDER = PROJECT_PATH.split('/')[-2]
CONF_PATH = PROJECT_PATH + PROJECT_FOLDER + '.conf'


def get_preferences():
    ff = open(PROJECT_PATH + 'preferences.txt', "r")
    preferences = json.loads(ff.read())
    ff.close()
    return preferences


EXCHANGES = get_preferences()['exchanges']
SYMBOLS = get_preferences()['symbols']
EXCHANGE_PAIRS = get_preferences()['ex_pairs']

DATABASE = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


# Logging
LOG_PATH = PROJECT_PATH + 'general.log'
ERR_LOG_PATH = PROJECT_PATH + 'errors.log'
EXCEL_LOG_PATH = PROJECT_PATH + 'stats.csv'
EXCEL_DIFF_LOG_PATH = PROJECT_PATH + 'stats_diff.csv'


# Constants
TICK_EXPIRATION_TIME = 6
MIN_PROFIT = 0.1
STATS_DIFF_TIMEOUT = 60
MONITORING_ACCURACY = .3
