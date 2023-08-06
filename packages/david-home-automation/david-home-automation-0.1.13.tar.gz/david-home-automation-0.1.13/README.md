# Home automation

## Installation
```
pip3 install david-home-automation==0.1.13
(sudo apt install --yes expect && cd $(mktemp -d) && git clone https://github.com/Heckie75/eQ-3-radiator-thermostat.git x && cd x && cp eq3.exp $HOME/.local/bin)
# Run server
FLASK_APP=david_home_automation.main flask run --host=0.0.0.0 --port 5050
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
```