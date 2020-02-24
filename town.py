import pygame
import os
from random import randint

COLOR_COUNTRIES = {'Россия': []}


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

    def __init__(self, x, y, cell, cells, country):
        """Города - основная единица страны"""
        self.x = x
        self.y = y
        self.parent_cell = cell
        self.name_size = 10
        self.cells = cells
        self.country = country
        self.coords = cell.get_coords()
        self.name = pygame.font.Font(None, self.name_size)
        self.image = load_image('buildings/town.png', -1)
        country.units_towns.append(self)

    def render(self, coords, cell_size, screen):
        image = pygame.transform.scale(self.image, (int(cell_size - 15), int(cell_size - 15)))
        screen.blit(image, ((coords[0][0] + coords[5][0]) // 2 - 8, (coords[0][1] + coords[5][1]) // 2 - 3))

    def next_move(self):
        # self.amount_of_food += self.growth_of_food
        # self.country.food += self.growth_of_food
        pass

    def __str__(self):
        return 'Town'


class Country:

    def __init__(self, name, board, food=20, t_food=0, pr='NEW'):
        self.name = name
        self.board = board
        self.t_food = t_food
        self.food = food
        self.t_stone = 0
        self.stone = 0
        self.units_towns = []
        if pr == 'NEW':
            self.set_parameters()

    def set_parameters(self):
        dop = self.board.get_size()
        if dop is None:
            return
        dop_x, dop_y = dop
        x, y = randint(0, dop_x - 1), randint(0, dop_y - 1)
        while self.board.get_cell(x, y).type == 'Ocean':
            x, y = randint(0, dop_x - 1), randint(0, dop_y - 1)
        self.board.init_settlers(self, x, y, 'NEW')

    def render(self, screen, width, height):
        """Рисуем название страны"""
        font = pygame.font.Font(None, 50)
        text = font.render(self.name, 1, (0, 0, 0))
        text_x = width - text.get_width()
        text_y = text.get_height()
        screen.blit(text, (text_x, text_y))
        """Рисуем информацию о ресурсах"""
        t_food = font.render(f'Текущий прирост еды: {self.t_food}', 1, (0, 0, 0))
        t_food_x = width - t_food.get_width()
        t_food_y = t_food.get_height() * 2
        screen.blit(t_food, (t_food_x, t_food_y))
        food = font.render(f'Текущее количество еды: {self.food}', 1, (0, 0, 0))
        food_x = width - food.get_width()
        food_y = food.get_height() * 3
        screen.blit(food, (food_x, food_y))
        """Рисуем информацию об активном юните"""
        unit = self.board.get_active_unit()
        if not unit or unit.country.name != self.name:
            return
        name = font.render(f'Юнит: {unit.who()}', 1, (0, 0, 0))
        name_x = width - name.get_width()
        name_y = name.get_height() * 4
        health = font.render(f'Здоровье: {unit.health}', 1, (0, 0, 0))
        health_x = width - health.get_width()
        health_y = health.get_height() * 5
        screen.blit(name, (name_x, name_y))
        screen.blit(health, (health_x, health_y))

    def __str__(self):
        return 'Country'
