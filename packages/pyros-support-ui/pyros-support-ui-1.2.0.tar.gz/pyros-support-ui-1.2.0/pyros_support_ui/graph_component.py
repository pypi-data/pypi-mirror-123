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
from typing import Union, List, Tuple, Optional, Callable

import pygame
import time

from pyros_support_ui.components import ALIGNMENT, Button, BaseUIFactory

NumberType = Union[int, float]
DataType = List[Tuple[float, NumberType]]


class GraphData:
    def __init__(self, maximum: NumberType, minimum: NumberType):
        self.maximum = maximum
        self.minimum = minimum
        self.name = ""

    def fetch(self, from_timestamp: float, to_timestamp: float) -> DataType:
        return []


class AutoScalingData(GraphData):
    def __init__(self, maximum: NumberType, minimum: NumberType):
        super(AutoScalingData, self).__init__(maximum, minimum)
        self._default_min = minimum
        self._default_max = maximum
        self._last_min_seen: Optional[NumberType] = None
        self._last_max_seen: Optional[NumberType] = None

    def auto_scale_data(self, data: DataType) -> None:
        max_seen = False
        max_found = -100000000
        min_seen = False
        min_found = 100000000
        for i in range(len(data)):
            if self.maximum < data[i][1]:
                self.maximum = data[i][1]
                self._last_max_seen = data[i][0]
                max_seen = True
            elif not max_seen and max_found < data[i][1]:
                max_found = data[i][1]
            if self.minimum > data[i][1]:
                self.minimum = data[i][1]
                self._last_min_seen = data[i][0]
                min_seen = True
            elif not min_seen and min_found > data[i][1]:
                min_found = data[i][1]
        if not max_seen:
            if max_found < self._default_max:
                max_found = self._default_max
            if max_found < self.maximum:
                self.maximum = max_found
        if not min_seen:
            if min_found > self._default_min:
                min_found = self._default_min
            if min_found > self.minimum:
                self.minimum = min_found


class TelemetryGraphData(AutoScalingData):
    def __init__(self,
                 telemetry_client,
                 stream,
                 column_name: str,
                 maximum: NumberType, minimum: NumberType, auto_scale: bool = False):
        super(TelemetryGraphData, self).__init__(maximum, minimum)
        self.telemetry_client = telemetry_client
        self.stream = stream
        self.name = column_name
        self.column_index = -1
        self.collect = True
        self.auto_scale = auto_scale

        for i, field in enumerate(self.stream.get_fields()):
            if field.name == column_name:
                self.column_index = i

    def fetch(self, from_timestamp: float, to_timestamp: float) -> DataType:
        result = []

        if self.collect:
            def fetch(data):
                result.extend([[d[0], d[self.column_index + 1]] for d in data])
                if self.auto_scale:
                    self.auto_scale_data(result)

            self.telemetry_client.retrieve(self.stream, from_timestamp, to_timestamp, fetch)
        return result


class ChangedSingleTelemetryGraphData(TelemetryGraphData):
    def __init__(self, telemetry_client, stream,
                 column_name: str, maximum: NumberType, minimum: NumberType,
                 transform: Callable[[NumberType], NumberType],
                 auto_scale: bool = False):
        super(ChangedSingleTelemetryGraphData, self).__init__(telemetry_client, stream, column_name, maximum, minimum, auto_scale=auto_scale)
        self.transform = transform

    def fetch(self, from_timestamp: float, to_timestamp: float) -> DataType:
        result = []

        if self.collect:
            def fetch(data):
                result.extend([[d[0], d[self.column_index + 1]] for d in data])
                for i in range(len(result)):
                    result[i][1] = self.transform(result[i][1])
                if self.auto_scale:
                    self.auto_scale_data(result)

            self.telemetry_client.retrieve(self.stream, from_timestamp, to_timestamp, fetch)
        return result


class GraphController:
    def __init__(self, timepoint: float = -1, timewindow: float = 10):
        self.timepoint = timepoint
        self.timewindow = timewindow

    def pause(self) -> None:
        self.timepoint = time.time() - self.timewindow

    def resume(self) -> None:
        self.timepoint = -1


class Graph(Button):
    # noinspection PyArgumentList
    def __init__(self, rect: pygame.Rect,
                 ui_factory: BaseUIFactory, small_font=None, controller: Optional[GraphController] = None,
                 on_click: Optional[Callable[[Tuple[int, int]], None]] = None,
                 inner_colour=pygame.color.THECOLORS['white'],
                 background_colour=pygame.color.THECOLORS['black'],
                 paused_background_colour=pygame.color.THECOLORS['black'],
                 label_colour=pygame.color.THECOLORS['grey']):
        self.label_colour = label_colour
        self.small_font = small_font if small_font is not None else ui_factory.small_font
        self.title = ui_factory.label(None, "", colour=self.label_colour, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.TOP)
        self.max_label = ui_factory.label(None, "", colour=self.label_colour, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP)
        self.min_label = ui_factory.label(None, "", colour=self.label_colour, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.BOTTOM)
        self.now_label = ui_factory.label(None, "now", colour=self.label_colour, h_alignment=ALIGNMENT.RIGHT, v_alignment=ALIGNMENT.BOTTOM)
        self.time_label = ui_factory.label(None, "", colour=self.label_colour, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.BOTTOM)

        super(Graph, self).__init__(rect, on_click=self.button_cliecked)
        self.supplied_on_click = on_click
        self._graph_data: Optional[GraphData] = None
        self.border_colour = ui_factory.colour
        self.paused_border_colour = ui_factory.warning_colour
        self.inner_colour = inner_colour
        self.background_colour = background_colour
        self.paused_background_colour = paused_background_colour
        self.line_colour = (96, 96, 96)
        self.inner_rect = None
        self.units = ''
        self.controller = controller if controller is not None else self

        self.timepoint = -1
        self.timewindow = 10
        self._min_value = 0
        self._max_value = 0

    def button_cliecked(self, *_args):
        if self.supplied_on_click is not None:
            self.supplied_on_click(*_args)
        else:
            self.paused = not self.paused

    @property
    def paused(self):
        return self.controller.timepoint != -1

    @paused.setter
    def paused(self, paused: bool):
        if paused:
            self.controller.pause()
        else:
            self.controller.resume()

    def get_timepoint(self):
        return self.timepoint

    def get_timewindow(self):
        return self.timewindow

    def redefine_rect(self, rect):
        super(Graph, self).redefine_rect(rect)
        if rect is not None:
            self.inner_rect = rect.inflate(-3, -2)
            if self.title is not None:
                self.title.redefine_rect(self.inner_rect)
            if self.max_label is not None:
                self.max_label.redefine_rect(self.inner_rect)
            if self.min_label is not None:
                self.min_label.redefine_rect(self.inner_rect)
            if self.now_label is not None:
                self.now_label.redefine_rect(self.inner_rect)
            if self.time_label is not None:
                self.time_label.redefine_rect(self.inner_rect)

    @property
    def graph_data(self) -> GraphData:
        return self._graph_data

    @graph_data.setter
    def graph_data(self, graph_data: GraphData) -> None:
        self._graph_data = graph_data
        self.title.text = graph_data.name
        self._max_value = graph_data.maximum
        self._min_value = graph_data.minimum
        self._set_max_label(graph_data.maximum)
        self._set_min_label(graph_data.minimum)

    def _set_max_label(self, _max):
        self.max_label.text = f"{round(_max, 3)}"

    def _set_min_label(self, _min):
        self.min_label.text = f"{round(_min, 3)}"

    def draw(self, surface):
        if self.paused:
            pygame.draw.rect(surface, self.paused_border_colour, self.rect, 1)
        else:
            pygame.draw.rect(surface, self.border_colour, self.rect, 1)

        pygame.draw.rect(surface, self.background_colour, self.inner_rect)

        if self._graph_data is not None:

            timepoint = self.controller.timepoint
            timewindow = self.controller.timewindow

            timepoint = timepoint if timepoint >= 0 else time.time() - timewindow

            data = self._graph_data.fetch(timepoint, timepoint + timewindow + 0.01)
            graph_last_timepoint = timepoint + timewindow

            if self._max_value != self._graph_data.maximum:
                self._set_max_label(self._graph_data.maximum)
                self._max_value = self._graph_data.maximum
            if self._min_value != self._graph_data.minimum:
                self._set_min_label(self._graph_data.minimum)
                self._min_value = self._graph_data.minimum

            if len(data) > 0:
                t0 = data[0][0]
                now = time.time()

                t_minutes = now - t0
                if t_minutes < 0.1:
                    self.time_label.text = ""
                elif int(t_minutes) < 60:
                    self.time_label.text = str(int(t_minutes)) + " s"
                elif int(t_minutes) == 60:
                    self.time_label.text = "1 min"
                else:
                    self.time_label.text = str(int(t_minutes / 60)) + " mins"

                data_time_width = now - t0
                # if data_time_width < self.min_width_time:
                #     data_time_width = self.min_width_time
                # t_max = t0 + data_width
                # d_max = self.max_value

                if data_time_width <= 20:
                    minute_line_time = 1
                elif data_time_width <= 60:
                    minute_line_time = 5
                elif data_time_width <= 300:
                    minute_line_time = 25
                else:
                    minute_line_time = 300

                if data_time_width > timewindow:
                    data_time_width = timewindow

                tlast = data[-1][0]
                while t0 < tlast - data_time_width:
                    del data[0]
                    t0 = data[0][0]

                t = t0 + minute_line_time
                while t < tlast:
                    x = self.inner_rect.right - (graph_last_timepoint - t) * self.inner_rect.width / timewindow
                    pygame.draw.line(surface, self.line_colour, (x, self.inner_rect.y + 1), (x, self.inner_rect.bottom - 2), 1)
                    t += minute_line_time

                data_range = self._graph_data.maximum - self._graph_data.minimum

                if self._graph_data.minimum <= 0:
                    y = int(self.inner_rect.bottom + self._graph_data.minimum * self.inner_rect.height / data_range)
                    pygame.draw.line(surface, self.line_colour, (self.inner_rect.x, y), (self.inner_rect.right, y), 1)

                points = []
                for d in data:
                    t = d[0]
                    p = d[1]
                    # print(f"{t} : {p}")
                    if p > self._graph_data.maximum:
                        p = self._graph_data.maximum
                    elif p < self._graph_data.minimum:
                        p = self._graph_data.minimum

                    p -= self._graph_data.minimum

                    x = int(self.inner_rect.right - (graph_last_timepoint - t) * self.inner_rect.width / timewindow)
                    y = int(self.inner_rect.bottom - p * self.inner_rect.height / data_range)
                    points.append((x, y))

                if len(points) > 1:
                    pygame.draw.lines(surface, self.inner_colour, False, points)

                # points.append((x, self.inner_rect.bottom))
                # points.append((self.inner_rect.x, self.inner_rect.bottom))
                # pygame.draw.polygon(surface, self.inner_colour, points)
                # pygame.draw.polygon(surface, self.border_colour, points, 1)

                # if self.warning_value >= 0:
                #     y = self.inner_rect.bottom - self.warning_value * self.inner_rect.height / self.max_value
                #     pygame.draw.line(surface, self.warning_colour, (self.inner_rect.x + 1, y), (self.inner_rect.right - 2, y))
                #
                # if self.critical_value >= 0:
                #     y = self.inner_rect.bottom - self.critical_value * self.inner_rect.height / self.max_value
                #     pygame.draw.line(surface, self.critical_colour, (self.inner_rect.x + 1, y), (self.inner_rect.right - 2, y))

            self.title.draw(surface)
            self.max_label.draw(surface)
            self.min_label.draw(surface)
            self.now_label.draw(surface)
            self.time_label.draw(surface)
