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
from local_resources import Resource
from io import BytesIO
from io import StringIO

last_keys = []
keys = []


def process_keys(on_key_down, on_key_up):
    global last_keys, keys

    last_keys = keys
    keys = pygame.key.get_pressed()
    if not len(keys) == 0 and not len(last_keys) == 0:

        for i in range(0, len(keys)):

            if keys[i] and not last_keys[i]:
                on_key_down(i)
            if not keys[i] and last_keys[i]:
                on_key_up(i)


def load_font(font_name: str, font_size: int):
    with Resource(font_name) as f:
        return pygame.font.Font(BytesIO(f.read()), font_size)


def load_image(image_name: str):
    with Resource(image_name) as f:
        return pygame.image.load(BytesIO(f.read()))
