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
import pyros
import pyros_support_ui.gccui
import threading
import time
import socket
import netifaces
import sys

from pyros_support_ui import gccui


DEBUG = False

rovers = []
do_discovery = True
show_rovers = False
selected_rover = 0
connected_rover = 0
selectedRoverMap = {}

# {
#     "rover2": {
#         "address": "172.24.1.184",
#         "port": 1883
#     },
#     "rover3": {
#         "address": "172.24.1.185",
#         "port": 1883
#     },
#     "rover4": {
#         "address": "172.24.1.186",
#         "port": 1883
#     },
#     "rover2proxy": {
#         "address": "gcc-wifi-ap",
#         "port": 1884
#     },
#     "rover3proxy": {
#         "address": "gcc-wifi-ap",
#         "port": 1885
#     },
#     "rover4proxy": {
#         "address": "gcc-wifi-ap",
#         "port": 1886
#     },
# }

THIS_PORT = 0xd15d
DISCOVERY_PORT = 0xd15c
BROADCAST_TIMEOUT = 5  # every 5 seconds
ROVER_TIMEOUT = 30  # 30 seconds no

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sckt.settimeout(1)


def setup_listen_socket():
    global THIS_PORT
    connected = 5

    while connected > 0:
        # noinspection PyBroadException
        try:
            sckt.bind(('', THIS_PORT))
            connected = 0
        except Exception:
            THIS_PORT = THIS_PORT + 1


setup_listen_socket()


def get_broadcasts():
    broadcasts = []

    ifacenames = netifaces.interfaces()
    for ifname in ifacenames:
        addrs = netifaces.ifaddresses(ifname)

        for d in addrs:
            for dx in addrs[d]:
                if "broadcast" in dx:
                    broadcasts.append(dx["broadcast"])
    return broadcasts


def add_to_list(rover_map):
    rover_map["lastSeen"] = time.time()
    if "PORT" in rover_map:
        rover_map["PORT"] = int(rover_map["PORT"])

    for rover in rovers:
        if rover["IP"] == rover_map["IP"] and rover["PORT"] == rover_map["PORT"]:
            for key in rover_map:
                rover[key] = rover_map[key]
            return

    rovers.append(rover_map)
    print("Found new rover " + str(rover_map["NAME"]) + " @ " + str(rover_map["IP"]) + ":" + str(rover_map["PORT"]))


def discover():
    global do_discovery
    packet = "Q#IP=255.255.255.255;PORT=" + str(THIS_PORT)

    last_broadcast_time = time.time()

    while True:
        if do_discovery or time.time() - last_broadcast_time > BROADCAST_TIMEOUT:
            do_discovery = False
            # noinspection PyBroadException
            try:
                broadcasts = get_broadcasts()

                for broadcast in broadcasts:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    bs = bytes(packet, 'utf-8')
                    s.sendto(bs, (broadcast, DISCOVERY_PORT))
                last_broadcast_time = time.time()

                for i in range(len(rovers) - 1, -1, -1):
                    rover = rovers[i]
                    if rover["lastSeen"] + ROVER_TIMEOUT < time.time():
                        print("Lost connection to rover " + str(rovers[i]["name"]) + " @ " + str(rovers[i]["ip"]) + ":" + str(rovers[i]["port"]))
                        del rovers[i]
            except Exception:
                pass

        # noinspection PyBroadException
        try:
            data, addr = sckt.recvfrom(1024)

            p = str(data, 'utf-8')

            if p.startswith("A#"):
                kvs = p[2:].split(";")

                ip = None
                name = None
                port = None
                device_type = None

                rover_map = {}

                for keyValue in kvs:
                    kvp = keyValue.split("=")
                    if len(kvp) == 2:
                        rover_map[kvp[0]] = kvp[1]
                        if kvp[0] == "IP":
                            ip = kvp[1]
                        elif kvp[0] == "PORT":
                            # noinspection PyBroadException
                            try:
                                port = int(kvp[1])
                            except Exception:
                                pass
                        elif kvp[0] == "NAME":
                            name = kvp[1]
                        elif kvp[0] == "TYPE":
                            device_type = kvp[1]
                        elif kvp[0] == "PYROS":
                            # noinspection PyBroadException
                            try:
                                port = int(kvp[1])
                            except Exception:
                                pass
                            device_type = "ROVER"

                if name is None:
                    name = ip
                if (port is not None) and (ip is not None) and device_type == "ROVER":
                    add_to_list(rover_map)
                    received_something = True

            print("Got " + p + "  Rovers: " + str(rovers))
        except Exception:
            pass


def add_supplied_rover():
    rover_map = {}

    kv = sys.argv[1].split(":")
    if len(kv) == 1:
        kv.append("1883")

    rover_map["IP"] = kv[0]
    rover_map["PORT"] = int(kv[1])
    rover_map["NAME"] = "Rover(args)"
    rover_map["TYPE"] = "ROVER"
    rover_map["JOY_PORT"] = "1880"

    add_to_list(rover_map)


if len(sys.argv) > 1:
    add_supplied_rover()

else:
    thread = threading.Thread(target=discover, args=())
    thread.daemon = True
    thread.start()


def get_host():
    if len(rovers) == 0:
        return None
    if DEBUG:
        print("Selected rover " + str(rovers[selected_rover]))
    return rovers[selected_rover]["IP"]


def get_port():
    if len(rovers) == 0:
        return None
    return int(rovers[selected_rover]["PORT"])


def connect():
    global selected_rover, connected_rover

    connected_rover = selected_rover

    if len(rovers) == 0:
        return None
    pyros.connect(rovers[selected_rover]["IP"], rovers[selected_rover]["PORT"], waitToConnect=False)


lmeta = False
rmeta = False
lshift = False
rshift = False


def handle_connect_key_down(key):
    global selected_rover, do_discovery, show_rovers
    global lmeta, rmeta, lshift, rshift

    if key == pygame.K_LMETA:
        lmeta = True
    elif key == pygame.K_RMETA:
        rmeta = True
    elif key == pygame.K_LSHIFT:
        lshift = True
    elif key == pygame.K_RSHIFT:
        rshift = True
    elif lmeta and key == pygame.K_q:
        sys.exit(0)

    if key == pygame.K_1 and (lmeta or rmeta):
        do_discovery = True
        show_rovers = True
    elif key == pygame.K_TAB:
        if show_rovers:
            if lshift or rshift:
                selected_rover -= 1
                if selected_rover < 0:
                    selected_rover = len(rovers) - 1
            else:
                selected_rover += 1
                if selected_rover >= len(rovers):
                    selected_rover = 0
        else:
            show_rovers = True
    elif show_rovers and key == pygame.K_UP and selected_rover > 0:
        selected_rover -= 1
    elif show_rovers and key == pygame.K_DOWN and selected_rover < len(rovers) - 1:
        selected_rover += 1
    elif show_rovers and key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
        connect()
        show_rovers = False
    elif show_rovers and key == pygame.K_ESCAPE:
        show_rovers = False
    elif key == pygame.K_F5:
        connect()

    return show_rovers


def handle_connect_key_up(key):
    global lmeta, rmeta, lshift, rshift

    if key == pygame.K_LMETA:
        lmeta = False
    elif key == pygame.K_RMETA:
        rmeta = False
    elif key == pygame.K_LSHIFT:
        lshift = False
    elif key == pygame.K_RSHIFT:
        rshift = False

    return show_rovers


def get_selected_rover_details_text(i):
    if selected_rover >= len(rovers):
        return "No rovers"

    name = "Unknown Rover"

    if "NAME" in rovers[i]:
        name = rovers[i]["NAME"]

    if name.startswith("gcc-rover-"):
        name = "GCC Rover " + name[10:]

    return name


def get_selected_rover_ip(i):
    if selected_rover >= len(rovers):
        return ""

    return str(rovers[i]["IP"]) + ":" + str(rovers[i]["PORT"])


_connection_counter = 1
_state = 1


def _draw_red_indicator():
    if _state == 1:
        gccui.draw_rect((9, 10), (16, 16), (96, 0, 0, 128), 2, 0)
        gccui.draw_rect((11, 12), (11, 11), (160, 0, 0, 64), 2, 0)
        gccui.draw_filled_rect((13, 14), (8, 8), (255, 0, 0, 64))
    if _state == 0:
        gccui.draw_filled_rect((9, 10), (16, 16), (160, 0, 0, 128))
        gccui.draw_rect((11, 12), (11, 11), (180, 0, 0, 64), 2, 0)
        gccui.draw_filled_rect((13, 14), (8, 8), (255, 0, 0, 64))


def _draw_green_indicator():
    if _state == 0 or _state == 1:
        gccui.draw_filled_rect((9, 10), (16, 16), (0, 128, 0, 128))
        gccui.draw_rect((11, 12), (11, 11), (0, 180, 0, 64), 2, 0)
        gccui.draw_filled_rect((13, 14), (8, 8), (0, 255, 0, 64))
    if _state == 2:
        gccui.draw_filled_rect((11, 10), (16, 16), (0, 96, 0, 128))
        gccui.draw_rect((9, 12), (15, 11), (0, 160, 0, 64), 2, 0)
        gccui.draw_filled_rect((11, 14), (12, 8), (0, 220, 0, 64))


def draw_connection():

    def draw_rover(rover_index, pos, colour):
        w = gccui.font.size(get_selected_rover_details_text(rover_index))[0]
        gccui.screen.blit(gccui.font.render(get_selected_rover_details_text(rover_index), 1, colour), pos)
        gccui.screen.blit(gccui.smallFont.render(get_selected_rover_ip(rover_index), 1, colour), (pos[0] + 8 + w, pos[1] + 5))

    global _connection_counter, _state
    if pyros.isConnected():
        _connectionCounter -= 1
        if _connectionCounter < 0:
            if _state == 0:
                _state = 2
                _connectionCounter = 10
            elif _state == 1:
                _state = 0
                _connectionCounter = 10
            elif _state == 2:
                _state = 1
                _connectionCounter = 10

        _draw_green_indicator()
        draw_rover(connected_rover, (32, 0), gccui.GREEN)
    else:
        _connectionCounter -= 1
        if _connectionCounter < 0:
            _connectionCounter = 10
            _state -= 1
            if _state < 0:
                _state = 3

        _draw_red_indicator()
        draw_rover(connected_rover, (32, 0), gccui.RED)

    if show_rovers:
        gccui.draw_frame(pygame.Rect(0, 30, 250, 178), gccui.LIGHT_BLUE, gccui.BLACK)

        st = 0
        if selected_rover > 2:
            st = selected_rover - 2

        en = st + 5
        if en > len(rovers):
            en = len(rovers)

        while en - st < 5 and st > 0:
            st = st - 1

        for i in range(st, en):
            y = 30 + (i - st) * 30 + 12
            if i == selected_rover:
                pygame.draw.rect(gccui.screen, gccui.DARK_GREY, pygame.Rect(8, y, 234, 30), 0)

            draw_rover(i, (12, y), gccui.LIGHT_BLUE)

        if st > 0:
            gccui.draw_up_arrow(120, 38, 130, 42, gccui.LIGHT_BLUE)
        if en < len(rovers):
            gccui.draw_down_arrow(120, 194, 130, 198, gccui.LIGHT_BLUE)
