# Home automation

## Installation
```shell
pip3 install david-home-automation==0.1.24
(sudo apt install --yes expect && cd $(mktemp -d) && git clone https://github.com/Heckie75/eQ-3-radiator-thermostat.git x && cd x && cp eq3.exp $HOME/.local/bin)

# (Optional) find your thermostat MACs via
bluetoothctl devices

# Create your config once 
cat > ~/.config/david-home-automation.yaml <<EOF
thermostats:
  - mac_address: XX:XX:XX:XX:XX:XX
    name: Arbeitszimmer
hosts:
  - broadcast_ip: 192.168.178.1
    mac_address: XX:XX:XX:XX:XX:XX
    name: Desktop
EOF

# You can also pass your config file path via an env variable
export HOME_AUTOMATION_CONFIG=your/path

python3 -m david_home_automation.server --server-host=0.0.0.0 --server-port 5000
```

## Development

- [Install poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions)

```
FLASK_ENV=development FLASK_APP=david_home_automation/main poetry run flask run --host=0.0.0.0 --port 5050
```

## As a service

```shell
sudo apt install --yes supervisor
./install.sh

# killall supervisord; supervisord -c /etc/supervisord.conf

cp home_automation.service ~/.config/systemd/user/home_automation.service
systemctl --user daemon-reload
systemctl --user start home_automation.service
systemctl --user status home_automation.service
```