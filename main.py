import pygame
from cell import Board
from town import Country
import sys
from PyQt5 import Qt


def get_size_of_desktop():
    desktop = Qt.QApplication(sys.argv).desktop()
    return desktop.width(), desktop.height()


def terminate():
    pygame.quit()
    sys.exit()


def rules_menu():
    intro_text = ["Для хода выделите юнит и нажмите на клетку в которую он должен идти",
                  "Важно, чтобы юнит принадлежал вашей стране",
                  "Для создания города: выделите поселенцев и нажмите пробел",
                  "Для создания юнита: выделите город и нажмите клавишу юнита",
                  "     Поселенец - 1",
                  "     Строитель - 2",
                  "     Воин - 3",
                  "Для строительства ферм выделите строителя и нажмите F",
                  "Для атаки вражеских юнитов: выделите своего воина и нажмите A, затем укажите щелчком вражеский юнит",
                  "Помните, что каждый созданный юнит тратит еду",
                  "Вы можете вылечить юнит, для этого выделите его и нажмите на H",
                  "Для завершения хода нажмите Enter",
                  "",
                  "",
                  "",
                  "Для выхода нажмите любую кнопку"]
    screen.fill((218, 112, 214))
    font = pygame.font.Font(None, 50)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def draw_start_menu():
    intro_text = ["Продолжить (1)", "",
                  "Правила игры (2)", "",
                  "Новая игра (3)"]
    screen.fill((218, 112, 214))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def start_menu():
    draw_start_menu()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_1:
                    return 'continue'
                elif event.key == pygame.K_2:
                    rules_menu()
                    draw_start_menu()
                    continue
        pygame.display.flip()
        clock.tick(fps)


def new_game():
    global x, y, size, board
    x, y, size = 60, 30, 60
    board = Board(x, y, size, MONITOR_width, MONITOR_height)


def load_game(info):
    if ',' in info[0]:
        countries_name = info[0].split(', ')
    else:
        countries_name = info[0]
    x, y = map(int, info[1])


def save_game():
    with open('data/maps/saves.txt', mode='w', encoding='utf-8') as file:
        file.write(', '.join(countries_name))
        file.write('\n')
        file.write(f'{board.get_size()[0]} {board.get_size()[1]}')
        file.write('\n')
        for i in range(board.get_size()[0]):
            for j in range(board.get_size()[1]):
                file.write(f'{i} {j} {board.get_cell(i, j).type}')
                file.write('\n')
        for i in range(board.get_size()[0]):
            for j in range(board.get_size()[1]):
                if board.get_cell(i, j).have_unit():
                    unit = board.get_cell(i, j).unit
                    file.write(f'{i} {j} {unit.who()} {unit.health} {unit.country.name}')
                elif board.get_cell(i, j).have_town():
                    pass


pygame.init()
MONITOR_width, MONITOR_height = get_size_of_desktop()
size = (MONITOR_width, MONITOR_height)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill((128, 128, 128))
fps = 60
clock = pygame.time.Clock()
# mode = start_menu()
# x, y, size = None, None, None
# board = None
# if mode == 'continue':
#     with open('data/maps/saves.txt', mode='r', encoding='utf-8') as file:
#         if file.read() == 'No saves':
#             new_game()
#         else:
#             load_game(file.readlines())
x, y, size = 60, 30, 60
board = Board(x, y, size, MONITOR_width, MONITOR_height)
running = True
MOUSEMOTION = False
MOUSE_BUTTON_PRESSED = False
K_MOVE = 2
x, y = 0, 0
countries = [Country('Россия', board), Country('Украина', board)]
countries_name = 'Россия', 'Украина'
i = 0
board.active_country = countries[i]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MOUSE_BUTTON_PRESSED = True
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
                save_game()
            elif event.key == pygame.K_SPACE:
                board.init_town(-1, -1, countries[i])
            elif event.key == pygame.K_1:
                board.init_settlers(countries[i])
            elif event.key == pygame.K_2:
                board.init_builders()
            elif event.key == pygame.K_f:
                board.init_farm(countries[i])
            elif event.key == pygame.K_3:
                board.init_warriors(countries[i])
            elif event.key == pygame.K_a:
                board.activate_battle_mode()
            elif event.key == pygame.K_h:
                board.heal()
            elif event.key == pygame.K_RETURN:
                i = (i + 1) % len(countries)
                board.next_move(countries[i])
        elif event.type == pygame.MOUSEBUTTONUP:
            MOUSE_BUTTON_PRESSED = False
            MOUSEMOTION = False
        elif event.type == pygame.MOUSEMOTION and MOUSE_BUTTON_PRESSED:
            dop_x, dop_y = event.pos[0] - x, event.pos[1] - y
            x, y = event.pos
            board.move(dop_x / K_MOVE, dop_y / K_MOVE)
            MOUSEMOTION = True
    clock.tick(fps)
    screen.fill((0, 0, 0))
    board.render(screen)
    countries[i].render(screen, MONITOR_width, MONITOR_height)
    pygame.display.flip()
pygame.quit()
