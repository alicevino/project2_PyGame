import pygame
import sys
import os
import random
import csv


# from random import randrange

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

data_tsm = []
data_cvx = []
data_abbv = []
data_sony = []

'''
import yfinance as yf
for c in yf.download('TSM', '2021-06-10', '2021-12-10')['Adj Close']:
    data_tsm.append(int(c))

for c in yf.download('CVX', '2021-06-10', '2021-12-10')['Adj Close']:
    data_cvx.append(int(c))

for c in yf.download('ABBV', '2021-06-10', '2021-12-10')['Adj Close']:
    data_abbv.append(int(c))

for c in yf.download('SONY', '2021-06-10', '2021-12-10')['Adj Close']:
    data_sony.append(int(c))

with open('tsm.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(data_tsm)
with open('cvx.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(data_cvx)
with open('abbv.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(data_abbv)
with open('sony.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(data_sony)
'''

with open('tsm.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_tsm.extend(map(int, row))
with open('cvx.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_cvx.extend(map(int, row))
with open('data/abbv.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_abbv.extend(map(int, row))
with open('sony.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_sony.extend(map(int, row))

# data_n = []  # random

INITIAL_CASH = 1_000
CUR_CASH = INITIAL_CASH

PL = []
LEVEL = {
    'CVX': [data_cvx, True, 'red', 0],
    'TSM': [data_tsm, True, 'green', 0],
    'ABBV': [data_abbv, True, 'blue', 0],
    'SONY': [data_sony, True, 'orange', 0],
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

pygame.init()
size = width, height = 900, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игра БИРЖА')


# class RandomStocks:
#     def change(self):
#         STOCKS.append(randrange(90, 130))
#         del STOCKS[0]
#
#     def __str__(self):
#         return STOCKS


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Coin(pygame.sprite.Sprite):
    image = load_image('mario coin_2.png')
    image = pygame.transform.scale(image, (40, 40))

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Coin.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.w)
        self.rect.y = random.randrange(height - self.rect.h)
        self.v = random.randrange(10, 20)

    def update(self, *args):
        self.fall()

    def fall(self):
        self.rect.y += self.v
        if self.rect.y > height:
            self.rect.x = random.randrange(width - self.rect.w)
            self.rect.y = - self.rect.h


all_sprites = pygame.sprite.Group()
for _ in range(25):
    Coin(all_sprites)


def set_text(text, color, xx, yy, size, pos):
    x, y = pos
    text = pygame.font.Font(None, size).render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2 + xx, y - text.get_height() // 2 + yy))


def set_input_text(text, pos, size):
    for x in -2, 0, 2:
        for y in -2, 0, 2:
            set_text(text, THEME, x, y, size, pos)
    set_text(text, COLOR, 0, 0, size, pos)


def draw_button(pos, size, w=4):
    pygame.draw.rect(screen, THEME,
                     (pos[0] - (w + 2), pos[1] - (w + 2),
                      size[0] + (w + 2) * 2, size[1] + (w + 2) * 2),
                     0)
    pygame.draw.rect(screen, COLOR,
                     (pos[0], pos[1],
                      size[0], size[1]),
                     w)


class StartWindow:
    def __init__(self):
        global LEVEL, PL, ROBOT
        LEVEL = {
            'CVX': [data_cvx, True, 'red', 0],
            'TSM': [data_tsm, True, 'green', 0],
            'ABBV': [data_abbv, True, 'blue', 0],
            'SONY': [data_sony, True, 'orange', 0],
        }
        PL = ['CVX', 'TSM', 'ABBV', 'SONY']
        ROBOT = {
            'CVX': [True, 0, 0],
            'TSM': [True, 0, 0],
            'ABBV': [True, 0, 0],
            'SONY': [True, 0, 0],
        }

        all_sprites.update()
        all_sprites.draw(screen)

        set_input_text("ИГРА БИРЖА", (width // 2, height // 2), 100)

        draw_button((width * 0.3, height * 0.7), (width * 0.4, height * 0.1))
        set_input_text('ИГРАТЬ', (width * 0.5, height * 0.75), 50)

        draw_button(
            (width * 0.02, height * 0.03),
            (width * 0.25, height * 0.07),
            2)
        set_input_text('изменить цвет темы',
                       (width * 0.145, height * 0.065),
                       30)

        draw_button(
            (width * 0.78, height * 0.03),
            (width * 0.2, height * 0.07),
            2)
        set_input_text('выйти из игры',
                       (width * 0.88, height * 0.065),
                       30)


class LevelWindow:
    def __init__(self):
        global CUR_CASH, PL, LEVEL, CUR_PRICE, ROBOT_CUR_CASH
        CUR_CASH = INITIAL_CASH
        ROBOT_CUR_CASH = INITIAL_CASH
        CUR_PRICE = 0

        draw_button(
            (width * 0.02, height * 0.03),
            (width * 0.1, height * 0.07),
            2)
        set_input_text('назад',
                       (width * 0.07, height * 0.065),
                       30)

        draw_button(
            (width * 0.82, height * 0.875),
            (width * 0.1558, height * 0.1),
            2)
        set_input_text('ИГРАТЬ',
                       (width * 0.9, height * 0.93),
                       40)

        self.draw_levels()
        self.set_rules()
        self.show_warning()

    def set_rules(self):
        set_input_text('Перед Вами финансовая игра БИРЖА.', (width * 0.5, height * 0.2), 50)

        set_input_text(f'Вы получаете на Ваш виртуальный счет {INITIAL_CASH} у.е.', (width * 0.5, height * 0.3), 30)
        set_input_text('Во время игры Вы сможете покупать или', (width * 0.5, height * 0.35), 30)
        set_input_text('продавать акции выбранных компаний, цена которых', (width * 0.5, height * 0.4), 30)
        set_input_text('повторяет реальные рыночные колебания.', (width * 0.5, height * 0.45), 30)

        set_input_text('Если в результате манипуляций с акциями', (width * 0.5, height * 0.55), 30)
        set_input_text('Вам удалось получить прибыль, Вы выиграли,', (width * 0.5, height * 0.6), 30)
        set_input_text('если убыток – проиграли.', (width * 0.5, height * 0.65), 30)

    def play(self):
        global WINDOW, ALERT, START_TIME, STEP_COUNT
        PL = []
        for c in LEVEL:
            if LEVEL[c][1]:
                PL.append(c)
        for c in LEVEL:
            if LEVEL[c][1]:
                WINDOW = 'game'
                START_TIME = pygame.time.get_ticks()
                STEP_COUNT = 0
                break
        else:
            ALERT = True

    def show_warning(self):
        if ALERT:
            draw_button(
                (width * 0.36, height * 0.42),
                (width * 0.28, height * 0.16),
                2)
            set_text('ВНИМАНИЕ!', 'red', 0, 0, 50, (width * 0.5, height * 0.48))
            set_input_text('нельзя начать игру,', (width * 0.5, height * 0.52), 20)
            set_input_text('пока не выбраны компании', (width * 0.5, height * 0.54), 20)

    def choose_level(self, pos):
        for i in range(1, len(PL) + 1):

            if (width * 0.23 * i - width * 0.05 <= pos[0] <= width * 0.23 * i - width * 0.05 + 40
                    and height * 0.75 <= pos[1] <= height * 0.75 + 40):
                LEVEL[PL[i - 1]][1] = not LEVEL[PL[i - 1]][1]

    def draw_levels(self):
        i = 0
        for c in LEVEL:
            i += 1
            set_text(c, LEVEL[c][2], 0, 0, 50, (width * 0.23 * i - width * 0.12, height * 0.785))
            pygame.draw.rect(screen, LEVEL[c][2], (width * 0.23 * i - width * 0.05, height * 0.75, 40, 40), 3)

            if LEVEL[c][1]:
                pygame.draw.rect(screen, LEVEL[c][2],
                                 (width * 0.23 * i - width * 0.05 + 5, height * 0.75 + 5, 40 - 5 * 2, 40 - 5 * 2),
                                 0)


class GameWindow:
    def __init__(self):
        draw_button(
            (width * 0.725, height * 0.03),
            (width * 0.25, height * 0.07),
            2)
        set_input_text('ЗАКОНЧИТЬ ИГРУ',
                       (width * 0.85, height * 0.065),
                       30)
        self.time = pygame.time.get_ticks()
        self.next()
        self.draw_timer()
        self.show_hint()

    def next(self):
        global WINDOW, STEP_COUNT, CUR_PRICE

        time = pygame.time.get_ticks()
        if time - START_TIME < GAME_TIME:
            if time - START_TIME > STEP_COUNT * STEP_TIME:
                STEP_COUNT += 1
                CUR_PRICE += 1
            self.draw_graphic()
        else:
            WINDOW = 'finish'

    def draw_graphic(self):
        for c in LEVEL:  # c -> [...]
            if LEVEL[c][1]:  # LEVEL[c] -> True
                for i in range(15):
                    if i + CUR_PRICE + 1 < len(LEVEL[c][0]):
                        pygame.draw.line(
                            screen,
                            LEVEL[c][2],
                            (
                                int(width * 0.1 + width * 0.046 * i),
                                int(height * 0.2 + height * 0.013 * (135 - LEVEL[c][0][i + CUR_PRICE]))
                            ),
                            (
                                int(width * 0.1 + width * 0.046 * (i + 1)),
                                int(height * 0.2 + height * (135 - LEVEL[c][0][i + CUR_PRICE + 1]) * 0.013)
                            ),
                            2)
        self.time = pygame.time.get_ticks()

        self.draw_axes()
        self.draw_profit()

    def draw_axes(self):
        pygame.draw.line(screen, COLOR,
                         (width * 0.1, height * 0.2),
                         (width * 0.1, height * 0.85), 2)

        set_input_text('90', (width * 0.07, height * 0.2 + height * 0.013 * (135 - 90)), 20)
        set_input_text('100', (width * 0.07, height * 0.2 + height * 0.013 * (135 - 100)), 20)
        set_input_text('110', (width * 0.07, height * 0.2 + height * 0.013 * (135 - 110)), 20)
        set_input_text('120', (width * 0.07, height * 0.2 + height * 0.013 * (135 - 120)), 20)
        set_input_text('130', (width * 0.07, height * 0.2 + height * 0.013 * (135 - 130)), 20)

        pygame.draw.line(screen, COLOR,
                         (width * 0.1, height * 0.85),
                         (width * 0.8, height * 0.85), 2)

    def draw_profit(self):
        global profit, ROBOT_CUR_CASH
        font = pygame.font.Font(None, 30)

        cur_sum = 0
        robot_cur_sum = 0
        robot_stocks = ''
        pl = 0

        text = font.render(f"PRICE:", True, COLOR)
        screen.blit(text, (width * 0.25, height * 0.042 + height * 0.05 * pl))

        text = font.render(f"SUM:", True, COLOR)
        screen.blit(text, (width * 0.38, height * 0.042 + height * 0.05 * pl))

        text = font.render(f"NUMBER:", True, COLOR)
        screen.blit(text, (width * 0.52, height * 0.042 + height * 0.05 * pl))

        pl += 1
        for c in LEVEL:  # c -> [...]
            if LEVEL[c][1]:  # LEVEL[c] -> True
                # ticker
                if 15 + CUR_PRICE < len(LEVEL[c][0]):
                    text = font.render(f"{c}:", True, LEVEL[c][2])
                    screen.blit(text, (width * 0.12, height * 0.042 + height * 0.05 * pl))

                    text = font.render(f"{LEVEL[c][0][15 + CUR_PRICE]}", True, LEVEL[c][2])
                    screen.blit(text, (width * 0.25, height * 0.042 + height * 0.05 * pl))

                    text = font.render(f"{LEVEL[c][0][15 + CUR_PRICE] * LEVEL[c][3]}", True, LEVEL[c][2])
                    screen.blit(text, (width * 0.38, height * 0.042 + height * 0.05 * pl))

                    text = font.render(f"{LEVEL[c][3]}", True, LEVEL[c][2])
                    screen.blit(text, (width * 0.52, height * 0.042 + height * 0.05 * pl))

                    self.draw_game_button(pl, LEVEL[c][2])

                    cur_sum += LEVEL[c][3] * LEVEL[c][0][15 + CUR_PRICE]

                    # Ход робота: простая игра на повышение
                    if not ROBOT[c][2] or ROBOT[c][2] > LEVEL[c][0][15 + CUR_PRICE]:
                        # Если цена падает, покупаем акции
                        if ROBOT_CUR_CASH - LEVEL[c][0][15 + CUR_PRICE] >= 0:
                            ROBOT[c][1] += 1
                            ROBOT[c][2] = LEVEL[c][0][15 + CUR_PRICE]
                            ROBOT_CUR_CASH -= LEVEL[c][0][15 + CUR_PRICE]

                    elif ROBOT[c][2] < LEVEL[c][0][15 + CUR_PRICE]:
                        # Если цена растет, продаем акции и получаем прибыль
                        if ROBOT[c][1] > 0:
                            ROBOT[c][1] -= 1
                            ROBOT[c][2] = LEVEL[c][0][15 + CUR_PRICE]
                            ROBOT_CUR_CASH += LEVEL[c][0][15 + CUR_PRICE]

                    robot_cur_sum += ROBOT[c][1] * LEVEL[c][0][15 + CUR_PRICE]
                    robot_stocks += f'{ROBOT[c][1]} '

                    pl += 1

        # Наличные
        text = font.render(f"CASH: {CUR_CASH}", True, 'red')
        screen.blit(text, (650, 25 + 30 * 2))

        # Общая прибыль портфеля акций
        profit = cur_sum + CUR_CASH - INITIAL_CASH
        text = font.render(f"TOTAL PROFIT: {profit}", True, 'red')
        screen.blit(text, (650, 25 + 30 * 3))

        # Общая прибыль робота
        font = pygame.font.Font(None, 25)
        robot_profit = robot_cur_sum + ROBOT_CUR_CASH - INITIAL_CASH
        text = font.render(f"ROBOT PROFIT: {robot_profit}", True, 'red')
        screen.blit(text, (650, 25 + 30 * 5))
        # Подсказка: список акций
        text = font.render(f"ROBOT STOCKS: {robot_stocks}", True, 'red')
        screen.blit(text, (650, 25 + 30 * 6 - 5))

    def draw_game_button(self, pl, color):
        font = pygame.font.Font(None, 40)

        text = font.render(f"+", True, color)
        screen.blit(text, (width * 0.6, height * 0.042 + height * 0.05 * pl - 5))

        pygame.draw.rect(screen, color,
                         (width * 0.6 - 5, height * 0.045 + height * 0.05 * pl - 5,
                          25, 25),
                         2)

        text = font.render(f"-", True, color)
        screen.blit(text, (width * 0.65, height * 0.042 + height * 0.05 * pl - 5))

        pygame.draw.rect(screen, color,
                         (width * 0.65 - 9, height * 0.045 + height * 0.05 * pl - 5,
                          25, 25),
                         2)

    def shange_stock_num(self, pos):
        global CUR_CASH

        if pos[1] >= height * 0.045 + height * 0.05 * (len(PL) + 1) - 5:
            screen.fill('white', (640, height * 0.045 + height * 0.05 * (len(PL) + 1) - 5, 20, 20))
            return

        for y in range(1, len(PL) + 1):
            if (width * 0.6 - 5 <= pos[0] <= width * 0.6 - 5 + 25 and
                    height * 0.045 + height * 0.05 * y - 5 <= pos[1] <= height * 0.045 + height * 0.05 * y - 5 + 25):
                # условие покупки
                if CUR_CASH - LEVEL[PL[y - 1]][0][15 + CUR_PRICE] > 0:
                    LEVEL[PL[y - 1]][-1] += 1
                    CUR_CASH -= LEVEL[PL[y - 1]][0][15 + CUR_PRICE]
                    # print(y, len(PL))

            elif (width * 0.65 - 9 <= pos[0] <= width * 0.65 - 9 + 25 and
                  height * 0.045 + height * 0.05 * y - 5 <= pos[1] <= height * 0.045 + height * 0.05 * y - 5 + 25):
                # условие продажи
                if LEVEL[PL[y - 1]][-1] > 0:
                    LEVEL[PL[y - 1]][-1] -= 1
                    CUR_CASH += LEVEL[PL[y - 1]][0][15 + CUR_PRICE]

    def show_hint(self):
        if HINT:
            draw_button(
                (635, 150),
                (180, height * 0.14),
                2)
            set_text('ПРОФИТ - прибыль,', COLOR, 0, 0, 25, (725, 170))
            set_input_text('полученная в результате', (725, 200), 20)
            set_input_text('успешных сделок', (725, 220), 20)

    def draw_timer(self):
        font = pygame.font.Font(None, 30)
        time = pygame.time.get_ticks()
        text = font.render(f"TIME LEFT: {(GAME_TIME - (time - START_TIME)) // 1000}", True, 'white')
        screen.blit(text, (730, 25 + 30 * 16 - 5))


class FinishWindow:
    def __init__(self):
        all_sprites.update()
        all_sprites.draw(screen)

        draw_button((width * 0.3, height * 0.7), (width * 0.4, height * 0.1))
        set_input_text('СЫГРАТЬ СНОВА', (width * 0.5, height * 0.75), 50)

        draw_button(
            (width * 0.78, height * 0.03),
            (width * 0.2, height * 0.07),
            2)
        set_input_text('выйти из игры',
                       (width * 0.88, height * 0.065),
                       30)

        self.draw_profit()

    def draw_profit(self):
        if profit > 0:
            set_input_text(f"ВЫ ВЫИГРАЛИ!", (width * 0.5, height * 0.35), 90)
            set_text(f'ваша прибыль составила: +{profit} y.e.', 'red', 0, 0, 55, (width * 0.5, height * 0.45))
        else:
            set_input_text(f"ВЫ ПРОИГРАЛИ :(", (width * 0.5, height * 0.35), 90)
            set_text(f'ваш убыток составил: {profit} y.e.', 'red', 0, 0, 55, (width * 0.5, height * 0.45))
        set_input_text(f"Попробуйте сыграть снова", (width * 0.5, height * 0.6), 40)
        set_input_text(f"и добиться лучших результатов!", (width * 0.5, height * 0.65), 40)


# if __name__ == '__main__':

running = True
fps = 60
clock = pygame.time.Clock()
window = StartWindow()

while running:
    screen.fill(THEME)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # theme changing
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (width * 0.02 <= event.pos[0] <= width * 0.27
                    and height * 0.03 <= event.pos[1] < height * 0.1):
                if WINDOW == 'start':
                    THEME, COLOR = COLOR, THEME
        # choose_level()
        # if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
        #     if (width * 0.23 * 1 - width * 0.05 <= event.pos[0] <= width * 0.23 * 4 - width * 0.05 + 40
        #             and height * 0.75 <= event.pos[1] < height * 0.75 + 40):
        #         if WINDOW == 'level':
        #             window.choose_level(event.pos)
        # from start to level
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (width * 0.3 <= event.pos[0] <= width * 0.7
                    and height * 0.7 <= event.pos[1] < height * 0.8):
                if WINDOW == 'start':
                    WINDOW = 'level'
        # from level to start
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (width * 0.02 <= event.pos[0] <= width * 0.12
                    and height * 0.03 <= event.pos[1] < height * 0.1):
                if WINDOW == 'level':
                    WINDOW = 'start'
        # from level to game
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (width * 0.82 <= event.pos[0] <= width * 0.9752
                    and height * 0.875 <= event.pos[1] < height * 0.975):
                if WINDOW == 'level':
                    window.play()
        # quit the game
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (width * 0.78 <= event.pos[0] <= width * 0.98
                    and height * 0.03 <= event.pos[1] < height * 0.1):
                if WINDOW == 'finish' or WINDOW == 'start':
                    running = False
        # from game to finish
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (width * 0.725 <= event.pos[0] <= width * 0.975
                    and height * 0.03 <= event.pos[1] < height * 0.1):
                if WINDOW == 'game':
                    WINDOW = 'finish'
        # from finish to start
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (width * 0.3 <= event.pos[0] <= width * 0.7
                    and height * 0.7 <= event.pos[1] < height * 0.8):
                if WINDOW == 'finish':
                    WINDOW = 'start'
        # hide alert
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if not (width * 0.36 <= event.pos[0] <= width * 0.64
                    and height * 0.42 <= event.pos[1] < height * 0.58
                    or width * 0.82 <= event.pos[0] <= width * 0.9752
                    and height * 0.875 <= event.pos[1] < height * 0.975):
                if WINDOW == 'level':
                    ALERT = False
        # change_stock_num()
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (width * 0.6 - 5 <= event.pos[0] <= width * 0.65 - 9 + 25 and
                    height * 0.045 + height * 0.05 - 5 <= event.pos[1] < height * 0.045 + height * 0.05 * len(PL) - 5 + 25):
                # print(len(PL))
                if WINDOW == 'game':
                    window.shange_stock_num(event.pos)
        # контекстная подсказка PROFIT
        if event.type == pygame.MOUSEMOTION:
            if WINDOW == 'game':
                if 650 <= event.pos[0] <= 800 and 115 <= event.pos[1] <= 130:
                    HINT = True
                else:
                    HINT = False

    if WINDOW == 'start':
        window = StartWindow()
    elif WINDOW == 'level':
        window = LevelWindow()
    elif WINDOW == 'game':
        window = GameWindow()
    elif WINDOW == 'finish':
        window = FinishWindow()

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
