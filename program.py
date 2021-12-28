import pygame
import sys
import os
import random
import yfinance as yf
# from random import randrange


STOCKS = [117, 105, 152, 93, 99, 115, 128]

WINDOW = 'start'  # start, level, game, finish
THEME = 'black'
COLOR = 'white'

GAME_TIME = 60_000  # 60, 120, 180
STEP_TIME = 2_000
STEP_COUNT = 0
START_TIME = 0
# SPEED = 60  # 30, ... - per minute

INITIAL_CASH = 1000
CUR_CASH = INITIAL_CASH

ALERT = False
data_tsm = []
for c in yf.download('TSM', '2021-06-10', '2021-12-10')['Adj Close']:
    data_tsm.append(int(c))
data_cvx = []
for c in yf.download('CVX', '2021-06-10', '2021-12-10')['Adj Close']:
    data_cvx.append(int(c))
data_abbv = []
for c in yf.download('ABBV', '2021-06-10', '2021-12-10')['Adj Close']:
    data_abbv.append(int(c))
data_sony = []
for c in yf.download('SONY', '2021-06-10', '2021-12-10')['Adj Close']:
    data_sony.append(int(c))

# data_n = []  # random

LEVEL = {
    'CVX': [data_cvx, True, 'red', 1],
    'TSM': [data_tsm, True, 'green', 1],
    'ABBV': [data_abbv, True, 'blue', 1],
    'SONY': [data_sony, True, 'orange', 1],
    # data_n: False
}

CUR_PRICE = 0

pygame.init()
size = width, height = 900, 650
screen = pygame.display.set_mode(size)


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
        self.v = random.randrange(4, 10)

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
        all_sprites.update()
        all_sprites.draw(screen)

        set_input_text("ИГРА-БИРЖА", (width // 2, height // 2), 100)

        draw_button((width * 0.3, height * 0.7), (width * 0.4, height * 0.1))
        set_input_text('ИГРАТЬ', (width * 0.5, height * 0.75), 50)

        draw_button(
            (width * 0.02, height * 0.03),
            (width * 0.25, height * 0.07),
            2)
        set_input_text('изменить цвет темы',
                       (width * 0.145, height * 0.065),
                       30)


class LevelWindow:
    def __init__(self):
        self.show_warning()
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

    def play(self):
        global WINDOW, ALERT, START_TIME, STEP_COUNT
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
            set_input_text('пока не выбран уровень', (width * 0.5, height * 0.54), 20)


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
        self.draw_axes()
        self.draw_profit()

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
        font = pygame.font.Font(None, 30)

        cur_sum = 0
        pl = 0
        for c in LEVEL:  # c -> [...]
            if LEVEL[c][1]:  # LEVEL[c] -> True

                # ticker
                if 15 + CUR_PRICE < len(LEVEL[c][0]):
                    text = font.render(f"{c}: {LEVEL[c][3]}", True, LEVEL[c][2])
                    screen.blit(text, (120, 25 + 30 * pl))

                    text = font.render(f"PRICE: {LEVEL[c][0][15 + CUR_PRICE]}", True, LEVEL[c][2])
                    screen.blit(text, (250, 25 + 30 * pl))

                    text = font.render(f"PROFIT: {LEVEL[c][0][15 + CUR_PRICE]}", True, LEVEL[c][2])
                    screen.blit(text, (380, 25 + 30 * pl))

                    cur_sum += LEVEL[c][3] * LEVEL[c][0][15 + CUR_PRICE]
                    pl += 1

        # Наличные
        text = font.render(f"CASH: {CUR_CASH}", True, 'red')
        screen.blit(text, (650, 25 + 30 * 2))

        # Общая прибыль портфеля акций
        profit = cur_sum + CUR_CASH - INITIAL_CASH
        text = font.render(f"TOTAL PROFIT: {profit}", True, 'red')
        screen.blit(text, (650, 25 + 30 * 3))


class FinishWindow:
    def __init__(self):
        all_sprites.update()
        all_sprites.draw(screen)

        draw_button((width * 0.3, height * 0.7), (width * 0.4, height * 0.1))
        set_input_text('СЫГРАТЬ СНОВА', (width * 0.5, height * 0.75), 50)


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
