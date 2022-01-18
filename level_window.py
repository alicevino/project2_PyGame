"""
Окно с инфрмацией о правилах игры. Обеспечивает выбор
параметров игры - списка компаний.
"""

import pygame

import params
import utils


# Окно для выбора параметров игры
class LevelWindow:
    def __init__(self):
        # инициализация базовых параметров игрока
        params.CUR_CASH = params.INITIAL_CASH
        params.ROBOT_CUR_CASH = params.INITIAL_CASH
        params.CUR_PRICE = 0

        # кнопка возврата на предыдущее окно
        utils.draw_button(
            (params.width * 0.02, params.height * 0.03),
            (params.width * 0.1, params.height * 0.07),
            2)
        utils.set_input_text('назад',
                             (params.width * 0.07, params.height * 0.065),
                             30)

        # начало игры
        utils.draw_button(
            (params.width * 0.82, params.height * 0.875),
            (params.width * 0.1558, params.height * 0.1),
            2)
        utils.set_input_text('ИГРАТЬ',
                             (params.width * 0.9, params.height * 0.93),
                             40)

        self.draw_levels()
        self.set_rules()
        self.show_warning()

    # правила игры
    def set_rules(self):
        utils.set_input_text('Перед Вами финансовая игра БИРЖА.', (params.width * 0.5, params.height * 0.2), 50)

        utils.set_input_text(f'Вы получаете на Ваш виртуальный счет {params.INITIAL_CASH} у.е.', (params.width * 0.5, params.height * 0.3), 30)
        utils.set_input_text('Во время игры Вы сможете покупать или', (params.width * 0.5, params.height * 0.35), 30)
        utils.set_input_text('продавать акции выбранных компаний, цена которых', (params.width * 0.5, params.height * 0.4), 30)
        utils.set_input_text('повторяет реальные рыночные колебания.', (params.width * 0.5, params.height * 0.45), 30)

        utils.set_input_text('Если в результате манипуляций с акциями', (params.width * 0.5, params.height * 0.55), 30)
        utils.set_input_text('Вам удалось получить прибыль, Вы выиграли,', (params.width * 0.5, params.height * 0.6), 30)
        utils.set_input_text('если убыток – проиграли.', (params.width * 0.5, params.height * 0.65), 30)

    # выбор компаний для игры
    def play(self):
        params.PL = []
        for c in params.LEVEL:
            if params.LEVEL[c][1]:
                params.PL.append(c)
        for c in params.LEVEL:
            if params.LEVEL[c][1]:
                params.WINDOW = 'game'
                params.START_TIME = pygame.time.get_ticks()
                params.STEP_COUNT = 0
                break
        else:
            params.ALERT = True

    # предупреждение, что ни одна компания не выбрана
    def show_warning(self):
        if params.ALERT:
            utils.draw_button(
                (params.width * 0.36, params.height * 0.42),
                (params.width * 0.28, params.height * 0.16),
                2)
            utils.set_text('ВНИМАНИЕ!', 'red', 0, 0, 50, (params.width * 0.5, params.height * 0.48))
            utils.set_input_text('нельзя начать игру,', (params.width * 0.5, params.height * 0.52), 20)
            utils.set_input_text('пока не выбраны компании', (params.width * 0.5, params.height * 0.54), 20)

    # выбор компаний для игры
    def choose_level(self, pos):
        for i in range(1, len(params.PL) + 1):

            if (params.width * 0.23 * i - params.width * 0.05 <= pos[0] <= params.width * 0.23 * i - params.width * 0.05 + 40
                    and params.height * 0.75 <= pos[1] <= params.height * 0.75 + 40):
                params.LEVEL[params.PL[i - 1]][1] = not params.LEVEL[params.PL[i - 1]][1]

    # отрисовка выбранных компаний
    def draw_levels(self):
        i = 0
        for c in params.LEVEL:
            i += 1
            utils.set_text(c, params.LEVEL[c][2], 0, 0, 50, (params.width * 0.23 * i - params.width * 0.12, params.height * 0.785))
            pygame.draw.rect(params.screen, params.LEVEL[c][2], (params.width * 0.23 * i - params.width * 0.05, params.height * 0.75, 40, 40), 3)

            if params.LEVEL[c][1]:
                pygame.draw.rect(params.screen, params.LEVEL[c][2],
                                 (params.width * 0.23 * i - params.width * 0.05 + 5, params.height * 0.75 + 5, 40 - 5 * 2, 40 - 5 * 2),
                                 0)
