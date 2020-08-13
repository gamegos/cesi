# CeSI (Centralized Supervisor Interface)

CeSI is a web interface for managing multiple [supervisors][1] from the same
place.

Supervisor has its own web UI but managing multiple supervisor installations is
hard with seperate UIs (If you are using the UI of course :). CeSI aims to solve
this problem by creating a centralized web UI, based on the RPC interface of
Supervisor.

## Installation Methods

- [Chef Cookbook][2]
- [Package managers][3]
- [Docker][4]
- [Manuel Instructions](#manuel-instructions)

## Manuel Instructions

**Install Dependencies For Cesi Api**

```bash
$ # On Ubuntu [18.04, 16.04, 14.04]
$ sudo apt install -y git python3 python3-pip python3-venv
$ # On Centos 7
$ sudo yum install -y git epel-release
$ sudo yum install -y python34 python34-pip python34-venv
$ # On Fedora 28
$ sudo dnf install -y git python3 python3-pip python3-venv
```

**Install Cesi**

```bash
$ export CESI_SETUP_PATH=~/cesi
$ mkdir ${CESI_SETUP_PATH}
$ cd ${CESI_SETUP_PATH}

$ # Download the project to ~/cesi directory
$ wget https://github.com/gamegos/cesi/releases/download/v2.7.1/cesi-extended.tar.gz -O cesi.tar.gz
$ tar -xvf cesi.tar.gz

$ # Create virtual environment and install requirement packages
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt

$ # Run with command line
(venv) $ python3 ${CESI_SETUP_PATH}/cesi/run.py --config-file ${CESI_SETUP_PATH}/defaults/cesi.conf.toml
```

**Install Cesi as a service**

```bash
$ # If you want to change CESI_SETUP_PATH, you must change the configurations in the cesi.service file.
$ export CESI_SETUP_PATH=/opt/cesi
$ mkdir ${CESI_SETUP_PATH}
$ cd ${CESI_SETUP_PATH}

$ # Download the project to CESI_SETUP_PATH directory
$ wget https://github.com/gamegos/cesi/releases/download/v2.7.1/cesi-extended.tar.gz -O cesi.tar.gz
$ tar -xvf cesi.tar.gz

$ # Create virtual environment and install requirement packages
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
(venv) $ deactivate   # Deactivate virtual environment

$ # Build ui (First you must install dependencies for ui -> yarn) - Optional
$ cd ${CESI_SETUP_PATH}/cesi/ui
$ yarn install
$ yarn build

$ # Create cesi.conf.toml file and update cesi.conf.toml for your environment.
$ # Config file documentation can be found inside default file.
$ # (You must create cesi.conf in the etc directory for cesi.service)
$ sudo cp ${CESI_SETUP_PATH}/defaults/cesi.conf.toml /etc/cesi.conf.toml

$ # Run as a service
$ sudo cp ${CESI_SETUP_PATH}/defaults/cesi.service /etc/systemd/system/cesi.service
$ sudo systemctl daemon-reload
$ sudo systemctl start cesi
```

**Running Cesi with uWSGI**

You may want to run Cesi using uWSGI (or any other WSGI deamon). Configure your system in the similiar way to running as a service and use `uwsgi` to start app. Check `defaults/cesi-uwsgi.ini` for details.

While running with uWSGI Cesi config host and port are ignored.

**Run Cesi with Docker**

```
$ # Download the project (update version to fit your needs)
$ wget --output-document cesi.tar.gz https://github.com/gamegos/cesi/releases/download/v2.7.1/cesi-extended.tar.gz
$ tar -xzvf cesi.tar.gz
$ cd cesi/
$ docker build -t=cesi:2.7.1 .

$ # Add --detach to background container
$ docker run --publish 5000:5000 cesi:2.7.1

$ # Open browser to http://localhost:5000 or http://127.0.0.1:5000
```

## First Login

Please change password after first login!

- **Username:** admin
- **Password:** admin

## TODO

- [x] Fix user related api endpoints
- [ ] Fix node log view
- [x] Refactor the usage of config
- [ ] Rewrite dockerfile and publish image on docker hub under gamegos
- [ ] Improve Docs
- [x] Do not use external adresses for javascript and css libraries
- [ ] Use a logging lib
- [ ] Better format for activity logs (tabbed date, level, component, message)
- [ ] Auto refresh page
- [ ] Option to select different templates
- [x] Upgrade flask
- [ ] Add tests
- [ ] CI integration

[1]: http://supervisord.org/
[2]: https://github.com/gamegos/cesi-cookbook/
[3]: https://github.com/gamegos/cesi-packaging/
[4]: https://hub.docker.com/r/gamegos/cesi/
