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
country = Country('Россия')
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
                board.init_town(-1, -1)
            elif event.key == pygame.K_1:
                board.init_settlers()
            elif event.key == pygame.K_2:
                board.init_builders()
            elif event.key == pygame.K_f:
                board.init_ferma()
            elif event.key == pygame.K_3:
                board.init_warriors()
            elif event.key == pygame.K_a:
                board.activate_battle_mode()
            elif event.key == pygame.K_RETURN:
                board.next_move()
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
    country.render(screen, MONITOR_width, MONITOR_height)
    pygame.display.flip()
pygame.quit()
