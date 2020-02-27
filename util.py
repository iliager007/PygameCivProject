import pygame
from win32api import GetSystemMetrics


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
        self.rect = [-600, -600, (count_cells_y + 3) * cell_size + 2200, (count_cells_x + 6) * cell_size + 2200]
        self.screen2 = pygame.Surface(((count_cells_y + 3) * cell_size + 2200, (count_cells_x - 6) * cell_size + 5200))
        self.x = -600
        self.y = -600
        self.active_cell = (0, 0)
        self.initBoard()

    def get_size(self):
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
        self.screen2.fill(pygame.Color('White'))
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

    def get_count_cells_x(self):
        """Возвращает количество клеток по ширине"""
        return self.count_x

    def get_count_cells_y(self):
        """Возвращает количество клеток по высоте"""
        return self.count_y

    def get_cell(self, x, y):
        """Возвращает клетку с координатами x, y"""
        return self.board[x][y]

    def get_coords(self):
        """Возращает текущие координаты левого верзнего угла второго экрана"""
        return self.x, self.y


class Cell:
    """Класс игровой клетки"""

    def __init__(self, coords: list, cell_size, board, x, y):
        """Создаем клетку и задаем её координаты"""
        self.color = pygame.Color('Black')
        self.coords = coords
        self.cell_size = cell_size
        self.color = pygame.Color('White')
        self.type = 'Nothing'
        self.sustenance = 0
        self.board = board
        self.x = x
        self.y = y

    def render(self):
        """Основная функция отрисовки"""
        pygame.draw.polygon(self.board.screen2, pygame.Color('black'), self.coords, 4)
        pygame.draw.polygon(self.board.screen2, self.color, self.coords)

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
        self.type = type
        if type == 'Forest':
            self.color = pygame.Color('#013220')
            hsv = self.color.hsva
            self.color.hsva = (hsv[0] + 10, hsv[1], hsv[2], hsv[3])
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
            self.cell_size *= 1.03
        if type == -1:
            for i in range(len(self.coords)):
                self.coords[i] = [(self.coords[i][0] + 32) / 1.05, (self.coords[i][1] + 18) / 1.05]
            self.cell_size /= 1.03

    def get_coords(self):
        """Возвращает координаты клетки"""
        return self.coords


pygame.init()
MONITOR_width = GetSystemMetrics(0)
MONITOR_height = GetSystemMetrics(1)
size = (MONITOR_width, MONITOR_height)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill(pygame.Color('White'))
fps = 60
clock = pygame.time.Clock()
board = Board(60, 30, 60, MONITOR_width, MONITOR_height)
running = True
MOUSEMOTION = False
MOUSE_BUTTON_PRESSED = False
K_MOVE = 2
x, y = 0, 0
i = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MOUSE_BUTTON_PRESSED = True
            x, y = event.pos
            if event.button == 4:
                board.zoom(1)
            elif event.button == 5:
                board.zoom(-1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_1:
                pass
            elif event.key == pygame.K_2:
                pass
            elif event.key == pygame.K_f:
                pass
            elif event.key == pygame.K_3:
                pass
            elif event.key == pygame.K_a:
                pass
            elif event.key == pygame.K_h:
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            MOUSE_BUTTON_PRESSED = False
            MOUSEMOTION = False
        elif event.type == pygame.MOUSEMOTION and MOUSE_BUTTON_PRESSED:
            dop_x, dop_y = event.pos[0] - x, event.pos[1] - y
            x, y = event.pos
            board.move(dop_x / K_MOVE, dop_y / K_MOVE)
            MOUSEMOTION = True
    clock.tick(fps)
    screen.fill(pygame.Color('White'))
    board.render(screen)
    pygame.display.flip()
pygame.quit()
