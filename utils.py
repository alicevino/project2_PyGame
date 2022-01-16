import os
import random
import sys

import pygame

import params


def load_image(name, colorkey=None):
    fullname = os.path.join('data\pictures', name)
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


def set_text(text, color, xx, yy, size, pos):
    x, y = pos
    text = pygame.font.Font(None, size).render(text, True, color)
    params.screen.blit(text, (x - text.get_width() // 2 + xx, y - text.get_height() // 2 + yy))


def set_input_text(text, pos, size):
    for x in -2, 0, 2:
        for y in -2, 0, 2:
            set_text(text, params.THEME, x, y, size, pos)
    set_text(text, params.COLOR, 0, 0, size, pos)


def draw_button(pos, size, w=4):
    pygame.draw.rect(params.screen, params.THEME,
                     (pos[0] - (w + 2), pos[1] - (w + 2),
                      size[0] + (w + 2) * 2, size[1] + (w + 2) * 2),
                     0)
    pygame.draw.rect(params.screen, params.COLOR,
                     (pos[0], pos[1],
                      size[0], size[1]),
                     w)


class Coin(pygame.sprite.Sprite):
    image = load_image('mario coin_2.png')
    image = pygame.transform.scale(image, (40, 40))

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Coin.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(params.width - self.rect.w)
        self.rect.y = random.randrange(params.height - self.rect.h)
        self.v = random.randrange(10, 20)

    def update(self, *args):
        self.fall()

    def fall(self):
        self.rect.y += self.v
        if self.rect.y > params.height:
            self.rect.x = random.randrange(params.width - self.rect.w)
            self.rect.y = - self.rect.h


all_sprites = pygame.sprite.Group()
for _ in range(25):
    Coin(all_sprites)
