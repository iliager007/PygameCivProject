import pygame
from win32api import GetSystemMetrics
import random
import os

COLOR = pygame.Color('white')


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


class Board:

    def __init__(self, count_cells_y: int, count_cells_x: int, cell_size: int):
        """
        Создаем поле игры,
        Первый параметр - количество клеток по ширине,
        Второй параметр - количество клеток по высоте,
        Третий - размер клеток
        """
        self.count_x = count_cells_x
        self.count_y = count_cells_y
        self.cell_size = cell_size
        self.board = [[[] for _ in range(count_cells_y)] for __ in range(count_cells_x)]
        self.rect = [-50, -50, (count_cells_y + 3) * cell_size, (count_cells_x - 6) * cell_size]
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
                    self.board[i][j] = Cell(coords, self.cell_size)
                else:
                    coords = [[1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 2 / 3 * x],
                              [x + j * x, 4 / 6 * (i - 1) * x + x],
                              [x + j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x],
                              [1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 5 / 3 * x],
                              [j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x],
                              [j * x, 4 / 6 * (i - 1) * x + x]]
                    self.board[i][j] = Cell(coords, self.cell_size)

    def render(self):
        """Основная функция отрисовки поля"""
        for i in self.board:
            for j in i:
                j.render()
        screen.blit(board.screen2, (self.x + 100, self.y + 100))

    def button_pressed(self, x, y):
        """Определение нажатой клетки"""
        for i in range(self.count_x):
            for j in range(self.count_y):
                if self.board[i][j].check_is_pressed(x, y):
                    print(i, j)

    def zoom(self, koef):
        pass
        # if koef == 1:
        #     for i in self.board:
        #         for j in i:
        #             j += (8, 4.5)
        # elif koef == -1:
        #     for i in self.board:
        #         for j in i:
        #             j += (-8, -4.5)

    def move(self, x, y):
        self.x += x
        self.y += y
        if self.x + self.rect[2] < MONITOR_width:
            self.x = MONITOR_width - self.rect[2]
        elif self.x > 0:
            self.x = 0
        if self.y > 0:
            self.y = 0
        elif self.y + self.rect[3] < MONITOR_height:
            self.y = MONITOR_height - self.rect[3]

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


class Cell:

    def __init__(self, coords: list, cell_size):
        """Создаем клетку и задаем её координаты"""
        self.coords = coords
        self.cell_size = cell_size
        self.color = ''
        self.image = ''

    def render(self):
        """Основная функция отрисовки"""
        pygame.draw.polygon(board.screen2, self.color, self.coords)

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
        print(1)
        image = load_image(type + '.png')
        self.image = pygame.transform.scale(image, (self.cell_size, self.cell_size))
        if type == 'Forest' or type == 'Meadow':
            self.color = pygame.Color('#228b22')
        elif type == 'Ocean':
            self.color = pygame.Color('#4169e1')
        elif type == 'Tundra':
            self.color = pygame.Color('#e6e6fa')
        elif type == 'Desert':
            self.color = pygame.Color('#f7e96d')


pygame.init()
MONITOR_width = GetSystemMetrics(0)
MONITOR_height = GetSystemMetrics(1)
size = (MONITOR_width, MONITOR_height)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill((0, 0, 0))

fps = 60
clock = pygame.time.Clock()
board = Board(50, 30, 60)
running = True
MOUSEBUTTONDOWN = False
MOUSEMOTION = False
K_MOVE = 2
x, y = 0, 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MOUSEBUTTONDOWN = True
            x, y = event.pos
            if event.button == 1:
                board.button_pressed(*event.pos)
            elif event.button == 4:
                board.zoom(1)
            elif event.button == 5:
                board.zoom(-1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            MOUSEBUTTONDOWN = False
            MOUSEMOTION = False
        elif event.type == pygame.MOUSEMOTION and MOUSEBUTTONDOWN:
            dop_x, dop_y = event.pos[0] - x, event.pos[1] - y
            x, y = event.pos
            board.move(dop_x / K_MOVE, dop_y / K_MOVE)
            MOUSEMOTION = True
    clock.tick(fps)
    screen.fill((0, 0, 0))
    board.screen2.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
pygame.quit()
