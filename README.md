#cesi ( Centralized Supervisor Interface )

cesi is a web interface provides manage [supervizors][1] from same interface.

## Dependencies

* Python ==> 2.7.6
* Flask
* xmlrpclib
* mmap
* ConfigParser
* sqlite3

## Installation
    sudo apt-get install sqlite3, python, python-flask

    sqlite3 path/to/userinfo.db < userinfo.sql

## Configuration

Fill cesi.conf.example

    mv cesi.conf.example cesi.conf

    cp cesi.conf /etc/cesi.conf

## Run Project
    git clone https://github.com/GulsahKose/cesi
    cd cesi
    python web.py

## Mailing list

cesi-commit@googlegroups.com

cesi-devel@googlegroups.com

[1]: http://supervisord.org/

