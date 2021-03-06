import random
import pygame
from town import Town
from units import *


class Board:

    def __init__(self, count_cells_y: int, count_cells_x: int, MONITOR_width, MONITOR_height,
                 generate_field=True):
        """
        Создаем поле игры,
        Первый параметр - количество клеток по ширине,
        Второй параметр - количество клеток по высоте,
        Третий - размер клеток
        Четвертый и пятый - размеры мониторы
        """
        self.cities_and_belonging = [[('Neutral', False) for _ in range(count_cells_y)] for __ in range(count_cells_x)]
        self.color_country = {}
        with open('data/buildings/colors.txt', 'r', encoding='utf-8') as file:
            dop = file.readline()
            while dop != '':
                country_name, color = dop.split()
                self.color_country[country_name] = pygame.Color(color)
                dop = file.readline()
        self.MONITOR_width = MONITOR_width
        self.MONITOR_height = MONITOR_height
        self.MAX_ZOOM = 15
        self.T_ZOOM = 0
        self.MIN_ZOOM = -15
        self.count_x = count_cells_x
        self.count_y = count_cells_y
        self.cell_size = 60
        self.board = [[[] for _ in range(count_cells_y)] for __ in range(count_cells_x)]
        self.rect = [-600, -600, (count_cells_y + 3) * self.cell_size + 2200,
                     (count_cells_x + 6) * self.cell_size + 2200]
        self.screen2 = pygame.Surface(
            ((count_cells_y + 3) * self.cell_size + 2200, (count_cells_x - 6) * self.cell_size + 5200))
        self.x = -600
        self.y = -600
        self.active_cell = (0, 0)
        self.x_to_change = 0
        self.y_to_change = 0
        self.battle_mod = False
        self.active_country = None
        self.initBoard()
        if generate_field:
            self.generate_field()

    def get_size(self):
        """Возращает размеры поля"""
        return self.count_x, self.count_y

    def initBoard(self):
        """Заполняем игровую площадь клетками Cell"""
        x = self.cell_size
        for i in range(self.count_x):
            for j in range(self.count_y):
                if i % 2 == 0:
                    coords = [[x + j * x + 600, 4 / 6 * i * x + 600],
                              [3 / 2 * x + j * x + 600, 4 / 6 * i * x + 1 / 3 * x + 600],
                              [3 / 2 * x + j * x + 600, 4 / 6 * i * x + 2 / 3 * x + 600],
                              [x + j * x + 600, 4 / 6 * i * x + x + 600],
                              [1 / 2 * x + j * x + 600, 4 / 6 * i * x + 2 / 3 * x + 600],
                              [1 / 2 * x + j * x + 600, 4 / 6 * i * x + 1 / 3 * x + 600]]
                    self.board[i][j] = Cell(coords, self.cell_size, self, i, j)
                else:
                    coords = [[1 / 2 * x + j * x + 600, 4 / 6 * (i - 1) * x + 2 / 3 * x + 600],
                              [x + j * x + 600, 4 / 6 * (i - 1) * x + x + 600],
                              [x + j * x + 600, 4 / 6 * (i - 1) * x + 4 / 3 * x + 600],
                              [1 / 2 * x + j * x + 600, 4 / 6 * (i - 1) * x + 5 / 3 * x + 600],
                              [j * x + 600, 4 / 6 * (i - 1) * x + 4 / 3 * x + 600],
                              [j * x + 600, 4 / 6 * (i - 1) * x + x + 600]]
                    self.board[i][j] = Cell(coords, self.cell_size, self, i, j)

    def render(self, screen):
        """Основная функция отрисовки поля"""
        self.screen2.fill((128, 128, 128))
        for i in self.board:
            for j in i:
                j.render()
        screen.blit(self.screen2, (self.x + 100, self.y + 100))

    def __copy__(self):
        """Копия доски"""
        dop = []
        for i in self.board:
            dop1 = []
            for j in i:
                dop1.append(j.__copy__())
            dop.append(dop1)
        return dop

    def button_pressed(self, x, y):
        """Определение нажатой клетки"""
        for i in range(self.count_x):
            for j in range(self.count_y):
                if self.board[i][j].check_is_pressed(x, y):
                    if self.active_cell is None or (self.board[i][j].have_unit() and not self.battle_mod) or \
                            self.board[i][j].have_town():
                        if self.board[i][j].have_unit():
                            if self.board[i][j].unit.country.name == self.active_country.name:
                                self.active_cell = (i, j)
                        elif self.board[i][j].have_town():
                            if self.board[i][j].town.country.name == self.active_country.name:
                                self.active_cell = (i, j)
                    else:
                        if self.battle_mod:
                            try:
                                distance = self.board[self.active_cell[0]][self.active_cell[1]].unit.get_distance(i, j)
                                max_move = self.board[self.active_cell[0]][self.active_cell[1]].unit.get_max_move()
                                if distance > max_move:
                                    self.x_to_change = self.active_cell[0]
                                    self.y_to_change = self.active_cell[1]
                                    self.board[self.active_cell[0]][self.active_cell[1]].move_to(i, max(0, j - 1))
                                else:
                                    self.attack(i, j)
                                    self.battle_mod = False
                            except TypeError:
                                print('TypeError')
                                return
                            except AttributeError:
                                print('AttributeError')
                                return
                        elif self.board[self.active_cell[0]][self.active_cell[1]].have_unit():
                            self.x_to_change = self.active_cell[0]
                            self.y_to_change = self.active_cell[1]
                            self.board[self.active_cell[0]][self.active_cell[1]].move_to(i, j)
                        self.active_cell = None

    def get_active_unit(self):
        """Возращает активный юнит"""
        if self.active_cell is None:
            return False
        x, y = self.active_cell
        if self.board[x][y].have_unit():
            return self.board[x][y].get_unit()

    def heal(self):
        """Лечит активный юнит"""
        try:
            x, y = self.active_cell
            if self.board[x][y].unit.who() == 'Warriors':
                self.board[x][y].unit.heal()
        except TypeError:
            return
        except AttributeError:
            return

    def attack(self, x, y):
        """Атаковать юнит на клетке x, y"""
        x1, y1 = self.active_cell
        if self.board[x][y].unit.who() != 'Воины':
            return
        self.board[x][y].unit.health = self.board[x][y].unit.health - self.board[x1][y1].unit.take_damage()
        if self.board[x][y].unit.health <= 0:
            self.board[x][y].unit.live = 0
            self.board[x][y].unit = None
            self.board[x][y].unit_on_cell = False

    def activate_battle_mode(self):
        """Активация боевого режима"""
        self.battle_mod = True

    def zoom(self, koef):
        """Изменение размеров клеток"""
        if self.T_ZOOM == self.MAX_ZOOM and koef == 1:
            return
        elif self.T_ZOOM == self.MIN_ZOOM and koef == -1:
            return
        self.T_ZOOM += koef
        if type == 1:
            self.cell_size *= 2
        if type == -1:
            self.cell_size //= 2
        for i in self.board:
            for j in i:
                j.change_size(koef)

    def move(self, x, y):
        """Перемещение поля на котором рисуем"""
        self.x += x
        self.y += y
        if self.x + self.rect[2] < self.MONITOR_width:
            self.x = self.MONITOR_width - self.rect[2]
        elif self.x > -100:
            self.x = -100
        if self.y > -100:
            self.y = -100
        elif self.y + self.rect[3] < self.MONITOR_height:
            self.y = self.MONITOR_height - self.rect[3]

    def generate_field(self):
        """Создаем лист, описывающий типы клеток"""
        size_x = self.count_x
        size_y = self.count_y
        a = [['Nothing' for _ in range(size_x)] for __ in range(size_y)]
        i, j = random.randint(0, size_y - 1), random.randint(0, size_x - 1)
        a[i][j] = 'Desert'
        queue = [(i, j)]
        while a[i][j] != 'Nothing':
            i, j = random.randint(0, size_y - 1), random.randint(0, size_x - 1)
        queue.append((i, j))
        a[i][j] = 'Ocean'
        while a[i][j] != 'Nothing':
            i, j = random.randint(0, size_y - 1), random.randint(0, size_x - 1)
        queue.append((i, j))
        a[i][j] = 'Forest'
        while a[i][j] != 'Nothing':
            i, j = random.randint(0, size_y - 1), random.randint(0, size_x - 1)
        queue.append((i, j))
        a[i][j] = 'Meadow'  # Луг
        while a[i][j] != 'Nothing':
            i, j = random.randint(0, size_y - 1), random.randint(0, size_x - 1)
        queue.append((i, j))
        a[i][j] = 'Tundra'
        while len(queue) != 0:
            i, j = queue[0]
            list_neighbour = []
            if i % 2 == 1:
                if i >= 1 and j >= 1 and a[i - 1][j - 1] != 'Nothing':
                    list_neighbour.append(a[i - 1][j - 1])
                elif i >= 1 and j >= 1 and (i - 1, j - 1) not in queue:
                    queue.append((i - 1, j - 1))
                if i >= 1 and a[i - 1][j] != 'Nothing':
                    list_neighbour.append(a[i - 1][j])
                elif i >= 1 and (i - 1, j) not in queue:
                    queue.append((i - 1, j))
                if j < size_x - 1 and a[i][j + 1] != 'Nothing':
                    list_neighbour.append(a[i][j + 1])
                elif j < size_x - 1 and (i, j + 1) not in queue:
                    queue.append((i, j + 1))
                if i < size_y - 1 and a[i + 1][j] != 'Nothing':
                    list_neighbour.append(a[i + 1][j])
                elif i < size_y - 1 and (i + 1, j) not in queue:
                    queue.append((i + 1, j))
                if i < size_y - 1 and j >= 1 and a[i + 1][j - 1] != 'Nothing':
                    list_neighbour.append(a[i + 1][j - 1])
                elif i < size_y - 1 and j >= 1 and (i + 1, j - 1) not in queue:
                    queue.append((i + 1, j - 1))
                if j >= 1 and a[i][j - 1] != 'Nothing':
                    list_neighbour.append(a[i][j - 1])
                elif j >= 1 and (i, j - 1) not in queue:
                    queue.append((i, j - 1))
            if i % 2 == 0:
                if i >= 1 and a[i - 1][j] != 'Nothing':
                    list_neighbour.append(a[i - 1][j])
                elif i >= 1 and (i - 1, j) not in queue:
                    queue.append((i - 1, j))
                if i >= 1 and j < size_x - 1 and a[i - 1][j + 1] != 'Nothing':
                    list_neighbour.append(a[i - 1][j + 1])
                elif i >= 1 and j < size_x - 1 and (i - 1, j + 1) not in queue:
                    queue.append((i - 1, j + 1))
                if j < size_x - 1 and a[i][j + 1] != 'Nothing':
                    list_neighbour.append(a[i][j + 1])
                elif j < size_x - 1 and (i, j + 1) not in queue:
                    queue.append((i, j + 1))
                if i < size_y - 1 and j < size_x - 1 and a[i + 1][j + 1] != 'Nothing':
                    list_neighbour.append(a[i + 1][j + 1])
                elif i < size_y - 1 and j < size_x - 1 and (i + 1, j + 1) not in queue:
                    queue.append((i + 1, j + 1))
                if i < size_y - 1 and a[i + 1][j] != 'Nothing':
                    list_neighbour.append(a[i + 1][j])
                elif i < size_y - 1 and (i + 1, j) not in queue:
                    queue.append((i + 1, j))
                if j >= 1 and a[i][j - 1] != 'Nothing':
                    list_neighbour.append(a[i][j - 1])
                elif j >= 1 and (i, j - 1) not in queue:
                    queue.append((i, j - 1))
            if a[i][j] == 'Nothing':
                a[i][j] = random.choice(list_neighbour)
            del queue[0]
        self.field_to_cells(a)

    def field_to_cells(self, field):
        """Записываем результат в клетки"""
        for i, v in enumerate(self.board):
            for j, k in enumerate(v):
                k.change_type(field[j][i])

    def get_board(self):
        """Передаем поле с условными обозначениями"""
        # Вода - 0
        # Лес - 1
        # Луг - 2
        # Тундра - 3
        # Пустыня - 4
        board = self.__copy__()
        for i, v in enumerate(board):
            for j, value in enumerate(v):
                if value.type == 'Ocean':
                    board[i][j] = 0
                elif value.type == 'Forest':
                    board[i][j] = 1
                elif value.type == 'Meadow':
                    board[i][j] = 2
                elif value.type == 'Tundra':
                    board[i][j] = 3
                elif board[i][j] == 'Desert':
                    board[i][j] = 4
        return board

    def get_count_cells_x(self):
        """Возвращает количество клеток по ширине"""
        return self.count_x

    def get_count_cells_y(self):
        """Возвращает количество клеток по высоте"""
        return self.count_y

    def init_town(self, x, y, country):
        """Создает город в клетке с координатами x, y"""
        try:
            if x == y == -1:
                if self.board[self.active_cell[0]][self.active_cell[1]].unit.who() == 'Поселенцы':
                    self.board[self.active_cell[0]][self.active_cell[1]].add_town(country)
                    self.board[self.active_cell[0]][self.active_cell[1]].del_unit()
            else:
                self.board[int(x)][int(y)].add_town(country)
        except TypeError:
            return
        except AttributeError:
            return

    def get_cell(self, x, y):
        """Возвращает клетку с координатами x, y"""
        return self.board[x][y]

    def get_town(self, x, y):
        """Достает город из клетки x, y"""
        return self.board[x][y].get_town()

    def change_cell(self, x1, y1, x=-1, y=-1):
        """Меняем юнита на двух клетках"""
        if x == y == -1:
            x = self.x_to_change
            y = self.y_to_change
        dop = self.board[x][y].get_unit()
        if dop is None:
            return
        self.board[x][y].del_unit()
        self.board[x1][y1].add_unit(dop)

    def init_settlers(self, country, x=-1, y=-1, pr='OLD'):
        """Создаем поселенцев"""
        if pr == 'SAVE':
            self.board[x][y].add_settlers(Settlers(x, y, country, self))
            return
        try:
            if self.active_cell is None or self.active_country.food <= 0:
                return
        except AttributeError:
            if self.active_cell is None and pr == 'OLD':
                return
        if x == y == -1:
            x, y = self.active_cell
        if pr == 'NEW':
            self.board[x][y].add_settlers(Settlers(x, y, country, self))
            return
        if not self.board[x][y].have_town():
            return
        if x % 2 == 0:
            for i in range(max(0, x - 1), min(x + 2, self.count_x)):
                for j in range(max(0, y - 1), min(y + 2, self.count_y)):
                    if i == x - 1 and j == y - 1 or i == x + 1 and j == y - 1 or self.board[i][j].type == 'Ocean':
                        continue
                    if not self.board[i][j].have_unit() and not self.board[i][j].have_town():
                        self.board[i][j].add_unit(Settlers(i, j, country, self))
                        self.active_country.food -= 10
                        return
        else:
            for i in range(max(0, x - 1), min(x + 2, self.count_x)):
                for j in range(max(0, y - 1), min(y + 2, self.count_y)):
                    if i == x - 1 and j == y + 1 or i == x + 1 and j == y + 1 or self.board[i][j].type == 'Ocean':
                        continue
                    if not self.board[i][j].have_unit() and not self.board[i][j].have_town():
                        self.board[i][j].add_unit(Settlers(i, j, country, self))
                        self.active_country.food -= 10
                        return

    def next_move(self, country):
        """Следующий ход"""
        dop = []
        for i in self.board:
            for j in i:
                if j.have_unit() or j.have_town():
                    dop.append(j)
        for i in dop:
            try:
                if i.unit.country.name == self.active_country.name:
                    i.next_move()
            except AttributeError:
                if i.town.country.name == self.active_country.name:
                    i.next_move()
        self.active_country = country
        self.battle_mod = False

    def init_builders(self, x=-1, y=-1, country=None):
        """Создаем строителей вокруг города"""
        if x != -1 and y != -1:
            self.board[int(x)][int(y)].add_builders(Builders(x, y, country, self))
            return
        try:
            if self.active_cell is None or self.active_country.food <= 0:
                return
        except AttributeError:
            if self.active_cell is None:
                return
        x, y = self.active_cell
        if not self.board[x][y].have_town():
            return
        if x % 2 == 0:
            for i in range(max(0, x - 1), min(x + 2, self.count_x)):
                for j in range(max(0, y - 1), min(y + 2, self.count_y)):
                    if i == x - 1 and j == y - 1 or i == x + 1 and j == y - 1 or self.board[i][j].type == 'Ocean':
                        continue
                    if not self.board[i][j].have_unit() and not self.board[i][j].have_town():
                        self.board[i][j].add_unit(Builders(i, j, self.active_country, self))
                        self.active_country.food -= 10
                        return
        else:
            for i in range(max(0, x - 1), min(x + 2, self.count_x)):
                for j in range(max(0, y - 1), min(y + 2, self.count_y)):
                    if i == x - 1 and j == y + 1 or i == x + 1 and j == y + 1 or self.board[i][j].type == 'Ocean':
                        continue
                    if not self.board[i][j].have_unit() and not self.board[i][j].have_town():
                        self.board[i][j].add_unit(Builders(i, j, self.active_country, self))
                        self.active_country.food -= 10
                        return

    def get_coords(self):
        """Возращает текущие координаты левого верзнего угла второго экрана"""
        return self.x, self.y

    def init_farm(self, country, pr='OLD', x=-1, y=-1):
        """Создает ферму"""
        if pr == 'SAVE':
            self.board[x][y].add_farm(country)
            country.units_towns.append(f'Farm {x} {y}')
        try:
            if self.board[self.active_cell[0]][self.active_cell[1]].unit.who() == 'Строители':
                self.board[self.active_cell[0]][self.active_cell[1]].add_farm(
                    self.board[self.active_cell[0]][self.active_cell[1]].unit.country)
                self.board[self.active_cell[0]][self.active_cell[1]].del_unit()
                country.units_towns.append(f'Farm {self.active_cell[0]} {self.active_cell[1]}')
        except TypeError:
            return
        except AttributeError:
            return

    def init_warriors(self, country, x=-1, y=-1, health=20):
        """Создает воинов"""
        if x != -1 and y != -1:
            self.board[x][y].add_warriors(Warriors(x, y, country, self, health, from_save=True))
        try:
            if self.active_cell is None or self.active_country.food <= 0:
                return
        except AttributeError:
            if self.active_cell is None:
                return
        x, y = self.active_cell
        if not self.board[x][y].have_town():
            return
        if x % 2 == 0:
            for i in range(max(0, x - 1), min(x + 2, self.count_x)):
                for j in range(max(0, y - 1), min(y + 2, self.count_y)):
                    if i == x - 1 and j == y - 1 or i == x + 1 and j == y - 1 or self.board[i][j].type == 'Ocean':
                        continue
                    if not self.board[i][j].have_unit() and not self.board[i][j].have_town():
                        self.board[i][j].add_unit(Warriors(i, j, country, self))
                        self.active_country.food -= 10
                        return
        else:
            for i in range(max(0, x - 1), min(x + 2, self.count_x)):
                for j in range(max(0, y - 1), min(y + 2, self.count_y)):
                    if i == x - 1 and j == y + 1 or i == x + 1 and j == y + 1 or self.board[i][j].type == 'Ocean':
                        continue
                    if not self.board[i][j].have_unit() and not self.board[i][j].have_town():
                        self.board[i][j].add_unit(Warriors(i, j, country, self))
                        self.active_country.food -= 10
                        return

    def set_cell(self, x, y, type):
        """Изменение типа клетки"""
        self.board[x][y].change_type(type)


class Cell:
    """Класс игровой клетки"""

    def __init__(self, coords: list, cell_size, board, x, y, type='Nothing'):
        """Создаем клетку и задаем её координаты"""
        self.color = pygame.Color('Black')
        self.coords = coords
        self.cell_size = cell_size
        self.color = ''
        self.type = type
        self.sustenance = 0
        self.board = board
        self.x = x
        self.y = y
        self.town = None
        self.unit = None
        self.town_on_cell = False
        self.unit_on_cell = False
        self.farm_on_cell = False

    def render(self):
        """Основная функция отрисовки"""
        pygame.draw.polygon(self.board.screen2, pygame.Color('black'), self.coords, 4)
        pygame.draw.polygon(self.board.screen2, self.color, self.coords)
        if self.town_on_cell:
            self.town.render(self.coords, self.cell_size, self.board.screen2)
        if self.farm_on_cell:
            dop = pygame.transform.scale(self.image_farm, (int(self.cell_size - 15), int(self.cell_size - 15)))
            self.board.screen2.blit(dop, (
                (self.coords[0][0] + self.coords[5][0]) // 2 - 8, (self.coords[0][1] + self.coords[5][1]) // 2 - 3))
        if self.unit_on_cell:
            self.unit.render(self.coords, self.cell_size, self.board.screen2)
        cities_and_belonging = self.board.cities_and_belonging
        i = self.x
        j = self.y
        size_x = self.board.get_count_cells_x()
        size_y = self.board.get_count_cells_y()
        if i % 2 == 1:
            if i >= 1 and j >= 1:
                if cities_and_belonging[i - 1][j - 1][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[5][0] + 2, self.coords[5][1] + 2),
                                     (self.coords[0][0] + 2, self.coords[0][1] + 2), 4)
            if i >= 1:
                if cities_and_belonging[i - 1][j][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[0][0] - 2, self.coords[0][1] + 2),
                                     (self.coords[1][0] - 2, self.coords[1][1] + 1), 4)
            if j < size_y - 1:
                if cities_and_belonging[i][j + 1][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[1][0] - 2, self.coords[1][1]),
                                     (self.coords[2][0] - 2, self.coords[2][1]), 5)
            if i < size_x - 1:
                if cities_and_belonging[i + 1][j][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[2][0] - 2, self.coords[2][1] - 2),
                                     (self.coords[3][0] - 2, self.coords[3][1] - 2), 5)
            if i < size_x - 1 and j >= 1:
                if cities_and_belonging[i + 1][j - 1][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[3][0] + 2, self.coords[3][1] - 2),
                                     (self.coords[4][0] + 2, self.coords[4][1] - 2), 5)
            if j >= 1:
                if cities_and_belonging[i][j - 1][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[4][0] + 2, self.coords[4][1]),
                                     (self.coords[5][0] + 2, self.coords[5][1]), 4)
        if i % 2 == 0:
            if i >= 1:
                if cities_and_belonging[i - 1][j][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[5][0] + 2, self.coords[5][1] + 2),
                                     (self.coords[0][0] + 2, self.coords[0][1] + 2), 4)
            if i >= 1 and j < size_y - 1:
                if cities_and_belonging[i - 1][j + 1][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[0][0] - 2, self.coords[0][1] + 2),
                                     (self.coords[1][0] - 2, self.coords[1][1] + 2), 4)
            if j < size_y - 1:
                if cities_and_belonging[i][j + 1][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[1][0] - 2, self.coords[1][1]),
                                     (self.coords[2][0] - 2, self.coords[2][1]), 5)
            if i < size_x - 1 and j < size_y - 1:
                if cities_and_belonging[i + 1][j + 1][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[2][0] - 2, self.coords[2][1] - 2),
                                     (self.coords[3][0] - 2, self.coords[3][1] - 2), 5)
            if i < size_x - 1:
                if cities_and_belonging[i + 1][j][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[3][0] + 2, self.coords[3][1] - 2),
                                     (self.coords[4][0] + 2, self.coords[4][1] - 2), 5)
            if j >= 1:
                if cities_and_belonging[i][j - 1][0] != cities_and_belonging[i][j][0]:
                    pygame.draw.line(self.board.screen2, self.board.color_country[cities_and_belonging[i][j][0]],
                                     (self.coords[4][0] + 2, self.coords[4][1]),
                                     (self.coords[5][0] + 2, self.coords[5][1]), 4)

    def check_is_pressed(self, x: int, y: int) -> bool:
        """Проверяем была ли нажата именно эта клетка"""
        x += 500 - (600 + self.board.get_coords()[0])
        y += 500 - (600 + self.board.get_coords()[1])
        coords = self.coords
        fl = True
        for v in range(-1, 1):
            x1, y1, x2, y2 = coords[(v + 6) % 6][0], coords[(v + 6) % 6][1], coords[(v + 7) % 6][0], \
                             coords[(v + 7) % 6][1]
            if y < (x - x1) * (y2 - y1) / (x2 - x1) + y1:
                fl = False
        for v in range(2, 4):
            x1, y1, x2, y2 = coords[v][0], coords[v][1], coords[v + 1][0], \
                             coords[v + 1][1]
            if y > (x - x1) * (y2 - y1) / (x2 - x1) + y1:
                fl = False
        if x < coords[4][0] or x > coords[2][0]:
            fl = False
        if fl:
            return True
        else:
            return False

    def change_type(self, type):
        """Меняем тип клетки и задаем ее цвет"""
        self.type = str(type)
        if type == 'Forest':
            self.color = pygame.Color('#013220')
        elif type == 'Meadow':
            self.color = pygame.Color('#228b22')
        elif type == 'Ocean':
            self.color = pygame.Color('#4169e1')
        elif type == 'Tundra':
            self.color = pygame.Color('#e6e6fa')
        elif type == 'Desert':
            self.color = pygame.Color('#f7e96d')

    def change_size(self, type):
        """Изменить размер клетки"""
        if type == 1:
            for i in range(len(self.coords)):
                self.coords[i] = [self.coords[i][0] * 1.05 - 32, self.coords[i][1] * 1.05 - 18]
            self.cell_size *= 1.035
        if type == -1:
            for i in range(len(self.coords)):
                self.coords[i] = [(self.coords[i][0] + 32) / 1.05, (self.coords[i][1] + 18) / 1.05]
            self.cell_size /= 1.035

    def get_coords(self):
        """Возвращает координаты клетки"""
        return self.coords

    def get_town(self):
        """Возращает город, если он существует"""
        if self.town_on_cell:
            return self.town
        return False

    def add_town(self, country):
        """Добавление города"""
        cities_and_belonging = self.board.cities_and_belonging
        dop = []
        i = self.x
        j = self.y
        size_x = self.board.get_count_cells_x()
        size_y = self.board.get_count_cells_y()
        cities_and_belonging[i][j] = (country.name, True)
        if i % 2 == 1:
            if i >= 1 and j >= 1:
                cities_and_belonging[i - 1][j - 1] = (country.name, False)
                dop.append(self.board.get_cell(i - 1, j - 1))
            if i >= 1:
                cities_and_belonging[i - 1][j] = (country.name, False)
                dop.append(self.board.get_cell(i - 1, j))
            if j < size_y - 1:
                cities_and_belonging[i][j + 1] = (country.name, False)
                dop.append(self.board.get_cell(i, j + 1))
            if i < size_x - 1:
                cities_and_belonging[i + 1][j] = (country.name, False)
                dop.append(self.board.get_cell(i + 1, j))
            if i < size_x - 1 and j >= 1:
                cities_and_belonging[i + 1][j - 1] = (country.name, False)
                dop.append(self.board.get_cell(i + 1, j - 1))
            if j >= 1:
                cities_and_belonging[i][j - 1] = (country.name, False)
                dop.append(self.board.get_cell(i, j - 1))
        if i % 2 == 0:
            if i >= 1:
                cities_and_belonging[i - 1][j] = (country.name, False)
                dop.append(self.board.get_cell(i - 1, j))
            if i >= 1 and j < size_y - 1:
                cities_and_belonging[i - 1][j + 1] = (country.name, False)
                dop.append(self.board.get_cell(i - 1, j + 1))
            if j < size_y - 1:
                cities_and_belonging[i][j + 1] = (country.name, False)
                dop.append(self.board.get_cell(i - 1, j + 1))
            if i < size_x - 1 and j < size_y - 1:
                cities_and_belonging[i + 1][j + 1] = (country.name, False)
                dop.append(self.board.get_cell(i + 1, j + 1))
            if i < size_x - 1:
                cities_and_belonging[i + 1][j] = (country.name, False)
                dop.append(self.board.get_cell(i + 1, j))
            if j >= 1:
                cities_and_belonging[i][j - 1] = (country.name, False)
                dop.append(self.board.get_cell(i, j - 1))
        self.town = Town(self.x, self.y, self, dop, country)
        self.town_on_cell = True
        self.unit_on_cell = False
        self.unit.live = 0
        self.unit = None

    def add_settlers(self, unit):
        """Добавление поселенцев на клетку"""
        self.unit_on_cell = True
        self.unit = unit
        unit.country.units_towns.append(unit)

    def add_builders(self, unit):
        """Добавление строителей в клетку"""
        self.unit_on_cell = True
        self.unit = unit
        unit.country.units_towns.append(unit)

    def have_unit(self):
        """Определяет есть ли в клетке юнит"""
        return self.unit_on_cell

    def have_town(self):
        """Определяет есть в клетке город"""
        return self.town_on_cell

    def get_unit(self):
        """Возвращает юнит, если тот существует"""
        if self.unit_on_cell:
            return self.unit

    def del_unit(self):
        """Удаление юнита из клетки"""
        # del self.unit.country.units_towns[self.unit.country.units_towns.index(self)]
        self.unit_on_cell = False
        self.unit = None

    def add_unit(self, unit):
        """Добавление юнита в клетку"""
        who = unit.who()
        if who == 'Поселенцы':
            self.add_settlers(unit)
        elif who == 'Строители':
            self.add_builders(unit)
        elif who == 'Воины':
            self.add_warriors(unit)

    def move_to(self, x, y):
        """Передвижение юнита на координаты x, y"""
        self.unit.move(x, y)

    def __copy__(self):
        """Возращает копию клетки"""
        return Cell(self.coords, self.cell_size, self.board, self.x, self.y)

    def __str__(self):
        """Приводит клетку в виду: x-координата y-координата юнит на этой клетке"""
        return ' '.join([str(self.x), str(self.y), str(self.unit)])

    def next_move(self):
        """Следующий ход"""
        if self.unit_on_cell:
            self.unit.update()
            self.unit.next_move()
        if self.town_on_cell:
            self.town.next_move()

    def add_farm(self, country):
        """Добавляет ферму в клетку"""
        if not self.farm_on_cell:
            self.farm_on_cell = True
            country.t_food += 3
            if self.unit is not None:
                self.unit.live = 0
            self.image_farm = load_image('buildings/farm.png', -1)

    def add_warriors(self, unit):
        """Добавление воинов на клетку"""
        self.unit_on_cell = True
        self.unit = unit
        unit.country.units_towns.append(unit)
