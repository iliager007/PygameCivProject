import pygame
import sys
import os
import tkinter


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


def terminate():
    """Завершает работы"""
    pygame.quit()
    sys.exit()


def button_pressed(event):
    try:
        return event.unicode
    except TypeError:
        return False


def get_size_of_desktop():
    """Возращает размеры монитора"""
    r = tkinter.Tk()
    return r.winfo_screenwidth(), r.winfo_screenheight()


