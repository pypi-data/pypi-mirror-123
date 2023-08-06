import os
import time
import typing

from flask import Flask, request, jsonify, send_from_directory
from wakeonlan import send_magic_packet

from david_home_automation.config import Host
from david_home_automation.config_hausackerweg import CONFIG

app = Flask(__name__)

# eq3_exp_executable = '/usr/bin/eq3.exp'
eq3_exp_executable = 'eq3.exp'


def get_host_by_name(name: str) -> typing.Optional[Host]:
    for host in CONFIG.wake_on_lan:
        if host.name == name:
            return host
    return None


@app.route("/")
def main():
    return send_from_directory('static', 'index.html')


@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory('static', path)


@app.route("/api/thermostats", methods=['GET'])
def list_thermostats():
    return jsonify(CONFIG.thermostats)


@app.route("/api/hosts", methods=['GET'])
def list_hosts():
    return jsonify(CONFIG.wake_on_lan)


@app.route("/api/thermostats/change-temperature", methods=['POST'])
def change_thermostat_temperature():
    body = request.get_json(force=True)
    name = body.get('name')
    thermostat = CONFIG.get_thermostat_by_name(name)
    if not name or not thermostat:
        return dict(error='invalid name'), 400
    try:
        temperature = float(body.get('temperature'))
    except:
        return dict(error='could not parse temperature'), 400

    os.system(thermostat.eq3_cmd(f'temp {temperature:.1f}'))
    return jsonify(dict())


@app.route("/api/thermostats/change-to-automatic", methods=['POST'])
def change_thermostat_to_automatic():
    body = request.get_json(force=True)
    name = body.get('name')
    thermostat = CONFIG.get_thermostat_by_name(name)
    if not name or not thermostat:
        return dict(error='invalid name'), 400
    os.system(thermostat.eq3_cmd(f'auto'))
    return jsonify(dict())


@app.route("/api/wake-on-lan", methods=['POST'])
def wake_up_host():
    body = request.get_json(force=True)
    name = body.get('name')
    host = get_host_by_name(name)
    if not name or not host:
        return dict(error='invalid name'), 400
    # Retry once or twice
    for _ in range(4):
        send_magic_packet(host.mac_address)
        time.sleep(0.5)
    return jsonify(dict())
