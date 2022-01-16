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
HINT = False

# data_n = []  # random

INITIAL_CASH = 1_000
CUR_CASH = INITIAL_CASH

PL = []
LEVEL = {
    'CVX': [data_reader.data_cvx, True, 'red', 0],
    'TSM': [data_reader.data_tsm, True, 'green', 0],
    'ABBV': [data_reader.data_abbv, True, 'blue', 0],
    'SONY': [data_reader.data_sony, True, 'orange', 0],
    # data_n: False
}

ROBOT = {
    'CVX': [True, 0, 0],
    'TSM': [True, 0, 0],
    'ABBV': [True, 0, 0],
    'SONY': [True, 0, 0],
    # data_n: False
}
ROBOT_CUR_CASH = INITIAL_CASH

CUR_PRICE = 0
profit = 0

screen = 0
width, height = 0, 0
