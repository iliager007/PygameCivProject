import pygame
from cell import Board
from town import Country
import sys
import tkinter
import os
from copy import deepcopy
from functions import *


def rules_menu():
    intro_text = []
    with open('data/rules/rules_menu.txt', 'r', encoding='utf-8') as file:
        dop = file.readlines()
        for i in dop:
            intro_text.append(i[:-1])
    screen.fill(pygame.Color('#98FB98'))
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


def rules_new_game():
    intro_text = []
    with open('data/rules/rules_new_game.txt', 'r', encoding='utf-8') as file:
        dop = file.readlines()
        for i in dop:
            intro_text.append(i[:-1])
    screen.fill(pygame.Color('#98FB98'))
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


def draw_start_menu(active_line):
    intro_text = ["Продолжить (1)",
                  "Новая игра (2)",
                  "Правила игры (3)"]
    fon = pygame.transform.scale(load_image('civilization.png'), (MONITOR_width, MONITOR_height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for i, line in enumerate(intro_text):
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += 70
        text_coord += intro_rect.height
        if i == active_line and line != "":
            pygame.draw.rect(screen, pygame.Color(130, 137, 143),
                             (intro_rect.x - 10, intro_rect.y - 10, intro_rect.w + 20, intro_rect.h + 20))
        screen.blit(string_rendered, intro_rect)


def start_menu():
    index = 0
    draw_start_menu(index)
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
                elif event.key == pygame.K_3:
                    rules_menu()
                    draw_start_menu(index)
                elif event.key == pygame.K_2:
                    dop = new_game()
                    draw_start_menu(index)
                elif event.key == pygame.K_DOWN:
                    index = (index + 1) % 3
                    draw_start_menu(index)
                elif event.key == pygame.K_UP:
                    index = (index - 1) % 3
                    draw_start_menu(index)
                elif event.key == pygame.K_RETURN:
                    if index == 0:
                        return 'continue'
                    elif index == 1:
                        return 'new'
                    elif index == 2:
                        rules_menu()
                        draw_start_menu(index)
        pygame.display.flip()
        clock.tick(fps)


def load_game(info):
    global countries_name, x, y, board, countries
    dop = []
    for i in info:
        dop.append(i.replace('\n', ''))
    info = deepcopy(dop)
    countries_name = info[0].split()
    y, x = map(int, info[1].split())
    board = Board(x, y, MONITOR_width, MONITOR_height, generate_field=False)
    for i in range(y):
        for j in range(x):
            board.set_cell(i, j, info[x * i + j + 2].split()[-1])
    del info[:2 + x * y]
    i = 0
    while info[i] != 'end':
        if info[i].split()[0] in countries_name:
            food, t_food = info[i + 1].split()
            countries.append(Country(info[i], board, pr='SAVE', food=int(food), t_food=int(t_food)))
        else:
            unit = info[i].split()[0]
            if unit == 'Settlers':
                unit, x, y, live = info[i].split()
                if int(live):
                    board.init_settlers(countries[-1], int(x), int(y), 'SAVE')
            elif unit == 'Builders':
                unit, x, y, live = info[i].split()
                if int(live):
                    board.init_builders(int(x), int(y), countries[-1])
            elif unit == 'Warriors':
                unit, x, y, health = info[i].split()
                if int(health) > 0:
                    board.init_warriors(countries[-1], int(x), int(y), health)
            elif unit == 'Town':
                unit, x, y = info[i].split()
                board.init_town(int(x), int(y), countries[-1])
            elif unit == 'Farm':
                unit, x, y = info[i].split()
                board.init_farm(countries[-1], pr='SAVE', x=int(x), y=int(y))
        i += 1


def save_game():
    countries_name = []
    for country in countries:
        countries_name.append(country.name.replace('\n', ''))
    with open('data/maps/saves.txt', mode='w', encoding='utf-8') as file:
        file.write(' '.join(countries_name))
        file.write('\n')
        file.write(f'{board.get_size()[0]} {board.get_size()[1]}')
        file.write('\n')
        for i in range(board.get_count_cells_x()):
            for j in range(board.get_count_cells_y()):
                file.write(f'{i} {j} {board.get_cell(i, j).type}')
                file.write('\n')
        for country in countries:
            file.write(str(country.name) + '\n')
            file.write(' '.join([str(country.food), str(country.t_food)]) + '\n')
            for unit in country.units_towns:
                name = str(unit)
                if 'farm' in name:
                    file.write(name + '\n')
                elif 'Settlers' in name:
                    file.write(name + ' ' + str(unit.x) + ' ' + str(unit.y) + ' ' + str(unit.live))
                    file.write('\n')
                elif 'Builders' in name:
                    file.write(name + ' ' + str(unit.x) + ' ' + str(unit.y) + ' ' + str(unit.live))
                    file.write('\n')
                elif 'Warriors' in name:
                    file.write(name + ' ' + str(unit.x) + ' ' + str(unit.y) + ' ' + str(unit.health))
                    file.write('\n')
                elif 'Town' in name:
                    file.write(name + ' ' + str(unit.x) + ' ' + str(unit.y))
                    file.write('\n')
                elif 'Farm' in name:
                    file.write(name)
                    file.write('\n')
        file.write('end')


def draw_new_game_menu(active_line, x, y, x_warning=False, y_warning=False):
    intro_text = ["Введите размеры поля",
                  f"X: {x}", f"Y: {y}",
                  "Выберите страны",
                  "Ознакомиться с инструкцией",
                  "Начать игру"]
    screen.fill(pygame.Color('#98FB98'))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for i, line in enumerate(intro_text):
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += 70
        text_coord += intro_rect.height
        if i == active_line and line != "":
            pygame.draw.rect(screen, pygame.Color(130, 137, 143),
                             (intro_rect.x - 10, intro_rect.y - 10, intro_rect.w + 20, intro_rect.h + 20))
        screen.blit(string_rendered, intro_rect)
        if "X" in line and x_warning:
            x_coord = intro_rect.w + intro_rect.x + 20
            string_warning = font.render(x_warning, 1, pygame.Color('red'))
            intro_rect = string_warning.get_rect()
            text_coord -= 120
            intro_rect.top = text_coord
            intro_rect.x = x_coord
            text_coord += intro_rect.height
            screen.blit(string_warning, intro_rect)
            text_coord += 70
        elif "Y" in line and y_warning:
            y_coord = intro_rect.w + intro_rect.x + 20
            string_warning = font.render(x_warning, 1, pygame.Color('red'))
            intro_rect = string_warning.get_rect()
            text_coord -= 120
            intro_rect.top = text_coord
            intro_rect.x = y_coord
            text_coord += intro_rect.height
            screen.blit(string_warning, intro_rect)
            text_coord += 70


def draw_countries_menu(info, active_line, text_coord, ok, no):
    font = pygame.font.Font(None, 70)
    screen.fill(pygame.Color('#98FB98'))
    for i, line in enumerate(info[:-1]):
        string_rendered = font.render(line.split()[0], 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 50
        if i == active_line and line != "":
            pygame.draw.rect(screen, pygame.Color(130, 137, 143),
                             (intro_rect.x - 10, intro_rect.y - 10, intro_rect.w + 20, intro_rect.h + 20))
        screen.blit(string_rendered, intro_rect)
        pygame.draw.rect(screen, pygame.Color(line.split()[1]),
                         (intro_rect.x + intro_rect.w + 20, intro_rect.y, intro_rect.h, intro_rect.h))
        text_coord += 70
        text_coord += intro_rect.height
        if line.split()[-1] == 'no':
            no = pygame.transform.scale(no, (intro_rect.h, intro_rect.h))
            screen.blit(no, (intro_rect.x + intro_rect.w + intro_rect.h + 40, intro_rect.y,
                             intro_rect.h, intro_rect.w))
        elif line.split()[-1] == 'yes':
            ok = pygame.transform.scale(ok, (intro_rect.h, intro_rect.h))
            screen.blit(ok, (intro_rect.x + intro_rect.w + intro_rect.h + 40, intro_rect.y,
                             intro_rect.h, intro_rect.w))


def countries_menu():
    info = []
    ok = load_image('ok.png', -1)
    no = load_image('no.png', -1)
    with open('data/buildings/colors.txt', 'r', encoding='utf-8') as file:
        for i in file.readlines():
            info.append(i[:-1] + ' no')
    text_coord = 50
    draw_countries_menu(info, 0, text_coord, ok, no)
    index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    index = (index + 1) % len(info)
                elif event.key == pygame.K_UP:
                    index = (index - 1) % len(info)
                elif event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RETURN:
                    info[index] += ' yes'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    text_coord -= 20
                    if text_coord <= -1420:
                        text_coord += 20
                elif event.button == 4:
                    text_coord += 20
                    if text_coord >= 70:
                        text_coord -= 20
        draw_countries_menu(info, index, text_coord, ok, no)
        pygame.display.flip()
        clock.tick(fps)


def new_game():
    global x, y, size, board, countries, i
    x, y, size = 0, 0, 0
    index = 0
    draw_new_game_menu(0, x, y)
    run = True
    x_warning, y_warning = False, False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_menu()
                elif event.key == pygame.K_DOWN:
                    index = (index + 1) % 6
                elif event.key == pygame.K_UP:
                    index = (index - 1) % 6
                elif event.key == pygame.K_RETURN:
                    if index == 1:
                        if x > 400 or x <= 4:
                            x_warning = 'Недопустимое значение X. Диапозон от 5 до 400'
                        else:
                            x_warning = 'Ок'
                    elif index == 2:
                        if y > 400 or y <= 4:
                            y_warning = 'Недопустимое значение Y. Диапозон от 5 до 400'
                        else:
                            y_warning = 'Ок'
                    elif index == 3:
                        countries_menu()
                    elif index == 4:
                        rules_new_game()
                        draw_new_game_menu(index, x, y)
                else:
                    char = button_pressed(event)
                    if char:
                        if char.isdigit():
                            if index == 1:
                                x *= 10
                                x += int(char)
                            elif index == 2:
                                y *= 10
                                y += int(char)
        draw_new_game_menu(index, x, y, x_warning, y_warning)
        pygame.display.flip()
        clock.tick(fps)


pygame.init()
MONITOR_width, MONITOR_height = get_size_of_desktop()
size = (MONITOR_width, MONITOR_height)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill((128, 128, 128))
fps = 60
clock = pygame.time.Clock()
mode = start_menu()
x, y, size = None, None, None
board = None
countries = []
if mode == 'continue':
    with open('data/maps/saves.txt', encoding='utf-8') as file:
        info = file.readlines()
        if 'No saves' in info[0]:
            new_game()
        else:
            load_game(info)
elif mode == 'new':
    new_game()
running = True
MOUSEMOTION = False
MOUSE_BUTTON_PRESSED = False
K_MOVE = 2
x, y = 0, 0
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
                countries[i].next_move()
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
