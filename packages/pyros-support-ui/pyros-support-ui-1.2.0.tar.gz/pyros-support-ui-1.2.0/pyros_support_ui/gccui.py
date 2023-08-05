################################################################################
# Copyright (C) 2020 Abstract Horizon
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License v2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#    Daniel Sendula - initial API and implementation
#
#################################################################################

import pygame
import os
import time

BLACK = (0, 0, 0)
DARK_GREY = (80, 80, 80)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
LIGHT_BLUE = (160, 255, 255)
GREEN = (128, 255, 128)
RED = (255, 128, 128)
YELLOW = (255, 255, 128)
BLUE = (128, 128, 255)

smallFont = None
font = None
big_font = None

frameclock = pygame.time.Clock()
screen = None
backgroundImage = None
scaledBackground = None
gccFullImage = None
gccGreenImage = None
gccColouredImage = None

SCREEN_RECT = None


def _this_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def init_all(screen_size, load_background=False, title="GCC"):
    global screen, backgroundImage, scaledBackground
    global smallFont, font, big_font
    global SCREEN_RECT
    global gccFullImage, gccGreenImage, gccColouredImage

    pygame.init()

    font_file = _this_path("garuda.ttf")
    big_font = pygame.font.Font(font_file, 20)
    font = pygame.font.Font(font_file, 16)
    smallFont = pygame.font.Font(font_file, 12)

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(title)

    SCREEN_RECT = pygame.Rect(0, 0, screen.get_width(), screen.get_height())

    if load_background:
        backgroundImage = pygame.image.load(_this_path("blue-background.png"))
        scaledBackground = pygame.transform.scale(backgroundImage, screen.get_size())

    gccFullImage = pygame.image.load(_this_path("GCC_full.png"))
    gccGreenImage = pygame.image.load(_this_path("GCC_green_small.png"))
    gccColouredImage = pygame.image.load(_this_path("GCC_coloured_small.png"))

    return screen


def screen_resized(size):
    global scaledBackground

    scaledBackground = pygame.transform.scale(backgroundImage, size)


def background(top_frame=False):
    if scaledBackground is not None:
        screen.blit(scaledBackground, (0, 0))
    else:
        screen.fill((0, 0, 0))

    if top_frame:
        draw_top_frame()


def frame_end():
    pygame.display.flip()
    frameclock.tick(30)


def draw_key_value(key, value, x, y, colour=WHITE):
    screen.blit(font.render(key + ":", 1, colour), (x, y))
    screen.blit(font.render(value, 1, colour), (x + 100, y))
    return y + 20  # font.get_height()


def draw_big_text(text, pos, colour=WHITE):
    screen.blit(big_font.render(text, 1, colour), pos)


def draw_text(text, pos, colour=WHITE):
    screen.blit(font.render(text, 1, colour), pos)


def draw_small_text(text, pos, colour=WHITE):
    screen.blit(smallFont.render(text, 1, colour), pos)


def draw_rect(pos, size, colour=LIGHT_BLUE, stick=0, outside=1):

    pygame.draw.line(screen, colour, (pos[0] - stick, pos[1] - outside), (pos[0] + size[0] + stick, pos[1] - outside))
    pygame.draw.line(screen, colour, (pos[0] - stick, pos[1] + size[1] + outside), (pos[0] + size[0] + stick, pos[1] + size[1] + outside))

    pygame.draw.line(screen, colour, (pos[0] - outside, pos[1] - stick), (pos[0] - outside, pos[1] + size[1] + stick))
    pygame.draw.line(screen, colour, (pos[0] + size[0] + outside, pos[1] - stick), (pos[0] + size[0] + outside, pos[1] + size[1] + stick))


def draw_frame(rect, colour=LIGHT_BLUE, background_colour=BLACK):
    if background_colour is not None:
        pygame.draw.rect(screen, background_colour, rect, 0)
    pygame.draw.rect(screen, colour, (rect[0] + 4, rect[1] + 4, rect[2] - 8, rect[3] - 8), 1)
    for i in range(6, 12):
        pygame.draw.line(screen, colour, (rect[0] + rect[2] - i, rect[1] + rect[3] - 6), (rect[0] + rect[2] - 6, rect[1] + rect[3] - i), 1)


def draw_top_frame(colour=LIGHT_BLUE):
    screen_rect = SCREEN_RECT

    if int(time.time()) % 20 < 10:
        screen.blit(gccGreenImage, (screen_rect[0] + screen_rect[2] - 8 - gccGreenImage.get_width(), screen_rect[1] + 8))
    else:
        screen.blit(gccColouredImage, (screen_rect[0] + screen_rect[2] - 8 - gccGreenImage.get_width(), screen_rect[1] + 8))

    pygame.draw.line(screen, colour, (screen_rect[0] + 4, screen_rect[1] + 4), (screen_rect[0] + 330, screen_rect[1] + 4))
    pygame.draw.line(screen, colour, (screen_rect[0] + 4, screen_rect[1] + 4), (screen_rect[0] + 4, screen_rect[1] + 30))
    pygame.draw.line(screen, colour, (screen_rect[0] + 4, screen_rect[1] + 30), (screen_rect[0] + 300, screen_rect[1] + 30))
    pygame.draw.line(screen, colour, (screen_rect[0] + 300, screen_rect[1] + 30), (screen_rect[0] + 330, screen_rect[1] + 4))

    pygame.draw.line(screen, colour, (screen_rect[0] + 330, screen_rect[1] + 4), (screen_rect[0] + screen_rect[2] - 12, screen_rect[1] + 4))

    pygame.draw.line(screen, colour, (screen_rect[0] + screen_rect[2] - 12, screen_rect[1] + 4), (screen_rect[0] + screen_rect[2] - 4, screen_rect[1] + 12))

    pygame.draw.line(screen, colour, (screen_rect[0] + screen_rect[2] - 4, screen_rect[1] + 12), (screen_rect[0] + screen_rect[2] - 4, screen_rect[1] + screen_rect[3] - 4))
    pygame.draw.line(screen, colour, (screen_rect[0] + 4, screen_rect[1] + screen_rect[3] - 4), (screen_rect[0] + screen_rect[2] - 4, screen_rect[1] + screen_rect[3] - 4))
    pygame.draw.line(screen, colour, (screen_rect[0] + 4, screen_rect[1] + screen_rect[3] - 4), (screen_rect[0] + 4, screen_rect[1] + 30))

    pygame.draw.line(screen, colour, (screen_rect[0] + screen_rect[2] - gccGreenImage.get_width() - 4, screen_rect[1] + gccGreenImage.get_height() + 12),
                     (screen_rect[0] + screen_rect[2] - 4, screen_rect[1] + gccGreenImage.get_height() + 12))
    pygame.draw.line(screen, colour, (screen_rect[0] + screen_rect[2] - gccGreenImage.get_width() - 4, screen_rect[1] + gccGreenImage.get_height() + 12),
                     (screen_rect[0] + screen_rect[2] - gccGreenImage.get_width() - 12, screen_rect[1] + gccGreenImage.get_height() + 4))

    pygame.draw.line(screen, colour, (screen_rect[0] + screen_rect[2] - gccGreenImage.get_width() - 12, screen_rect[1] + 4),
                     (screen_rect[0] + screen_rect[2] - gccGreenImage.get_width() - 12, screen_rect[1] + gccGreenImage.get_height() + 4))


def draw_filled_rect(pos, size, colour=LIGHT_BLUE):
    pygame.draw.rect(screen, colour, pygame.Rect(pos, size))


def draw_image(image, pos, stick=6):
    screen.blit(image, pos)

    draw_rect(pos, image.get_size(), stick=stick, outside=1)


def draw_up_arrow(x1, y1, x2, y2, colour):
    pygame.draw.line(screen, colour, (x1, y2), (x1 + (x2 - x1) / 2, y1))
    pygame.draw.line(screen, colour, (x1 + (x2 - x1) / 2, y1), (x2, y2))
    pygame.draw.line(screen, colour, (x1, y2), (x2, y2))


def draw_down_arrow(x1, y1, x2, y2, colour):
    pygame.draw.line(screen, colour, (x1, y1), (x1 + (x2 - x1) / 2, y2))
    pygame.draw.line(screen, colour, (x1 + (x2 - x1) / 2, y2), (x2, y1))
    pygame.draw.line(screen, colour, (x1, y1), (x2, y1))


def draw_graph(pos, size, data, min_data, max_data, max_points, axis_colour=LIGHT_BLUE, data_colour=GREEN, stick=0):

    def calc_point(_d, mn, mx, _x, _y, h):
        r = mx - mn - 1
        if r < 5:
            r = 5

        _d = _d - mn
        if _d > mx:
            _d = mx
        if _d < 0:
            _d = 0
        _d = r - _d

        return _x, _y + int(_d / r * h)

    outside = 0

    # pygame.draw.line(screen, axisColour, (pos[0] - stick, pos[1] - outside), (pos[0] + size[0] + stick, pos[1] - outside))
    pygame.draw.line(screen, axis_colour, (pos[0] - stick, pos[1] + size[1] + outside), (pos[0] + size[0] + stick, pos[1] + size[1] + outside))

    pygame.draw.line(screen, axis_colour, (pos[0] - outside, pos[1] - stick), (pos[0] - outside, pos[1] + size[1] + stick))
    # pygame.draw.line(screen, axisColour, (pos[0] + size[0] + outside, pos[1] - stick), (pos[0] + size[0] + outside, pos[1] + size[1] + stick))

    if len(data) > 1:
        to = len(data) - max_points
        if to < 0:
            to = 0

        stretch = size[0] / min([max_points, len(data) - 1])

        x = pos[0] + size[0] - 1

        _ld = data[len(data) - 1]
        lp = calc_point(_ld, min_data, max_data, x, pos[1], size[1])

        for i in range(len(data) - 2, to - 1, -1):
            x = x - int(stretch)
            d = data[i]
            p = calc_point(d, min_data, max_data, x, pos[1], size[1])

            pygame.draw.line(screen, data_colour, lp, p)
            _ld = d
            lp = p
