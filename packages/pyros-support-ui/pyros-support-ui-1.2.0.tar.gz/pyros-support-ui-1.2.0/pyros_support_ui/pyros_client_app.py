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
from typing import Optional

import pygame
import pyros
import threading
import traceback
import time

from functools import partial

from pygame import Rect, draw

from pyros_support_ui.components import Component, Collection, Button
from discovery import Discover


_GREEN = (128, 255, 128)
_RED = (255, 128, 128)
_YELLOW = (255, 255, 128)
_BLUE = (128, 128, 255)
_LIGHT_BLUE = (160, 255, 255)
_BLACK = (0, 0, 0)
_DARK_GREY = (80, 80, 80)
_GREY = (160, 160, 160)
_WHITE = (255, 255, 255)


class _DiscoveredRover:
    def __init__(self, host: str, port: int, name: str, predefined: bool = False):
        self.host = host
        self.port = port
        self.name = name
        self.predefined = predefined


class ScreenFrame(Component):
    def __init__(self, rect,
                 line_colour, background_colour,
                 margin=4,
                 background_image=None,
                 logo_image=None, logo_alt_image=None):
        super(ScreenFrame, self).__init__(rect)
        self.background_image = background_image
        self.logo_image = logo_image
        self.logo_alt_image = logo_alt_image if logo_alt_image else logo_image
        self.line_colour = line_colour
        self.background_colour = background_colour
        self.margin = margin

    def draw(self, surface):
        if self.background_image is not None:
            surface.blit(self.background_image, (0, 0))
        else:
            if self.background_colour is not None:
                draw.rect(surface, self.background_colour, self.rect, 0)
            else:
                surface.fill((0, 0, 0))

        rect = self.rect
        draw.rect(surface, self.line_colour, (rect.x + self.margin, rect.y + self.margin, rect.width - self.margin * 2, rect.height - self.margin * 2), 1)
        for _i in range(6, 12):
            draw.line(surface, self.line_colour, (rect.x + rect.width - _i, rect[1] + rect.height - self.margin - 2), (rect.x + rect.width - self.margin - 2, rect.y + rect.height - _i), 1)

        if self.logo_image is not None:
            image_size = self.logo_image.get_size()
            if int(time.time()) % 20 < 10:
                surface.blit(self.logo_image, (rect.x + rect.width - self.margin * 2 - self.logo_image.get_width(), rect.y + self.margin * 2))
            else:
                surface.blit(self.logo_alt_image, (rect.x + rect.width - self.margin * 2 - self.logo_alt_image.get_width(), rect.y + self.margin * 2))
        else:
            image_size = (32, 32)

        draw.line(surface, self.line_colour, (rect.x + rect.width - image_size[0] - self.margin, rect.y + image_size[1] + 12),
                  (rect.x + rect.width - self.margin, rect.y + image_size[1] + 12))
        draw.line(surface, self.line_colour, (rect.x + rect.width - image_size[0] - self.margin, rect.y + image_size[1] + 12),
                  (rect.x + rect.width - image_size[0] - 12, rect.y + image_size[1] + self.margin))

        draw.line(surface, self.line_colour, (rect.x + rect.width - image_size[0] - 12, rect.y + self.margin),
                  (rect.x + rect.width - image_size[0] - 12, rect.y + image_size[1] + self.margin))


class PyrosServersButton(Button):
    def __init__(self, rect, colour,
                 slate=30,
                 font=None,
                 small_font=None,
                 on_click=None):

        super(PyrosServersButton, self).__init__(rect, on_click=on_click)  # Call super constructor to store rectangle
        self.colour = colour
        self.font = font
        self.small_font = small_font
        self.slate = slate
        self._state = 1
        self._connection_counter = 1
        self.rovers = []
        self.selected_rover = None

    def draw(self, surface):
        def _draw_rect(pos, size, colour, stick=0, outside=1):
            draw.line(surface, colour, (pos[0] - stick, pos[1] - outside), (pos[0] + size[0] + stick, pos[1] - outside))
            draw.line(surface, colour, (pos[0] - stick, pos[1] + size[1] + outside), (pos[0] + size[0] + stick, pos[1] + size[1] + outside))

            draw.line(surface, colour, (pos[0] - outside, pos[1] - stick), (pos[0] - outside, pos[1] + size[1] + stick))
            draw.line(surface, colour, (pos[0] + size[0] + outside, pos[1] - stick), (pos[0] + size[0] + outside, pos[1] + size[1] + stick))

        def _draw_filled_rect(pos, size, colour=_LIGHT_BLUE):
            draw.rect(surface, colour, pygame.Rect(pos, size))

        def _draw_red_indicator():
            if self._state == 1:
                _draw_rect((9, 10), (16, 16), (96, 0, 0, 128), 2, 0)
                _draw_rect((11, 12), (11, 11), (160, 0, 0, 64), 2, 0)
                _draw_filled_rect((13, 14), (8, 8), (255, 0, 0, 64))
            if self._state == 0:
                _draw_filled_rect((9, 10), (16, 16), (160, 0, 0, 128))
                _draw_rect((11, 12), (11, 11), (180, 0, 0, 64), 2, 0)
                _draw_filled_rect((13, 14), (8, 8), (255, 0, 0, 64))

        def _draw_green_indicator():
            if self._state == 0 or self._state == 1:
                _draw_filled_rect((9, 10), (16, 16), (0, 128, 0, 128))
                _draw_rect((11, 12), (11, 11), (0, 180, 0, 64), 2, 0)
                _draw_filled_rect((13, 14), (8, 8), (0, 255, 0, 64))
            if self._state == 2:
                _draw_filled_rect((11, 10), (16, 16), (0, 96, 0, 128))
                _draw_rect((9, 12), (15, 11), (0, 160, 0, 64), 2, 0)
                _draw_filled_rect((11, 14), (12, 8), (0, 220, 0, 64))

        def _get_selected_rover_ip(rover):
            return rover.host + ":" + str(rover.port) if rover is not None else ""

        def _draw_rover(rover, pos, colour):
            rover_details_text = rover.name if rover is not None else ("No Rovers" if len(self.rovers) == 0 else "Select Rover")
            if len(rover_details_text) > 0:
                w = self.font.size(rover_details_text)[0]
                sur = self.font.render(rover_details_text, 1, colour)
                surface.blit(sur, pos)
                surface.blit(self.small_font.render(_get_selected_rover_ip(rover), 1, colour), (pos[0] + 8 + w, pos[1] + 5))

        rect = self.rect

        draw.line(surface, self.colour, (rect.x, rect.y), (rect.x + rect.width, rect.y))
        draw.line(surface, self.colour, (rect.x, rect.y), (rect.x, rect.y + rect.height))
        draw.line(surface, self.colour, (rect.x, rect.y + self.slate), (rect.x + rect.width - self.slate, rect.y + self.slate))
        draw.line(surface, self.colour, (rect.x + rect.width - self.slate, rect.y + self.slate), (rect.x + rect.width, rect.y))

        if pyros.is_connected():
            self._connection_counter -= 1
            if self._connection_counter < 0:
                if self._state == 0:
                    self._state = 2
                    _connection_counter = 10
                elif self._state == 1:
                    self._state = 0
                    self._connection_counter = 10
                elif self._state == 2:
                    self._state = 1
                    self._connection_counter = 10
                else:
                    self._state = 0

            _draw_green_indicator()
            _draw_rover(self.selected_rover, (32, 0), _GREEN)
        else:
            self._connection_counter -= 1
            if self._connection_counter < 0:
                self._connection_counter = 10
                self._state -= 1
                if self._state < 0:
                    self._state = 3

            _draw_red_indicator()
            _draw_rover(self.selected_rover, (32, 0), _RED)


class PyrosClientApp(Collection):
    _DISCOVERY_TIMEOUT = 30  # Every 10 seconds

    def __init__(self, ui_factory,
                 background_image=None,
                 logo_image=None, logo_alt_image=None,
                 font=None,
                 small_font=None,
                 connect_to_first=False,
                 connect_to_only=True,
                 rover_filter=None):
        super(PyrosClientApp, self).__init__(None)  # Call super constructor to store rectable
        self.ui_factory = ui_factory
        self.ui_adapter = ui_factory.ui_adapter
        self.content: Optional[Component] = None
        self.modal: Optional[Component] = None
        self.background_image = background_image
        self.logo_image = logo_image
        self.logo_alt_image = logo_alt_image if logo_alt_image else logo_image
        self.line_colour = ui_factory.colour
        self.font = font if font is not None else self.ui_factory.font
        self.small_font = small_font if small_font is not None else self.ui_factory.small_font
        
        self.screen_frame = ScreenFrame(None, self.line_colour, ui_factory.background_colour,
                                        background_image=background_image,
                                        logo_image=logo_image, logo_alt_image=logo_alt_image)
        self.add_component(self.screen_frame)

        self.discovery = Discover(5)
        self.thread = None
        self.connect_to_first = connect_to_first
        self.connect_to_only = connect_to_only
        self.rover_filter = rover_filter
        self._first_discovery_run = True
        self.rovers_button = PyrosServersButton(Rect(0, 0, 100, 30), ui_factory.colour,
                                                font=self.font,
                                                small_font=self.small_font,
                                                on_click=self._show_rovers_action)
        self.add_component(self.rovers_button)

        self.rovers_menu = ui_factory.menu(Rect(0, 0, 150, 200), background_colour=pygame.color.THECOLORS['black'])
        # self.rovers_menu.add_menu_item("item1", partial(self._select_rover, 0), height=30)
        # self.rovers_menu.add_menu_item("item2", partial(self._select_rover, 1), height=30)
        self.add_component(self.rovers_menu)
        self.on_connected_subscribers = []
        self.redefine_rect(self.ui_adapter.screen.get_rect())

    def set_modal(self, modal: Component) -> None:
        self.modal = modal
        self.modal.redefine_rect(self.rect)

    def clear_modal(self) -> None:
        self.modal = None

    def _show_rovers_action(self, _button, _pos):
        self.rovers_menu.show()

    def _select_rover(self, rover, _button, _pos):
        print(f"Selected: rover {rover.host}:{rover.port} {rover.name}")
        if self.rovers_button.selected_rover != rover:
            print(f"  Connecting rover {rover.host}:{rover.port} {rover.name}")
            pyros.connect(rover.host, rover.port, wait_to_connect=False)
            print(f"  Connected rover {rover.host}:{rover.port} {rover.name}")
            self.rovers_button.selected_rover = rover
        elif not pyros.is_connected():
            print(f"  Reconnecting rover {rover.host}:{rover.port} {rover.name}")
            pyros.connect(rover.host, rover.port, wait_to_connect=False)
            print(f"  Connected rover {rover.host}:{rover.port} {rover.name}")
        else:
            print(f"  Selected rover {rover.host}:{rover.port} {rover.name} - is already selected")
        self.rovers_menu.hide()

    def _set_contents_rectangle(self, rect):
        inside = Rect(rect.x + self.screen_frame.margin + 2,
                      self.rovers_button.rect.bottom + self.screen_frame.margin,
                      rect.width - self.screen_frame.margin * 2 - 4,
                      rect.bottom - self.rovers_button.rect.bottom - self.screen_frame.margin * 2 - 2)
        self.content.redefine_rect(inside)

    def find_component(self, pos) -> Optional[Component]:
        if self.modal is not None:
            rect = self.modal.rect
            if self.modal.visible and rect is not None and rect.collidepoint(pos):
                return self.modal
        else:
            return super().find_component(pos)
        return None

    def redefine_rect(self, rect):
        # super(RoverClientApp, self).redefine_rect(rect)
        self.rect = rect
        self.screen_frame.redefine_rect(rect)
        self.rovers_button.redefine_rect(Rect(rect.x + self.screen_frame.margin, rect.y + self.screen_frame.margin, 320, 30))
        self.rovers_menu.redefine_rect(Rect(self.rovers_button.rect.x, self.rovers_button.rect.bottom, self.rovers_button.rect.width - self.rovers_button.slate * 2, 10))
        if self.content is not None:
            self._set_contents_rectangle(rect)

        if self.modal is not None:
            self.modal.draw(rect)

    def set_content(self, component):
        self.content = component
        top = self.components[-1]
        del self.components[-1]
        self.add_component(component)
        self.add_component(top)
        self._set_contents_rectangle(self.rect)

    def draw_border(self, surface):
        if self.background_image is not None:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill((0, 0, 0))

        screen_rect = self.rect

        if self.logo_image is not None:
            image_size = self.logo_image.get_size()
            if int(time.time()) % 20 < 10:
                surface.blit(self.logo_image, (screen_rect.x + screen_rect.width - 8 - self.logo_image.get_width(), screen_rect.y + 8))
            else:
                surface.blit(self.logo_alt_image, (screen_rect.x + screen_rect.width - 8 - self.logo_alt_image.get_width(), screen_rect.y + 8))
        else:
            image_size = (32, 32)

        draw.line(surface, self.line_colour, (screen_rect.x + 4, screen_rect.y + 4), (screen_rect.x + 330, screen_rect.y + 4))
        draw.line(surface, self.line_colour, (screen_rect.x + 4, screen_rect.y + 4), (screen_rect.x + 4, screen_rect.y + 30))
        draw.line(surface, self.line_colour, (screen_rect.x + 4, screen_rect.y + 30), (screen_rect.x + 300, screen_rect.y + 30))
        draw.line(surface, self.line_colour, (screen_rect.x + 300, screen_rect.y + 30), (screen_rect.x + 330, screen_rect.y + 4))

        draw.line(surface, self.line_colour, (screen_rect.x + 330, screen_rect.y + 4), (screen_rect.x + screen_rect.width - 12, screen_rect.y + 4))

        draw.line(surface, self.line_colour, (screen_rect.x + screen_rect.width - 12, screen_rect.y + 4), (screen_rect.x + screen_rect.width - 4, screen_rect.y + 12))

        draw.line(surface, self.line_colour, (screen_rect.x + screen_rect.width - 4, screen_rect.y + 12), (screen_rect.x + screen_rect.width - 4, screen_rect.y + screen_rect.height - 4))
        draw.line(surface, self.line_colour, (screen_rect.x + 4, screen_rect.y + screen_rect.height - 4), (screen_rect.x + screen_rect.width - 4, screen_rect.y + screen_rect.height - 4))
        draw.line(surface, self.line_colour, (screen_rect.x + 4, screen_rect.y + screen_rect.height - 4), (screen_rect.x + 4, screen_rect.y + 30))

        draw.line(surface, self.line_colour, (screen_rect.x + screen_rect.width - image_size[0] - 4, screen_rect.y + image_size[1] + 12),
                  (screen_rect.x + screen_rect.width - 4, screen_rect.y + image_size[1] + 12))
        draw.line(surface, self.line_colour, (screen_rect.x + screen_rect.width - image_size[0] - 4, screen_rect.y + image_size[1] + 12),
                  (screen_rect.x + screen_rect.width - image_size[0] - 12, screen_rect.y + image_size[1] + 4))

        draw.line(surface, self.line_colour, (screen_rect.x + screen_rect.width - image_size[0] - 12, screen_rect.y + 4),
                  (screen_rect.x + screen_rect.width - image_size[0] - 12, screen_rect.y + image_size[1] + 4))

    def draw(self, surface) -> None:
        super().draw(surface)
        if self.modal is not None:
            self.modal.draw(surface)

    def pyros_init(self, pyros_mqtt_client_name, unique=True):
        pyros.init(pyros_mqtt_client_name, unique=unique, host=None, port=1883, wait_to_connect=False, on_connected=self._pyros_connected)

    def _pyros_connected(self):
        for on_connected_subscriber in self.on_connected_subscribers:
            try:
                on_connected_subscriber()
            except Exception as ex:
                print("MainLoop Exception: " + str(ex) + "\n" + ''.join(traceback.format_tb(ex.__traceback__)))

    def add_on_connected_subscriber(self, subscriber):
        self.on_connected_subscribers.append(subscriber)

    def remove_on_connected_subscriber(self, subscriber):
        self.on_connected_subscribers.remove(subscriber)

    def add_from_arguments(self, host_port: str, extra_data: dict = None):
        kv = host_port.split(":")
        if len(kv) == 1:
            kv.append("1883")

        rover_map = {
            "IP": kv[0],
            "PORT": int(kv[1]),
            "NAME": "Rover(args)",
            "TYPE": "ROVER",
            "PYROS": int(kv[1])
        }
        if extra_data is not None:
            rover_map.update(extra_data)

        rover = self.create_to_rover(rover_map)
        rover.predefined = True

        self.rovers_button.rovers.append(rover)
        self.rovers_menu.add_menu_item(rover.name, partial(self._select_rover, rover), height=30)

        self.rovers_button.selected_rover = rover
        pyros.connect(rover.host, rover.port, wait_to_connect=False)
        self._first_discovery_run = False

    def create_to_rover(self, response: dict) -> Optional[_DiscoveredRover]:
        def process_name(_host, _port, name):
            return "Unknown Rover" if name is None else name.replace("gcc-rover-", "GCC Rover ")

        def make_rover(host: str, port: str, name: str) -> Optional[_DiscoveredRover]:
            # noinspection PyBroadException
            try:
                _port = int(port)
                return _DiscoveredRover(host, _port, process_name(host, port, name))
            except Exception:
                return None

        rover = None
        if 'IP' in response and 'PYROS' in response:
            rover = make_rover(response['IP'], response['PYROS'], process_name(response['IP'], response['PYROS'], response.get('NAME')))
        elif 'IP' in response and 'PORT' in response and 'TYPE' in response and response['TYPE'] == 'ROVER':
            # backward compatibility
            rover = make_rover(response['IP'], response['PORT'], process_name(response['IP'], response['PORT'], response.get('NAME')))
        # else:
        #     rover = make_rover(response['IP'], 1883, process_name(response['IP'], 1883, response.get('NAME')))
        return rover if self.rover_filter is None or self.rover_filter(response, rover) else None

    def run_discovery(self):
        def connect_to_first_callback(response):
            rover = self.create_to_rover(response)
            self.rovers_button.selected_rover = rover
            pyros.connect(rover.host, rover.port, wait_to_connect=False)

        callback = None
        if self._first_discovery_run and self.connect_to_first:
            callback = connect_to_first_callback
        responses = self.discovery.discover(callback)

        existing_rover_ids = set([r.host + str(r.port) + (r.name if r.name is not None else "") for r in self.rovers_button.rovers])
        new_rovers = []
        for response in responses:
            rover = self.create_to_rover(response)
            if rover is not None:
                new_rovers.append(rover)

        new_rover_ids = set([r.host + str(r.port) + (r.name if r.name is not None else "") for r in new_rovers])

        if existing_rover_ids != new_rover_ids:
            self.rovers_menu.clear_menu_items()
            predefined_rovers = [rover for rover in self.rovers_button.rovers if rover.predefined]
            del self.rovers_button.rovers[:]
            for rover in predefined_rovers + new_rovers:
                self.rovers_button.rovers.append(rover)
                self.rovers_menu.add_menu_item(rover.name, partial(self._select_rover, rover), height=30)

        if self._first_discovery_run:
            self._first_discovery_run = False
            if self.connect_to_only and not self.connect_to_first and len(self.rovers_button.rovers) == 1:
                rover = self.rovers_button.rovers[0]
                self.rovers_button.selected_rover = rover
                pyros.connect(rover.host, rover.port, wait_to_connect=False)

    def start_discovery_in_background(self):
        def _run_discovery_thread():
            last_run = 0
            while True:
                # noinspection PyBroadException
                try:
                    now = time.time()
                    if now - last_run < self._DISCOVERY_TIMEOUT:
                        time.sleep(now - last_run)
                    last_run = now
                    self.run_discovery()
                except Exception as ex:
                    pass  # Ignore errors
                    print("MainLoop Exception: " + str(ex) + "\n" + ''.join(traceback.format_tb(ex.__traceback__)))

        self.thread = threading.Thread(target=_run_discovery_thread, daemon=True)
        self.thread.start()

    def key_down(self, code):
        if code == pygame.K_TAB:
            if self.rovers_menu.visible:
                self.rovers_menu.hide()
            else:
                self._show_rovers_action(None, None)
            return True

        if self.rovers_menu.visible:
            return self.rovers_menu.key_down(code)
        return False

    def key_up(self, code):
        if self.rovers_menu.visible:
            return self.rovers_menu.key_up(code)
        return False
