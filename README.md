# CeSI (Centralized Supervisor Interface)

CeSI is a web interface for managing multiple [supervisors][1] from the same
place.

Supervisor has its own web UI but managing multiple supervisor installations is
hard with seperate UIs (If you are using the UI of course :). CeSI aims to solve
this problem by creating a centralized web UI, based on the RPC interface of
Supervisor.

## Installation

For running CeSI inside a docker container without installation see "Usage"
section.

**Install Dependencies For Api**

```bash
$ # On Ubuntu [18.04, 16.04, 14.04]
$ sudo apt install -y git python3 python3-pip
$ # On Centos 7
$ sudo yum install -y git epel-release
$ sudo yum install -y python34 python34-pip
$ # On Fedora 28
$ sudo dnf install -y git python3 python3-pip
```

**Install Dependencies For Ui (Optional)**

```bash
$ # On Ubuntu [18.04]
$ sudo apt install -y nodejs npm
$ sudo npm install -g yarn
$ # On Centos 7
$ sudo yum install -y nodejs
$ sudo npm install -g yarn
```

**Installation**

Then run these commands to install CeSI

```bash
$ export CESI_SETUP_PATH=/opt/cesi

$ # Download the project to /opt/cesi directory
$ sudo git clone https://github.com/gamegos/cesi $CESI_SETUP_PATH


$ # Install Requirement Packages Into Global Enviroment
$ cd $CESI_SETUP_PATH
$ sudo pip3 install -r requirements.txt

$ # Build ui (Optional)
$ cd ${CESI_SETUP_PATH}/cesi/ui
$ sudo yarn install
$ sudo yarn build

$ # Download the builded ui
$ cd ${CESI_SETUP_PATH}/cesi/ui
$ wget https://github.com/gamegos/cesi/releases/download/2.0/build-ui.tar -O build.tar
$ tar -xvf build.tar

$ # Create cesi.conf file and update cesi.conf for your environment.
$ # Config file documentation can be found inside default file.
$ # (You must create cesi.conf in the etc directory for cesi.service)
$ sudo cp ${CESI_SETUP_PATH}/defaults/cesi.conf /etc/cesi.conf
```

## Usage

```bash
$ # Run with command line
$ sudo python3 ${CESI_SETUP_PATH}/cesi/run.py --config path/to/cesi.conf

$ # Run as a service
$ sudo cp ${CESI_SETUP_PATH}/defaults/cesi.service /etc/systemd/system/cesi.service
$ sudo systemctl daemon-reload
$ sudo systemctl start cesi
```

### First Login

Please change password after first login!

- **Username:** admin
- **Password:** admin

## Blog

[Usage][2]

[1]: http://supervisord.org/
[2]: http://www.gulsahkose.com/2014/09/cesi-centralized-supervisor-interface.html

## TODO

- [x] Fix user related api endpoints
- [ ] Fix node log view
- [ ] Refactor the usage of config
- [ ] Rewrite dockerfile and publish image on docker hub under gamegos
- [ ] Improve Docs
- [ ] Do not use external adresses for javascript and css libraries
- [ ] Use a logging lib
- [ ] Better format for activity logs (tabbed date, level, component, message)
- [ ] Auto refresh page
- [ ] Option to select different templates
- [x] Upgrade flask
- [ ] Add tests
- [ ] CI integration
