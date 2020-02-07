import pygame
import random
from copy import deepcopy
from town import Town
from units import  Settlers


class Board:

    def __init__(self, count_cells_y: int, count_cells_x: int, cell_size: int, MONITOR_width, MONITOR_height):
        """
        Создаем поле игры,
        Первый параметр - количество клеток по ширине,
        Второй параметр - количество клеток по высоте,
        Третий - размер клеток
        Четвертый и пятый - размеры мониторы
        """
        self.MONITOR_width = MONITOR_width
        self.MONITOR_height = MONITOR_height
        self.MAX_ZOOM = 15
        self.T_ZOOM = 0
        self.MIN_ZOOM = -15
        self.count_x = count_cells_x
        self.count_y = count_cells_y
        self.cell_size = cell_size
        self.board = [[[] for _ in range(count_cells_y)] for __ in range(count_cells_x)]
        self.rect = [-50, -50, (count_cells_y + 3) * cell_size, (count_cells_x + 6) * cell_size]
        self.screen2 = pygame.Surface(((count_cells_y + 3) * cell_size, (count_cells_x - 6) * cell_size))
        self.x = -55
        self.y = -55
        self.initBoard()
        self.generate_field()

    def initBoard(self):
        """Заполняем игровую площадь клетками Cell"""
        x = self.cell_size
        for i in range(self.count_x):
            for j in range(self.count_y):
                if i % 2 == 0:
                    coords = [[x + j * x, 4 / 6 * i * x],
                              [3 / 2 * x + j * x, 4 / 6 * i * x + 1 / 3 * x],
                              [3 / 2 * x + j * x, 4 / 6 * i * x + 2 / 3 * x],
                              [x + j * x, 4 / 6 * i * x + x],
                              [1 / 2 * x + j * x, 4 / 6 * i * x + 2 / 3 * x],
                              [1 / 2 * x + j * x, 4 / 6 * i * x + 1 / 3 * x]]
                    self.board[i][j] = Cell(coords, self.cell_size, self, i, j)
                else:
                    coords = [[1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 2 / 3 * x],
                              [x + j * x, 4 / 6 * (i - 1) * x + x],
                              [x + j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x],
                              [1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 5 / 3 * x],
                              [j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x],
                              [j * x, 4 / 6 * (i - 1) * x + x]]
                    self.board[i][j] = Cell(coords, self.cell_size, self, i, j)
        self.init_town(3, 3)

    def render(self, screen):
        """Основная функция отрисовки поля"""
        for i in self.board:
            for j in i:
                j.render()
        screen.blit(self.screen2, (self.x + 100, self.y + 100))

    def button_pressed(self, x, y):
        """Определение нажатой клетки"""
        for i in range(self.count_x):
            for j in range(self.count_y):
                if self.board[i][j].check_is_pressed(x, y):
                    print(i, j)

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
        elif self.x > 0:
            self.x = 0
        if self.y > 0:
            self.y = 0
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
        board = deepcopy(self.board)
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
        return self.board

    def get_count_cells_x(self):
        """Возвращает количество клеток по ширине"""
        return self.count_x

    def get_count_cells_y(self):
        """Возвращает количество клеток по высоте"""
        return self.count_y

    def init_town(self, x, y):
        """Создает город в клетке с координатами x, y"""
        self.board[x][y].add_town()

    def get_cell(self, x, y):
        """Возвращает клетку с координатами x, y"""
        return self.board[x][y]

class Cell:

    def __init__(self, coords: list, cell_size, board, x, y):
        """Создаем клетку и задаем её координаты"""
        self.coords = coords
        self.cell_size = cell_size
        self.color = ''
        self.type = 'Nothing'
        self.sustenance = 0
        self.board = board
        self.x = x
        self.y = y
        self.town = ''
        self.town_on_cell = False
        self.unit_on_cell = False

    def render(self):
        """Основная функция отрисовки"""
        pygame.draw.polygon(self.board.screen2, pygame.Color('black'), self.coords, 4)
        if not self.town_on_cell:
            pygame.draw.polygon(self.board.screen2, self.color, self.coords)
        # if self.unit_on_cell:
        #     self.unit.render(self.coords, self.cell_size, self.board.screen2)
        if self.town_on_cell:
            self.town.render(self.coords, self.cell_size, self.board.screen2)

    def check_is_pressed(self, x: int, y: int) -> bool:
        """Проверяем была ли нажата именно эта клетка"""
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
        """Меняем тип клетки и загружаем её фоновое изображение"""
        self.type = type
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
                self.coords[i] = (self.coords[i][0] * 1.05 - 32, self.coords[i][1] * 1.05 - 18)
        if type == -1:
            for i in range(len(self.coords)):
                self.coords[i] = ((self.coords[i][0] + 32) / 1.05, (self.coords[i][1] + 18) / 1.05)

    def get_coords(self):
        """Возвращает координаты клетки"""
        return self.coords

    def add_town(self):
        """Добавление города"""
        dop = []
        for i in range(min(0, self.x - 1), min(self.board.get_count_cells_x(), self.x + 2)):
            for j in range(min(0, self.y - 1), min(self.board.get_count_cells_y(), self.y + 2)):
                dop.append(self.board.get_cell(i, j))
        self.town = Town(self.x, self.y, self, dop)
        self.town_on_cell = True

    def add_unit(self, unit):
        self.unit_on_cell = True
        self.unit = unit