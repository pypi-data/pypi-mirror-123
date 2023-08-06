# Home automation


- [Install poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions)

```
FLASK_ENV=development FLASK_APP=david_home_automation/main poetry run flask run --host=0.0.0.0
```


## Dependencies
```
(sudo apt install --yes expect && cd $(mktemp -d) && git clone https://github.com/Heckie75/eQ-3-radiator-thermostat.git x && cd x && cp eq3.exp $HOME/.local/bin)
```

## As a service

```shell
sudo apt install --yes supervisor
./install.sh

# killall supervisord; supervisord -c /etc/supervisord.conf
```