import pygame
from random import choice

import yfinance as yf
import matplotlib.pyplot as plt

import matplotlib
import matplotlib.backends.backend_agg as agg

import pylab
from pygame.locals import *


matplotlib.use("Agg")

STOCKS = [15, 15, 15, 15, 15, 15, 15]
for_choosing = (5, 10, 15, 20, 25)
PROFIT = 0
CUR_PRICE = 0
STOCK_NUMBER = 10
STOCK_ADD = 1
TICKER = 'AAPL'


class StockData:
    pass


class StocksGraphic:
    def __init__(self):
        global STOCKS
        global PROFIT
        global CUR_PRICE

        self.first_time = True

        self.data = yf.download('MSFT', '2021-11-10', '2021-12-10')
        plt.rcParams.update({
            "lines.marker": "o",
            # available ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
            "lines.linewidth": "1.8",
            "axes.prop_cycle": plt.cycler('color', ['white']),  # line color
            "text.color": "white",  # no text in this example
            "axes.facecolor": "black",  # background of the figure
            "axes.edgecolor": "lightgray",
            "axes.labelcolor": "white",  # no labels in this example
            "axes.grid": "True",
            "grid.linestyle": "--",  # {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
            "xtick.color": "white",
            "ytick.color": "white",
            "grid.color": "lightgray",
            "figure.facecolor": "black",  # color surrounding the plot
            "figure.edgecolor": "black",
        })

        self.fig = pylab.figure(figsize=[6, 6],  # Inches
                                dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                                )
        self.fig.patch.set_alpha(0.1)

    def draw_graphic_matplot(self):
        data_size = len(self.data['Adj Close'])
        for i in range(0, data_size):
            self.data['Adj Close'][i:i+10].plot()

            canvas = agg.FigureCanvasAgg(self.fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            # raw_data = renderer.tostring_rgb()
            raw_data = renderer.buffer_rgba()

            #screen = pygame.display.get_surface()
            #screen.fill('black')

            size = canvas.get_width_height()

            # surf = pygame.image.fromstring(raw_data, size, "RGB")
            surf = pygame.image.frombuffer(raw_data, size, "RGBA")
            screen.fill('black')
            screen.blit(surf, (0, 0))

            pygame.display.flip()

    def draw_graphic(self):
        global CUR_PRICE
        global PROFIT

        screen.fill('black')
        self.draw_axes()

        STOCKS.append(choice(for_choosing))
        del STOCKS[0]

        CUR_PRICE = STOCKS[-1]
        PROFIT = STOCK_NUMBER * CUR_PRICE
        self.draw_profit()
        self.check_profit()

        for i in range(6):   # STOCKS[:-1]
            pygame.draw.line(screen,
                             'yellow',
                             (50 + i * 100, 50 + (25 - STOCKS[i]) * 16),
                             (50 + (i + 1) * 100, 50 + (25 - STOCKS[i + 1]) * 16),
                             1)
            pygame.display.flip()

    def draw_profit(self):
        font = pygame.font.Font(None, 30)
        text = font.render(f"PROFIT: {PROFIT}", True, 'red')
        screen.blit(text, (350, 25))

        text = font.render(f"{TICKER}: {STOCK_NUMBER}", True, 'red')
        screen.blit(text, (100, 25))

        text = font.render(f"PRICE: {CUR_PRICE}", True, 'red')
        screen.blit(text, (230, 25))

    def check_profit(self):
        global PROFIT
        if PROFIT >= 300 and self.first_time:
            self.draw_money()
            self.first_time = False
        elif PROFIT < 300:
            self.first_time = True

    def draw_money(self):
        money_serf = pygame.image.load('money2.jpg').convert()
        money_serf.set_colorkey('white')
        money_serf = pygame.transform.scale(money_serf, (60, 60))

        money_rect = money_serf.get_rect(center=(520, 35))
        screen.blit(money_serf, money_rect)

    def draw_axes(self):
        pygame.draw.line(screen, 'white', (50, 30), (50, 450), 2)
        for i in range(6):
            font = pygame.font.Font(None, 20)
            text = font.render(f"{25 - i * 5}", True, 'white')
            screen.blit(text, (25, i * 80 + 40))
        pygame.draw.line(screen, 'white', (50, 450), (650, 450), 2)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    data = yf.download('MSFT', '2021-11-10', '2021-12-10')
    close_price = data['Adj Close']

    running = True
    fps = 60
    clock = pygame.time.Clock()
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    STOCK_NUMBER -= STOCK_ADD
                elif event.key == pygame.K_UP:
                    STOCK_NUMBER += STOCK_ADD

        # отрисовка и изменение свойств объектов
        # ...
        obj = StocksGraphic()
        obj.draw_graphic()
        # obj.draw_graphic_matplot()
        # обновление экрана
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
