import pygame


class Town:

    def __init__(self, x, y, name, cell, cells):
        """Города - основная единица страны"""
        self.x = x
        self.y = y
        self.parent_cell = cell
        self.name_size = 10
        self.cells = cells
        self.name_town = name
        self.coords = cell.get_coords()
        self.name = pygame.font.Font(None, self.name_size)
        self.get_name_size()

    def get_name_size(self):
        """Подгоняем размер текста под размер клетки"""
        x = self.coords[0][0]
        y = self.coords[0][1]
        x1 = self.coords[1][0]
        y1 = self.coords[1][1]
        self.width = x1 - x
        self.height = y1 - y
        while self.name.size(self.name_town)[0] > self.width or \
                self.name.size(self.name_town)[1] > self.height:
            self.name_size -= 1
            self.name = pygame.font.Font(None, self.name_size)

    def render(self):
        pass
