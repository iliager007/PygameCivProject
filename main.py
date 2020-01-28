import pygame
from win32api import GetSystemMetrics
from cell import Board

pygame.init()
MONITOR_width = GetSystemMetrics(0)
MONITOR_height = GetSystemMetrics(1)
size = (MONITOR_width, MONITOR_height)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill((0, 0, 0))
fps = 60
clock = pygame.time.Clock()
board = Board(60, 30, 60, MONITOR_width, MONITOR_height)
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
    board.render(screen)
    pygame.display.flip()
pygame.quit()