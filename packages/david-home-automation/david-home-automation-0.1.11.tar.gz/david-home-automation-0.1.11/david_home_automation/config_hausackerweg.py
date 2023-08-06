from david_home_automation.config import Config, Host, BluetoothThermostat

CONFIG = Config(
    thermostats=[
        BluetoothThermostat(
            name='Arbeitszimmer',
            mac_address='00:1A:22:12:34:E7'
        ),
        BluetoothThermostat(
            name='Schlafzimmer',
            mac_address='00:1A:22:12:21:10'
        ),
    ],
    wake_on_lan=[
        Host(
            name='Desktop',
            mac_address='08:60:6e:e6:04:97',
            broadcast_ip='192.168.178.1'
        )
    ]
)
