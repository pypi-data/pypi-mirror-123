import typing
from dataclasses import dataclass


@dataclass
class Host(object):
    name: str
    mac_address: str
    broadcast_ip: str = '255.255.255.255'


@dataclass
class BluetoothThermostat(object):
    name: str
    mac_address: str

    def eq3_cmd(self, cmd):
        return f'eq3.exp {self.mac_address} {cmd}'


@dataclass
class Config(object):
    wake_on_lan: typing.List[Host]
    thermostats: typing.List[BluetoothThermostat]

    def get_host_by_name(self, name: str) -> typing.Optional[Host]:
        return self._get_by('wake_on_lan', name)

    def get_thermostat_by_name(self, name: str) -> typing.Optional[BluetoothThermostat]:
        return self._get_by('thermostats', name)

    def _get_by(self, attr: str, name: str):
        for el in getattr(self, attr):
            if el.name == name:
                return el
        return None
