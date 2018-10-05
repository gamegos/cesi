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
- [Docker][4] (unavailable)
- [Manuel Instructions](#manuel-instructions)

## Manuel Instructions

**Install Dependencies For Cesi Api**

```bash
$ # On Ubuntu [18.04, 16.04, 14.04]
$ sudo apt install -y git python3 python3-pip
$ # On Centos 7
$ sudo yum install -y git epel-release
$ sudo yum install -y python34 python34-pip
$ # On Fedora 28
$ sudo dnf install -y git python3 python3-pip
```

**Install Dependencies For Cesi Ui (Optional)**

```bash
$ # On Ubuntu [18.04]
$ sudo apt install -y nodejs npm
$ sudo npm install -g yarn
$ # On Centos 7
$ sudo yum install -y nodejs
$ sudo npm install -g yarn
```

**Install Cesi**

```bash
$ export CESI_SETUP_PATH=~/cesi

$ # Download the project to ~/cesi directory
$ git clone https://github.com/gamegos/cesi $CESI_SETUP_PATH

$ # Create virtual environment and install requirement packages
$ cd $CESI_SETUP_PATH
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt

# There are 2 options for ui.
$ # 1. Build ui (First you must install dependencies for ui)
(venv) $ cd ${CESI_SETUP_PATH}/cesi/ui
(venv) $ yarn install
(venv) $ yarn build

$ # 2. Download the builded ui
(venv) $ cd ${CESI_SETUP_PATH}/cesi/ui
(venv) $ wget https://github.com/gamegos/cesi/releases/download/v2.2/build-ui.tar -O build.tar
(venv) $ tar -xvf build.tar

$ # Run with command line
(venv) $ python3 ${CESI_SETUP_PATH}/cesi/run.py --config ${CESI_SETUP_PATH}/defaults/cesi.conf
```

**Install Cesi as a service**

```bash
$ # If you want to change CESI_SETUP_PATH and don't want to install packages globally, you must change the configurations in the cesi.service file.

$ export CESI_SETUP_PATH=/opt/cesi

$ # Download the project to /opt/cesi directory
$ sudo git clone https://github.com/gamegos/cesi $CESI_SETUP_PATH

$ # Install Requirement Packages Into Global Enviroment
$ cd $CESI_SETUP_PATH
$ sudo pip3 install -r requirements.txt

$ # There are 2 options for ui.
$ # 1. Build ui (First you must install dependencies for ui)
$ cd ${CESI_SETUP_PATH}/cesi/ui
$ sudo yarn install
$ sudo yarn build

$ # 2. Download the builded ui
$ cd ${CESI_SETUP_PATH}/cesi/ui
$ wget https://github.com/gamegos/cesi/releases/download/v2.2/build-ui.tar -O build.tar
$ tar -xvf build.tar

$ # Create cesi.conf file and update cesi.conf for your environment.
$ # Config file documentation can be found inside default file.
$ # (You must create cesi.conf in the etc directory for cesi.service)
$ sudo cp ${CESI_SETUP_PATH}/defaults/cesi.conf /etc/cesi.conf

$ # Run as a service
$ sudo cp ${CESI_SETUP_PATH}/defaults/cesi.service /etc/systemd/system/cesi.service
$ sudo systemctl daemon-reload
$ sudo systemctl start cesi
```

## First Login

Please change password after first login!

- **Username:** admin
- **Password:** admin

## TODO

- [x] Fix user related api endpoints
- [ ] Fix node log view
- [ ] Refactor the usage of config
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
