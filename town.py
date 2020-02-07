import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Town:

    def __init__(self, x, y, cell, cells):
        """Города - основная единица страны"""
        self.x = x
        self.y = y
        self.parent_cell = cell
        self.name_size = 10
        self.cells = cells
        self.coords = cell.get_coords()
        self.name = pygame.font.Font(None, self.name_size)
        self.image = load_image('город.png', -1)

    def render(self, coords, cell_size, screen):
        self.image = pygame.transform.scale(self.image, (cell_size - 15, cell_size - 15))
        screen.blit(self.image, ((coords[0][0] + coords[5][0]) // 2 - 8, (coords[0][1] + coords[5][1]) // 2 - 3))
