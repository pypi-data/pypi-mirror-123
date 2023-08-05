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

import os
import time
import pyros

AGENT_PING_TIMEOUT = 10

_returncodes = {}

_agents = []

_lastPinged = 0

_agent_files = {}


def init(_client, filename, optional_files=None, agent_id=None):
    def send_file(_agent_id, _dest_path, _filename):
        with open(_filename, "rb") as f:
            _file_content = f.read()

            extra_name = os.path.join(_dest_path, os.path.split(_filename)[1])
            _agent_files[_agent_id].append(extra_name)

            pyros.publish("exec/" + _agent_id + "/process/" + extra_name, _file_content)

    def process_dir(_agent_id, _dest_path, _dir):
        for _file in os.listdir(_dir):
            if not _file.endswith('__pycache__'):
                if os.path.isdir(_file):
                    process_dir(_agent_id, os.path.join(_dest_path, _file), os.path.join(_dir, _file))
                else:
                    send_file(_agent_id, _dest_path, os.path.join(_dir, _file))

    # print("Connected to Rover " + str(client))
    if agent_id is None:
        if filename.endswith(".py"):
            agent_id = filename[: len(filename) - 3]
        else:
            agent_id = filename
            agent_id = agent_id.replace("/", "-")

        if "/" in agent_id:
            segments = agent_id.split("/")
            agent_id = segments[len(segments) - 1]

    with open(filename) as file:
        file_content = file.read()

    _agents.append(agent_id)
    _returncodes[agent_id] = None

    _agent_files[agent_id] = [agent_id + ".py"]

    pyros.subscribe("exec/" + str(agent_id) + "/out", process)
    pyros.subscribe("exec/" + str(agent_id) + "/status", process)
    pyros.publish("exec/" + str(agent_id), "stop")
    pyros.publish("exec/" + str(agent_id) + "/process", file_content)
    if optional_files is not None:
        for extra_file in optional_files:
            if os.path.isdir(extra_file):
                process_dir(agent_id, os.path.split(extra_file)[1], extra_file)
            else:
                send_file(agent_id, "", extra_file)

    pyros.publish("exec/" + str(agent_id), "make-agent")


def process(topic, message, _groups):
    if topic.startswith("exec/"):
        if topic.endswith("/out"):
            if len(message) > 0:
                agent_id = topic[5: len(topic) - 4]
                if message.endswith("\n"):
                    print(agent_id + ": " + message, end="")
                else:
                    print(agent_id + ": " + message)
            return True
        elif topic.endswith("/status"):
            agent_id = topic[5: len(topic) - 7]
            if message.startswith("stored "):
                filename = message[7:]
                if filename not in _agent_files[agent_id] and filename.endswith("_main.py"):
                    filename = filename[:-8] + ".py"
                if filename in _agent_files[agent_id]:
                    i = _agent_files[agent_id].index(filename)
                    del _agent_files[agent_id][i]
                    if len(_agent_files[agent_id]) == 0:
                        pyros.publish("exec/" + str(agent_id), "restart")
            elif message.startswith("exit"):
                if len(message) > 5:
                    _returncodes[agent_id] = message[5:]
                else:
                    _returncodes[agent_id] = "-1"

            return True

    return False


def stop_agent(_client, process_id):
    pyros.publish("exec/" + process_id, "stop")
    del _agents[process_id]


def keep_agents():
    global _lastPinged
    now = time.time()

    if now - _lastPinged > AGENT_PING_TIMEOUT:
        _lastPinged = now
        for agentId in _agents:
            pyros.publish("exec/" + agentId, "ping")


def returncode(agentId):
    return _returncodes[agentId]
