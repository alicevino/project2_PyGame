import params
import utils


class FinishWindow:
    def __init__(self):
        utils.all_sprites.update()
        utils.all_sprites.draw(params.screen)

        utils.draw_button((params.width * 0.3, params.height * 0.7), (params.width * 0.4, params.height * 0.1))
        utils.set_input_text('ИГРАТЬ СНОВА', (params.width * 0.5, params.height * 0.75), 50)

        utils.draw_button(
            (params.width * 0.78, params.height * 0.03),
            (params.width * 0.2, params.height * 0.07),
            2)
        utils.set_input_text('выйти из игры',
                       (params.width * 0.88, params.height * 0.065),
                       30)

        self.draw_profit()

    def draw_profit(self):
        if params.profit > 0:
            utils.set_input_text(f"ВЫ ВЫИГРАЛИ!", (params.width * 0.5, params.height * 0.35), 90)
            utils.set_text(f'ваша прибыль составила: +{params.profit} y.e.', 'red', 0, 0, 55, (params.width * 0.5, params.height * 0.45))
        else:
            utils.set_input_text(f"ВЫ ПРОИГРАЛИ :(", (params.width * 0.5, params.height * 0.35), 90)
            utils.set_text(f'ваш убыток составил: {params.profit} y.e.', 'red', 0, 0, 55, (params.width * 0.5, params.height * 0.45))
        utils.set_input_text(f"Попробуйте сыграть снова", (params.width * 0.5, params.height * 0.6), 40)
        utils.set_input_text(f"и добиться лучших результатов!", (params.width * 0.5, params.height * 0.65), 40)
