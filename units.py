from copy import deepcopy


class Settlers:
    """Класс Поселенцы"""
    def __init__(self, x, y, town, board):
        self.x = x
        self.y = y
        self.town = town
        self.board = board
        self.t_level = 0
        self.t_moving = []
        self.max_move = 3

    def move(self, x, y):
        if len(self.t_moving) == 0:
            dop = self.check_can_move(x, y)
            if dop is False:
                return
            self.t_moving = deepcopy(dop)
        for i in self.t_moving[:self.max_move]:
            if i == 'down':
                self.y += 1
            elif i == 'up':
                self.y -= 1
            elif i == 'right':
                self.x += 1
            elif i == 'left':
                self.x -= 1
        self.t_moving = self.t_moving[self.max_move:]

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
