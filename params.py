"""
Основные параметры игры для данных игрока, робота и
графических элементов.
"""

import data_reader

WINDOW = 'start'  # start, level, game, finish
THEME = 'black'
COLOR = 'white'

GAME_TIME = 90_000  # 60, 120, 180
STEP_TIME = 2_000
STEP_COUNT = 0
START_TIME = 0
# SPEED = 60  # 30, ... - per minute

ALERT = False
HINT_PROF = False
HINT_TICK = False
HINT_COT = False
HINT_STOP_LOSS = False
HINT_TAKE_PROFIT = False

# Параметры игрока
INITIAL_CASH = 1_000
CUR_CASH = INITIAL_CASH

PL = []
LEVEL = {
    'CVX': [data_reader.data_cvx, True, 'red', 0],
    'TSM': [data_reader.data_tsm, True, 'green', 0],
    'ABBV': [data_reader.data_abbv, True, 'blue', 0],
    'SONY': [data_reader.data_sony, True, 'orange', 0],
}

# Параметры робота
ROBOT = {
    'CVX': [True, 0, 0, 0],
    'TSM': [True, 0, 0, 0],
    'ABBV': [True, 0, 0, 0],
    'SONY': [True, 0, 0, 0],
}
ROBOT_CUR_CASH = INITIAL_CASH
ROBOT_STOP_LOSS = 10
RSL = False
ROBOT_TAKE_PROFIT = 10
RTP = False
robot_profit = 0

CUR_PRICE = 0
profit = 0

screen = 0
width, height = 0, 0
