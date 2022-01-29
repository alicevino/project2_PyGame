"""
Основное игровое окно. Обеспечивает отрисовку графиков котировой,
обработку нажатия кнопок игры, подсчет и печать игровой информации
для игрока и торгового робота.
"""

import pygame

import params
import utils


# Основное игровое окно
class GameWindow:
    def __init__(self):
        utils.draw_button(
            (params.width * 0.725, params.height * 0.03),
            (params.width * 0.25, params.height * 0.07),
            2)
        utils.set_input_text('ЗАКОНЧИТЬ ИГРУ',
                       (params.width * 0.85, params.height * 0.065),
                       30)
        self.time = pygame.time.get_ticks()
        self.next()
        self.draw_timer()
        self.show_hint_prof()
        self.show_hint_tick()
        self.show_hint_cot()

    # переход к сдедующему игровому такту
    def next(self):
        time = pygame.time.get_ticks()
        if time - params.START_TIME < params.GAME_TIME:
            if time - params.START_TIME > params.STEP_COUNT * params.STEP_TIME:
                params.STEP_COUNT += 1
                params.CUR_PRICE += 1
            self.draw_graphic()
        else:
            params.WINDOW = 'finish'

    # отрисовка графиков котировок
    def draw_graphic(self):
        for c in params.LEVEL:  # c -> [...]
            if params.LEVEL[c][1]:  # params.LEVEL[c] -> True
                for i in range(15):
                    if i + params.CUR_PRICE + 1 < len(params.LEVEL[c][0]):
                        pygame.draw.line(
                            params.screen,
                            params.LEVEL[c][2],
                            (
                                int(params.width * 0.1 + params.width * 0.046 * i),
                                int(params.height * 0.2 + params.height * 0.013 * (135 - params.LEVEL[c][0][i + params.CUR_PRICE]))
                            ),
                            (
                                int(params.width * 0.1 + params.width * 0.046 * (i + 1)),
                                int(params.height * 0.2 + params.height * (135 - params.LEVEL[c][0][i + params.CUR_PRICE + 1]) * 0.013)
                            ),
                            2)
        self.time = pygame.time.get_ticks()

        self.draw_axes()
        self.draw_profit()

    # отрисовка осей для графиков
    def draw_axes(self):
        pygame.draw.line(params.screen, params.COLOR,
                         (params.width * 0.1, params.height * 0.2),
                         (params.width * 0.1, params.height * 0.85), 2)

        utils.set_input_text('90', (params.width * 0.07, params.height * 0.2 + params.height * 0.013 * (135 - 90)), 20)
        utils.set_input_text('100', (params.width * 0.07, params.height * 0.2 + params.height * 0.013 * (135 - 100)), 20)
        utils.set_input_text('110', (params.width * 0.07, params.height * 0.2 + params.height * 0.013 * (135 - 110)), 20)
        utils.set_input_text('120', (params.width * 0.07, params.height * 0.2 + params.height * 0.013 * (135 - 120)), 20)
        utils.set_input_text('130', (params.width * 0.07, params.height * 0.2 + params.height * 0.013 * (135 - 130)), 20)

        pygame.draw.line(params.screen, params.COLOR,
                         (params.width * 0.1, params.height * 0.85),
                         (params.width * 0.8, params.height * 0.85), 2)

    # подсчет и печать игровой информации для очередного такта
    def draw_profit(self):
        font = pygame.font.Font(None, 30)

        cur_sum = 0
        robot_cur_sum = 0
        robot_stocks = ''
        pl = 0

        # печать заголовка
        text = font.render(f"PRICE:", True, params.COLOR)
        params.screen.blit(text, (params.width * 0.25, params.height * 0.042 + params.height * 0.05 * pl))

        text = font.render(f"SUM:", True, params.COLOR)
        params.screen.blit(text, (params.width * 0.38, params.height * 0.042 + params.height * 0.05 * pl))

        text = font.render(f"NUMBER:", True, params.COLOR)
        params.screen.blit(text, (params.width * 0.52, params.height * 0.042 + params.height * 0.05 * pl))

        # цикл по компаниям
        pl += 1
        for c in params.LEVEL:  # c -> [...]
            if params.LEVEL[c][1]:  # params.LEVEL[c] -> True
                # текущая позиция в списке котировок
                cur_pos = 15 + params.CUR_PRICE

                # для очередной компании печать тикера
                # и информации об акциях в соответствии с текущей ценой
                if cur_pos < len(params.LEVEL[c][0]):
                    # текущая рыночная цена выбранной компании
                    cur_price = params.LEVEL[c][0][cur_pos]
                    # цвет выбранной компании
                    cur_color = params.LEVEL[c][2]

                    text = font.render(f"{c}:", True, cur_color)
                    params.screen.blit(text, (params.width * 0.12, params.height * 0.042 + params.height * 0.05 * pl))

                    text = font.render(f"{cur_price}", True, cur_color)
                    params.screen.blit(text, (params.width * 0.25, params.height * 0.042 + params.height * 0.05 * pl))

                    text = font.render(f"{cur_price * params.LEVEL[c][3]}", True, cur_color)
                    params.screen.blit(text, (params.width * 0.38, params.height * 0.042 + params.height * 0.05 * pl))

                    text = font.render(f"{params.LEVEL[c][3]}", True, cur_color)
                    params.screen.blit(text, (params.width * 0.52, params.height * 0.042 + params.height * 0.05 * pl))

                    self.draw_game_button(pl, cur_color)

                    cur_sum += params.LEVEL[c][3] * cur_price

                    # Ход робота: простая игра на повышение
                    if not params.ROBOT[c][2] or params.ROBOT[c][2] > cur_price:
                        # если цена падает ниже ROBOT_STOP_LOSS, продаем все
                        if params.ROBOT_USE_STOP and \
                                params.ROBOT[c][3] - cur_price > \
                                params.ROBOT[c][3] * params.ROBOT_STOP_LOSS:
                            params.ROBOT_CUR_CASH += params.ROBOT[c][1] * cur_price
                            params.ROBOT[c][1] = 0
                            params.ROBOT[c][3] = 0
                            params.ROBOT[c][2] = cur_price

                        # Если цена падает, покупаем акции
                        elif params.ROBOT_CUR_CASH - cur_price >= 0:
                            params.ROBOT[c][1] += 1
                            params.ROBOT[c][2] = cur_price
                            params.ROBOT_CUR_CASH -= cur_price
                            # запоминаем базовую цену акции
                            if not params.ROBOT[c][3]:
                                params.ROBOT[c][3] = cur_price

                    elif params.ROBOT[c][2] < cur_price:
                        # если цена растет выше ROBOT_TAKE_PROFIT, продаем все
                        if params.ROBOT_USE_STOP and \
                                cur_price - params.ROBOT[c][3] > \
                                params.ROBOT[c][3] * params.ROBOT_TAKE_PROFIT:
                            params.ROBOT_CUR_CASH += params.ROBOT[c][1] * cur_price
                            params.ROBOT[c][1] = 0
                            params.ROBOT[c][3] = 0
                            params.ROBOT[c][2] = cur_price

                        # Если цена растет, продаем акции и получаем прибыль
                        elif params.ROBOT[c][1] > 0:
                            params.ROBOT[c][1] -= 1
                            params.ROBOT[c][2] = cur_price
                            params.ROBOT_CUR_CASH += cur_price

                    robot_cur_sum += params.ROBOT[c][1] * cur_price
                    robot_stocks += f'{params.ROBOT[c][1]} '

                    pl += 1

        # Наличные
        text = font.render(f"CASH: {params.CUR_CASH}", True, 'red')
        params.screen.blit(text, (650, 25 + 30 * 2))

        # Общая прибыль портфеля акций
        params.profit = cur_sum + params.CUR_CASH - params.INITIAL_CASH
        text = font.render(f"TOTAL PROFIT: {params.profit}", True, 'red')
        params.screen.blit(text, (650, 25 + 30 * 3))

        # Общая прибыль робота
        font = pygame.font.Font(None, 25)
        params.robot_profit = robot_cur_sum + params.ROBOT_CUR_CASH - params.INITIAL_CASH
        text = font.render(f"ROBOT PROFIT: {params.robot_profit}", True, 'red')
        params.screen.blit(text, (650, 25 + 30 * 5))

        # Подсказка: список акций
        text = font.render(f"ROBOT STOCKS: {robot_stocks}", True, 'red')
        params.screen.blit(text, (650, 25 + 30 * 6 - 5))

    # отрисовка кнопок покупки/продажи акции
    def draw_game_button(self, pl, color):
        font = pygame.font.Font(None, 40)

        # кнопка купить
        text = font.render(f"+", True, color)
        params.screen.blit(text, (params.width * 0.6, params.height * 0.042 + params.height * 0.05 * pl - 5))

        pygame.draw.rect(params.screen, color,
                         (params.width * 0.6 - 5, params.height * 0.045 + params.height * 0.05 * pl - 5,
                          25, 25),
                         2)

        # кнопка продать
        text = font.render(f"-", True, color)
        params.screen.blit(text, (params.width * 0.65, params.height * 0.042 + params.height * 0.05 * pl - 5))

        pygame.draw.rect(params.screen, color,
                         (params.width * 0.65 - 9, params.height * 0.045 + params.height * 0.05 * pl - 5,
                          25, 25),
                         2)

    # изменение акций в портфеле в результате покупки или продажи
    def shange_stock_num(self, pos):
        cur_pos = 15 + params.CUR_PRICE

        if pos[1] >= params.height * 0.045 + params.height * 0.05 * (len(params.PL) + 1) - 5:
            params.screen.fill('white', (640, params.height * 0.045 + params.height * 0.05 * (len(params.PL) + 1) - 5, 20, 20))
            return

        for y in range(1, len(params.PL) + 1):
            # текущая компания
            cur_comp = params.PL[y - 1]
            # текущая цена выбранной компании
            cur_price = params.LEVEL[cur_comp][0][cur_pos]

            if (params.width * 0.6 - 5 <= pos[0] <= params.width * 0.6 - 5 + 25 and
                    params.height * 0.045 + params.height * 0.05 * y - 5 <= pos[1] <= params.height * 0.045 + params.height * 0.05 * y - 5 + 25):
                # условие покупки
                if params.CUR_CASH - cur_price > 0:
                    params.LEVEL[cur_comp][-1] += 1
                    params.CUR_CASH -= cur_price
                    # print(y, len(params.PL))

            elif (params.width * 0.65 - 9 <= pos[0] <= params.width * 0.65 - 9 + 25 and
                  params.height * 0.045 + params.height * 0.05 * y - 5 <= pos[1] <= params.height * 0.045 + params.height * 0.05 * y - 5 + 25):
                # условие продажи
                if params.LEVEL[cur_comp][-1] > 0:
                    params.LEVEL[cur_comp][-1] -= 1
                    params.CUR_CASH += cur_price

    # печать контекстных подсказок - профит
    def show_hint_prof(self):
        if params.HINT_PROF:
            utils.draw_button(
                (635, 150),
                (180, params.height * 0.14),
                2)
            utils.set_text('ПРОФИТ - прибыль,', params.COLOR, 0, 0, 25, (725, 170))
            utils.set_input_text('полученная в результате', (725, 200), 20)
            utils.set_input_text('успешных сделок', (725, 220), 20)

    # печать контекстных подсказок - тикер
    def show_hint_tick(self):
        if params.HINT_TICK:
            utils.draw_button(
                (100, 80),
                (230, params.height * 0.14),
                2)
            utils.set_text('ТИКЕР - буквенный код,', params.COLOR, 0, 0, 25, (215, 105))
            utils.set_input_text('биржевого или внебиржевого', (215, 125), 20)
            utils.set_input_text('инструмента', (215, 145), 20)

    # печать контекстных подсказок - котировка
    def show_hint_cot(self):
        if params.HINT_COT:
            utils.draw_button(
                (215, 80),
                (200, params.height * 0.25),
                2)
            utils.set_text('КОТИРОВКА -', params.COLOR, 0, 0, 25, (315, 105))
            utils.set_text('конкретная цена,', params.COLOR, 0, 0, 25, (315, 125))
            utils.set_input_text('по которой торгуется', (315, 145), 20)
            utils.set_input_text('ценная бумага на', (315, 165), 20)
            utils.set_input_text('конкретной бирже в', (315, 185), 20)
            utils.set_input_text('конкретнай момент', (315, 205), 20)
            utils.set_input_text('времени', (315, 225), 20)

    # печать времени, оставшегося до конца игры
    def draw_timer(self):
        font = pygame.font.Font(None, 30)
        time = pygame.time.get_ticks()
        text = font.render(f"TIME LEFT: {(params.GAME_TIME - (time - params.START_TIME)) // 1000}", True, 'white')
        params.screen.blit(text, (730, 25 + 30 * 16 - 5))
