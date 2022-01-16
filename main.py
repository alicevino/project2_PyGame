import pygame

import params
# import data_reader

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

while running:
    params.screen.fill(params.THEME)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # theme changing
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.02 <= event.pos[0] <= params.width * 0.27
                    and params.height * 0.03 <= event.pos[1] < params.height * 0.1):
                if params.WINDOW == 'start':
                    params.THEME, params.COLOR = params.COLOR, params.THEME
        # choose_level()
        # if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
        #     if (width * 0.23 * 1 - width * 0.05 <= event.pos[0] <= width * 0.23 * 4 - width * 0.05 + 40
        #             and height * 0.75 <= event.pos[1] < height * 0.75 + 40):
        #         if WINDOW == 'level':
        #             window.choose_level(event.pos)
        # from start to level
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.3 <= event.pos[0] <= params.width * 0.7
                    and params.height * 0.7 <= event.pos[1] < params.height * 0.8):
                if params.WINDOW == 'start':
                    params.WINDOW = 'level'
        # from level to start
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.02 <= event.pos[0] <= params.width * 0.12
                    and params.height * 0.03 <= event.pos[1] < params.height * 0.1):
                if params.WINDOW == 'level':
                    params.WINDOW = 'start'
        # from level to game
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.82 <= event.pos[0] <= params.width * 0.9752
                    and params.height * 0.875 <= event.pos[1] < params.height * 0.975):
                if params.WINDOW == 'level':
                    window.play()
        # quit the game
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.78 <= event.pos[0] <= params.width * 0.98
                    and params.height * 0.03 <= event.pos[1] < params.height * 0.1):
                if params.WINDOW == 'finish' or params.WINDOW == 'start':
                    running = False
        # from game to finish
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.725 <= event.pos[0] <= params.width * 0.975
                    and params.height * 0.03 <= event.pos[1] < params.height * 0.1):
                if params.WINDOW == 'game':
                    params.WINDOW = 'finish'
        # from finish to start
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.3 <= event.pos[0] <= params.width * 0.7
                    and params.height * 0.7 <= event.pos[1] < params.height * 0.8):
                if params.WINDOW == 'finish':
                    params.WINDOW = 'start'
        # hide alert
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if not (params.width * 0.36 <= event.pos[0] <= params.width * 0.64
                    and params.height * 0.42 <= event.pos[1] < params.height * 0.58
                    or params.width * 0.82 <= event.pos[0] <= params.width * 0.9752
                    and params.height * 0.875 <= event.pos[1] < params.height * 0.975):
                if params.WINDOW == 'level':
                    params.ALERT = False
        # change_stock_num()
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if (params.width * 0.6 - 5 <= event.pos[0] <= params.width * 0.65 - 9 + 25 and
                    params.height * 0.045 + params.height * 0.05 - 5 <= event.pos[1] < params.height * 0.045 + params.height * 0.05 * len(
                        params.PL) - 5 + 25):
                # print(len(PL))
                if params.WINDOW == 'game':
                    window.shange_stock_num(event.pos)
        # контекстная подсказка PROFIT
        if event.type == pygame.MOUSEMOTION:
            if params.WINDOW == 'game':
                if 650 <= event.pos[0] <= 800 and 115 <= event.pos[1] <= 130:
                    HINT = True
                else:
                    HINT = False
        # finish_window stars
        if event.type == pygame.MOUSEBUTTONUP:
            if params.WINDOW == 'finish':
                utils.all_sprites_coins.update(event)

    if params.WINDOW == 'start':
        window = start_window.StartWindow()
    elif params.WINDOW == 'level':
        window = level_window.LevelWindow()
    elif params.WINDOW == 'game':
        window = game_window.GameWindow()
    elif params.WINDOW == 'finish':
        window = finish_window.FinishWindow()

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
