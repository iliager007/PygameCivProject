import pygame


class Cells:
    def __init__(self, height, width, size_cell):
        self.height = height
        self.width = width
        self.size_cell = size_cell
        self.cells = [[[] for _ in range(width)] for __ in range(height)]

    def draw(self):
        x = self.size_cell
        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 0:
                    self.cells[i][j] = ((x + j * x, 4 / 6 * i * x), (3 / 2 * x + j * x, 4 / 6 * i * x + 1 / 3 * x),
                                        (3 / 2 * x + j * x, 4 / 6 * i * x + 2 / 3 * x), (x + j * x, 4 / 6 * i * x + x),
                                        (1 / 2 * x + j * x, 4 / 6 * i * x + 2 / 3 * x),
                                        (1 / 2 * x + j * x, 4 / 6 * i * x + 1 / 3 * x))
                    pygame.draw.polygon(screen, pygame.Color('white'), self.cells[i][j], 5)
                else:
                    self.cells[i][j] = (
                        (1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 2 / 3 * x), (x + j * x, 4 / 6 * (i - 1) * x + x),
                        (x + j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x),
                        (1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 5 / 3 * x),
                        (j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x), (j * x, 4 / 6 * (i - 1) * x + x))
                    pygame.draw.polygon(screen, pygame.Color('green'), self.cells[i][j], 5)

    def what_cell(self, x, y):
        for i in range(self.height):
            for j in range(self.width):
                coords = self.cells[i][j]
                fl = True
                for v in range(-1, 1):
                    x1, y1, x2, y2 = coords[(v + 6) % 6][0], coords[(v + 6) % 6][1], coords[(v + 7) % 6][0], \
                                     coords[(v + 7) % 6][1]
                    if y < (x - x1) * (y2 - y1) / (x2 - x1) + y1:
                        fl = False
                for v in range(2, 4):
                    x1, y1, x2, y2 = coords[v][0], coords[v][1], coords[v][0], \
                                     coords[v][1]
                    if y > (x - x1) * (y2 - y1) / (x2 - x1) + y1:
                        fl = False
                if x < coords[4][0] or x > coords[2][0]:
                    fl = False
                if fl:
                    return i, j


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
        print(*self.board, sep='\n')
        print(len(self.board[0]))
        self.initBoard()

    def initBoard(self):
        """Заполняем игровую площадь клетками Cell"""
        x = self.cell_size
        for i in range(self.count_x):
            for j in range(self.count_y):
                if i % 2 == 0:
                    coords = ((x + j * x, 4 / 6 * i * x),
                              (3 / 2 * x + j * x, 4 / 6 * i * x + 1 / 3 * x),
                              (3 / 2 * x + j * x, 4 / 6 * i * x + 2 / 3 * x),
                              (x + j * x, 4 / 6 * i * x + x),
                              (1 / 2 * x + j * x, 4 / 6 * i * x + 2 / 3 * x),
                              (1 / 2 * x + j * x, 4 / 6 * i * x + 1 / 3 * x))
                    self.board[i][j] = Cell(coords)
                else:
                    coords = ((1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 2 / 3 * x),
                              (x + j * x, 4 / 6 * (i - 1) * x + x),
                              (x + j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x),
                              (1 / 2 * x + j * x, 4 / 6 * (i - 1) * x + 5 / 3 * x),
                              (j * x, 4 / 6 * (i - 1) * x + 4 / 3 * x),
                              (j * x, 4 / 6 * (i - 1) * x + x))
                    self.board[i][j] = Cell(coords)

    def render(self):
        """Основная функция отрисовки поля"""
        for i in self.board:
            for j in i:
                j.render()

    def button_pressed(self, x, y):
        for i in range(self.count_x):
            for j in range(self.count_y):
                if self.board[i][j].check_is_pressed(x, y):
                    print(i, j)


class Cell:

    def __init__(self, coords):
        """Создаем клетку и задаем её координаты"""
        self.coords = coords

    def render(self):
        """Основная функция отрисовки"""
        pygame.draw.polygon(screen, pygame.Color('white'), self.coords, 1)

    def check_is_pressed(self, x, y) -> bool:
        """Проверяем была ли нажата именно эта клетка"""
        pass


pygame.init()
size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)
fps = 60
clock = pygame.time.Clock()
board = Board(10, 15, 60)
while pygame.event.wait().type != pygame.QUIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.button_pressed(*event.pos)
    clock.tick(fps)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
pygame.quit()
