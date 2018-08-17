# cesi ( Centralized Supervisor Interface )

cesi is a web interface provides manage [supervizors][1] from same interface.

For an updated version please visit https://github.com/gamegos/cesi/tree/v2_api

## Dependencies

* Python2
* Flask
* sqlite3

## Installation

```bash
$ # Install dependencies
$ # On Ubuntu 18.04
$ sudo apt-get install sqlite3 python python-flask
$ # On Centos 7
$ sudo yum install git python-flask

$ # # Download the project
$ sudo git clone https://github.com/gamegos/cesi /opt/cesi

$ # Create user database
$ sudo sqlite3 /opt/cesi/userinfo.db < /opt/cesi/userinfo.sql

$ # Create cesi.conf file.
$ sudo cp /opt/cesi/defaults/cesi.conf /etc/cesi.conf

$ # If you want to change configuration of cesi, update cesi.conf for your environment.
$ sudo vim /etc/cesi.conf
```

## Usage

```bash
$ # Run with command line
$ sudo python /opt/cesi/cesi/web.py

$ # Run as a service
$ sudo cp /opt/cesi/defaults/cesi.service /etc/systemd/system/cesi.service
$ sudo systemctl daemon-reload
$ sudo systemctl start cesi
```

## First Login

Please change password after first login!

- **Username**: admin

- **Password** : admin

## Mailing list

cesi-commit@googlegroups.com

cesi-devel@googlegroups.com


## Screenshots

![Dashboard](https://github.com/GulsahKose/cesi/blob/master/screenshots/image2)


![Showall](https://github.com/GulsahKose/cesi/blob/master/screenshots/image1)

## Blog

[Usage][2]


[1]: http://supervisord.org/
[2]: http://www.gulsahkose.com/2014/09/cesi-centralized-supervisor-interface.html
