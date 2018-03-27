#cesi ( Centralized Supervisor Interface )

cesi is a web interface provides manage [supervizors][1] from same interface.

For an updated version please visit https://github.com/gamegos/cesi/tree/v2_api

## Dependencies

* Python
* Flask
* sqlite3

## Installation

    $sudo apt-get install sqlite3 python python-flask

    $git clone https://github.com/Gamegos/cesi

    $cd cesi

    $sqlite3 path/to/userinfo.db < userinfo.sql

## Configuration

Fill cesi.conf

    #cp cesi.conf /etc/cesi.conf

## Run Project

    $python web.py

## First Login

Please change password after first login!

Username : admin

Password : admin

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
