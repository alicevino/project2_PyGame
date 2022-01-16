import data_reader
import params
import utils


class StartWindow:
    def __init__(self):
        params.LEVEL = {
            'CVX': [data_reader.data_cvx, True, 'red', 0],
            'TSM': [data_reader.data_tsm, True, 'green', 0],
            'ABBV': [data_reader.data_abbv, True, 'blue', 0],
            'SONY': [data_reader.data_sony, True, 'orange', 0],
        }
        params.PL = ['CVX', 'TSM', 'ABBV', 'SONY']
        params.ROBOT = {
            'CVX': [True, 0, 0],
            'TSM': [True, 0, 0],
            'ABBV': [True, 0, 0],
            'SONY': [True, 0, 0],
        }

        utils.all_sprites_coins.update()
        utils.all_sprites_coins.draw(params.screen)

        utils.set_input_text("ИГРА БИРЖА", (params.width // 2, params.height // 2), 100)

        utils.draw_button((params.width * 0.3, params.height * 0.7), (params.width * 0.4, params.height * 0.1))
        utils.set_input_text('ИГРАТЬ', (params.width * 0.5, params.height * 0.75), 50)

        utils.draw_button(
            (params.width * 0.02, params.height * 0.03),
            (params.width * 0.25, params.height * 0.07),
            2)
        utils.set_input_text('изменить цвет темы',
                       (params.width * 0.145, params.height * 0.065),
                       30)

        utils.draw_button(
            (params.width * 0.78, params.height * 0.03),
            (params.width * 0.2, params.height * 0.07),
            2)
        utils.set_input_text('выйти из игры',
                       (params.width * 0.88, params.height * 0.065),
                       30)
