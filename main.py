"""
Основной игровой цикл. Обеспечивает реакцию на события
и переключения между игровыми окнами.
"""

import pygame

import params

# Инициализация библиотеки
pygame.init()
size = params.width, params.height = 900, 650
params.screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игра БИРЖА')

import utils

import start_window
import level_window
import game_window
import finish_window

# if __name__ == '__main__':

running = True
fps = 60
clock = pygame.time.Clock()
window = start_window.StartWindow()

# Основной цикл
while running:
    params.screen.fill(params.THEME)
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # изменение цветовой темы
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.02 <= event.pos[0] <= params.width * 0.27
                    and params.height * 0.03 <= event.pos[1] < params.height * 0.1):
                if params.WINDOW == 'start':
                    params.THEME, params.COLOR = params.COLOR, params.THEME

        # choose_level()
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.23 * 1 - params.width * 0.05 <= event.pos[0] <= params.width * 0.23 * 4 - params.width * 0.05 + 40
                    and params.height * 0.75 <= event.pos[1] < params.height * 0.75 + 40):
                if params.WINDOW == 'level':
                    window.choose_level(event.pos)

        # переход from start to level
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.3 <= event.pos[0] <= params.width * 0.7
                    and params.height * 0.7 <= event.pos[1] < params.height * 0.8):
                if params.WINDOW == 'start':
                    params.WINDOW = 'level'

        # переход from level to start
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.02 <= event.pos[0] <= params.width * 0.12
                    and params.height * 0.03 <= event.pos[1] < params.height * 0.1):
                if params.WINDOW == 'level':
                    params.WINDOW = 'start'

        # переход from level to game
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.82 <= event.pos[0] <= params.width * 0.9752
                    and params.height * 0.875 <= event.pos[1] < params.height * 0.975):
                if params.WINDOW == 'level':
                    window.play()

        # выход из игры
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.78 <= event.pos[0] <= params.width * 0.98
                    and params.height * 0.03 <= event.pos[1] < params.height * 0.1):
                if params.WINDOW == 'finish' or params.WINDOW == 'start':
                    running = False

        # переход from game to finish
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.725 <= event.pos[0] <= params.width * 0.975
                    and params.height * 0.03 <= event.pos[1] < params.height * 0.1):
                if params.WINDOW == 'game':
                    params.WINDOW = 'finish'

        # переход from finish to start
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.3 <= event.pos[0] <= params.width * 0.7
                    and params.height * 0.7 <= event.pos[1] < params.height * 0.8):
                if params.WINDOW == 'finish':
                    params.WINDOW = 'start'

        # переход на окно настроек hide alert
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if not (params.width * 0.36 <= event.pos[0] <= params.width * 0.64
                    and params.height * 0.42 <= event.pos[1] < params.height * 0.58
                    or params.width * 0.82 <= event.pos[0] <= params.width * 0.9752
                    and params.height * 0.875 <= event.pos[1] < params.height * 0.975):
                if params.WINDOW == 'level':
                    params.ALERT = False

        # изменение выбранных компаний
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.6 - 5 <= event.pos[0] <= params.width * 0.65 - 9 + 25 and
                    params.height * 0.045 + params.height * 0.05 - 5 <= event.pos[1] < params.height * 0.045 + params.height * 0.05 * len(
                        params.PL) - 5 + 25):
                # print(len(PL))
                if params.WINDOW == 'game':
                    window.shange_stock_num(event.pos)

        # контекстная подсказка - профит
        if event.type == pygame.MOUSEMOTION:
            if params.WINDOW == 'game':
                if 650 <= event.pos[0] <= 800 and 115 <= event.pos[1] <= 130:
                    params.HINT_PROF = True
                else:
                    params.HINT_PROF = False
        
        # контекстная подсказка - тикер
        if event.type == pygame.MOUSEMOTION:
            if params.WINDOW == 'game':
                if 115 <= event.pos[0] <= 140 and 50 <= event.pos[1] <= 70:
                    params.HINT_TICK = True
                else:
                    params.HINT_TICK = False

        # контекстная подсказка - котировка
        if event.type == pygame.MOUSEMOTION:
            if params.WINDOW == 'game':
                if 230 <= event.pos[0] <= 260 and 50 <= event.pos[1] <= 70:
                    params.HINT_COT = True
                else:
                    params.HINT_COT = False

        # finish_window stars
        if event.type == pygame.MOUSEBUTTONUP:
            if params.WINDOW == 'finish':
                utils.all_sprites_coins.update(event)

    # Выбор рабочего окна
    if params.WINDOW == 'start':
        window = start_window.StartWindow()
    elif params.WINDOW == 'level':
        window = level_window.LevelWindow()
    elif params.WINDOW == 'game':
        window = game_window.GameWindow()
    elif params.WINDOW == 'finish':
        window = finish_window.FinishWindow()

    clock.tick(fps)
    # обновление экрана
    pygame.display.flip()
pygame.quit()
