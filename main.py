import pygame
from win32api import GetSystemMetrics
from cell import Board
from town import Country
from units import Settlers

pygame.init()
MONITOR_width = GetSystemMetrics(0)
MONITOR_height = GetSystemMetrics(1)
size = (MONITOR_width, MONITOR_height)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill((128, 128, 128))
fps = 60
clock = pygame.time.Clock()
board = Board(60, 30, 60, MONITOR_width, MONITOR_height)
running = True
MOUSEMOTION = False
MOUSE_BUTTON_PRESSED = False
K_MOVE = 2
x, y = 0, 0
countries = [Country('Россия', board), Country('Япония', board)]
i = 0
board.active_country = countries[i]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
            elif event.key == pygame.K_SPACE:
                board.init_town(-1, -1, countries[i])
            elif event.key == pygame.K_1:
                board.init_settlers(countries[i])
            elif event.key == pygame.K_2:
                board.init_builders()
            elif event.key == pygame.K_f:
                board.init_ferma(countries[i])
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
