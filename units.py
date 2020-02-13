from copy import deepcopy
import os
import pygame


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


class Settlers:
    """Класс Поселенцы"""

    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
        self.t_level = 0
        self.country = '1'
        self.t_moving = []
        self.max_move = 1
        self.count_move = 0
        self.moveble = False
        self.image = load_image('переселенцы.png', -1)

    def move(self, x, y):
        if self.moveble:
            return
        self.count_move = 0
        dop = self.check_can_move(x, y)
        if dop is False:
            return
        self.t_moving = deepcopy(dop)
        self.next_move()

    def next_move(self):
        if self.moveble:
            return
        if len(self.t_moving) == 0:
            return
        self.count_move += 1
        dop_x, dop_y = self.x, self.y
        for i in self.t_moving[:3]:
            if i == 'down':
                self.x += 1
            elif i == 'up':
                self.x -= 1
            elif i == 'right':
                self.y += 1
            elif i == 'left':
                self.y -= 1
        self.t_moving = self.t_moving[3:]
        self.board.change_cell(self.x, self.y, dop_x, dop_y)
        self.moveble = True

    def check_can_move(self, x, y):
        """Проверка можно ли перейти в нужную клетку"""
        board = self.board.get_board()
        if self.t_level >= 2:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    board[i][j] = 0
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == 0:
                        board[i][j] = -1
                    else:
                        board[i][j] = 0
        board[self.x][self.y] = 1
        if not self.found_path(board, (x, y)):
            return False
        result = self.return_path(board, (x, y))
        return result

    def found_path(self, pathArr, finPoint):
        weight = 1
        for i in range(len(pathArr) * len(pathArr[0])):
            weight += 1
            for y in range(len(pathArr)):
                for x in range(len(pathArr[y])):
                    if pathArr[y][x] == (weight - 1):
                        if y > 0 and pathArr[y - 1][x] == 0:
                            pathArr[y - 1][x] = weight
                        if y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0:
                            pathArr[y + 1][x] = weight
                        if x > 0 and pathArr[y][x - 1] == 0:
                            pathArr[y][x - 1] = weight
                        if x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == 0:
                            pathArr[y][x + 1] = weight
                        if (abs(y - finPoint[0]) + abs(x - finPoint[1])) == 1:
                            pathArr[finPoint[0]][finPoint[1]] = weight
                            return True
        return False

    def return_path(self, pathArr, finPoint):
        y = finPoint[0]
        x = finPoint[1]
        weight = pathArr[y][x]
        result = list(range(weight))
        while weight:
            weight -= 1
            if y > 0 and pathArr[y - 1][x] == weight:
                y -= 1
                result[weight] = 'down'
            elif y < (len(pathArr) - 1) and pathArr[y + 1][x] == weight:
                result[weight] = 'up'
                y += 1
            elif x > 0 and pathArr[y][x - 1] == weight:
                result[weight] = 'right'
                x -= 1
            elif x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == weight:
                result[weight] = 'left'
                x += 1
        return result[1:]

    def render(self, coords, cell_size, screen):
        dop = pygame.transform.scale(self.image, (int(cell_size - 15), int(cell_size - 15)))
        screen.blit(dop, ((coords[0][0] + coords[5][0]) // 2 - 8, (coords[0][1] + coords[5][1]) // 2 - 3))

    def who(self):
        return 'Settlers'

    def __str__(self):
        return 'Settlers'

    def update(self):
        self.moveble = False

    def upgrade(self):
        self.max_move += 1


class Builders:

    def __init__(self, x, y, town, board):
        self.x = x
        self.y = y
        self.town = town
        self.moveble = False
        self.board = board
        self.country = '1'
        self.t_level = 0
        self.t_moving = []
        self.max_move = 1
        self.count_move = 0
        self.image = load_image('строители.png', -1)

    def move(self, x, y):
        if self.moveble:
            return
        self.count_move = 0
        dop = self.check_can_move(x, y)
        if dop is False:
            return
        self.t_moving = deepcopy(dop)
        self.next_move()

    def next_move(self):
        if len(self.t_moving) == 0:
            return
        self.count_move += 1
        dop_x, dop_y = self.x, self.y
        for i in self.t_moving[:3]:
            if i == 'down':
                self.x += 1
            elif i == 'up':
                self.x -= 1
            elif i == 'right':
                self.y += 1
            elif i == 'left':
                self.y -= 1
        self.t_moving = self.t_moving[3:]
        self.board.change_cell(self.x, self.y, dop_x, dop_y)
        self.moveble = True

    def check_can_move(self, x, y):
        """Проверка можно ли перейти в нужную клетку"""
        board = self.board.get_board()
        if self.t_level >= 2:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    board[i][j] = 0
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == 0:
                        board[i][j] = -1
                    else:
                        board[i][j] = 0
        board[self.x][self.y] = 1
        if not self.found_path(board, (x, y)):
            return False
        result = self.return_path(board, (x, y))
        return result

    def found_path(self, pathArr, finPoint):
        weight = 1
        for i in range(len(pathArr) * len(pathArr[0])):
            weight += 1
            for y in range(len(pathArr)):
                for x in range(len(pathArr[y])):
                    if pathArr[y][x] == (weight - 1):
                        if y > 0 and pathArr[y - 1][x] == 0:
                            pathArr[y - 1][x] = weight
                        if y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0:
                            pathArr[y + 1][x] = weight
                        if x > 0 and pathArr[y][x - 1] == 0:
                            pathArr[y][x - 1] = weight
                        if x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == 0:
                            pathArr[y][x + 1] = weight
                        if (abs(y - finPoint[0]) + abs(x - finPoint[1])) == 1:
                            pathArr[finPoint[0]][finPoint[1]] = weight
                            return True
        return False

    def return_path(self, pathArr, finPoint):
        y = finPoint[0]
        x = finPoint[1]
        weight = pathArr[y][x]
        result = list(range(weight))
        while weight:
            weight -= 1
            if y > 0 and pathArr[y - 1][x] == weight:
                y -= 1
                result[weight] = 'down'
            elif y < (len(pathArr) - 1) and pathArr[y + 1][x] == weight:
                result[weight] = 'up'
                y += 1
            elif x > 0 and pathArr[y][x - 1] == weight:
                result[weight] = 'right'
                x -= 1
            elif x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == weight:
                result[weight] = 'left'
                x += 1
        return result[1:]

    def render(self, coords, cell_size, screen):
        dop = pygame.transform.scale(self.image, (int(cell_size - 15), int(cell_size - 15)))
        screen.blit(dop, ((coords[0][0] + coords[5][0]) // 2 - 8, (coords[0][1] + coords[5][1]) // 2 - 3))

    def who(self):
        return 'Builders'

    def __str__(self):
        return 'Builders'

    def get_town(self):
        return self.town

    def update(self):
        self.moveble = False

    def upgrade(self):
        self.max_move += 1


class Warriors:

    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.moveble = False
        self.board = board
        self.health = 20
        self.max_health = 20
        self.country = '1'
        self.damage = 10
        self.t_level = 0
        self.t_moving = []
        self.max_move = 1
        self.count_move = 0
        self.image = load_image('воин.png', -1)

    def move(self, x, y):
        if self.moveble:
            return
        self.count_move = 0
        dop = self.check_can_move(x, y)
        if dop is False:
            return
        self.t_moving = deepcopy(dop)
        self.next_move()

    def next_move(self):
        if len(self.t_moving) == 0:
            return
        self.count_move += 1
        dop_x, dop_y = self.x, self.y
        for i in self.t_moving[:3]:
            if i == 'down':
                self.x += 1
            elif i == 'up':
                self.x -= 1
            elif i == 'right':
                self.y += 1
            elif i == 'left':
                self.y -= 1
        self.t_moving = self.t_moving[3:]
        self.board.change_cell(self.x, self.y, dop_x, dop_y)
        self.moveble = True

    def check_can_move(self, x, y):
        """Проверка можно ли перейти в нужную клетку"""
        board = self.board.get_board()
        if self.t_level >= 2:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    board[i][j] = 0
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == 0:
                        board[i][j] = -1
                    else:
                        board[i][j] = 0
        board[self.x][self.y] = 1
        if not self.found_path(board, (x, y)):
            return False
        result = self.return_path(board, (x, y))
        return result

    def found_path(self, pathArr, finPoint):
        weight = 1
        for i in range(len(pathArr) * len(pathArr[0])):
            weight += 1
            for y in range(len(pathArr)):
                for x in range(len(pathArr[y])):
                    if pathArr[y][x] == (weight - 1):
                        if y > 0 and pathArr[y - 1][x] == 0:
                            pathArr[y - 1][x] = weight
                        if y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0:
                            pathArr[y + 1][x] = weight
                        if x > 0 and pathArr[y][x - 1] == 0:
                            pathArr[y][x - 1] = weight
                        if x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == 0:
                            pathArr[y][x + 1] = weight
                        if (abs(y - finPoint[0]) + abs(x - finPoint[1])) == 1:
                            pathArr[finPoint[0]][finPoint[1]] = weight
                            return True
        return False

    def return_path(self, pathArr, finPoint):
        y = finPoint[0]
        x = finPoint[1]
        weight = pathArr[y][x]
        result = list(range(weight))
        while weight:
            weight -= 1
            if y > 0 and pathArr[y - 1][x] == weight:
                y -= 1
                result[weight] = 'down'
            elif y < (len(pathArr) - 1) and pathArr[y + 1][x] == weight:
                result[weight] = 'up'
                y += 1
            elif x > 0 and pathArr[y][x - 1] == weight:
                result[weight] = 'right'
                x -= 1
            elif x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == weight:
                result[weight] = 'left'
                x += 1
        return result[1:]

    def render(self, coords, cell_size, screen):
        dop = pygame.transform.scale(self.image, (int(cell_size - 15), int(cell_size - 15)))
        screen.blit(dop, ((coords[0][0] + coords[5][0]) // 2 - 8, (coords[0][1] + coords[5][1]) // 2 - 3))

    def who(self):
        return 'Warriors'

    def __str__(self):
        return 'Warriors'

    def get_town(self):
        return self.town

    def update(self):
        self.moveble = False

    def heal(self):
        self.health += 5
        if self.health > self.max_health:
            self.health = self.max_health

    def upgrade(self):
        self.max_health += 10
        self.health = self.max_health
        self.damage += 5

    def get_distance(self, x, y):
        dop = self.check_can_move(x, y)
        if dop:
            return len(dop)

    def get_max_move(self):
        return self.max_move

    def take_damage(self):
        return self.damage

    def get_damage(self, damage):
        self.health -= damage
