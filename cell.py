import pygame
from win32api import GetSystemMetrics


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
        self.initBoard()

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
                    self.board[i][j] = Cell(coords)
                else:
                    coords = [[1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 2 / 3 * x],
                              [x + j * x, 4 / 6 * (i - 1) * x + x],
                              [x + j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x],
                              [1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 5 / 3 * x],
                              [j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x],
                              [j * x, 4 / 6 * (i - 1) * x + x]]
                    self.board[i][j] = Cell(coords)

    def render(self):
        """Основная функция отрисовки поля"""
        for i in self.board:
            for j in i:
                j.render()

    def button_pressed(self, x: int, y: int):
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
        for i in self.board:
            for j in i:
                j += (x, y)


class Cell:

    def __init__(self, coords: list):
        """Создаем клетку и задаем её координаты"""
        self.coords = coords

    def render(self):
        """Основная функция отрисовки"""
        pygame.draw.polygon(screen, pygame.Color('white'), self.coords, 1)

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

    def __add__(self, other):
        x, y = other[0], other[1]
        self.coords[0][0] += x
        self.coords[0][1] += y
        self.coords[1][0] += x
        self.coords[1][1] += y
        self.coords[2][0] += x
        self.coords[2][1] += y
        self.coords[3][0] += x
        self.coords[3][1] += y
        self.coords[4][0] += x
        self.coords[4][1] += y
        self.coords[5][0] += x
        self.coords[5][1] += y


pygame.init()
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
size = (width, height)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
fps = 60
clock = pygame.time.Clock()
board = Board(150, 150, 60)
running = True
MOUSEBUTTONDOWN = False
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
            if event.key == pygame.K_F11:
                screen.set_mode(size, pygame.FULLSCREEN)
        elif event.type == pygame.MOUSEBUTTONUP:
            MOUSEBUTTONDOWN = False
        elif event.type == pygame.MOUSEMOTION and MOUSEBUTTONDOWN:
            dop_x, dop_y = event.pos[0] - x, event.pos[1] - y
            x, y = event.pos
            board.move(dop_x / K_MOVE, dop_y / K_MOVE)
    clock.tick(fps)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
pygame.quit()
