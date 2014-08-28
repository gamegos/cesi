#cesi ( Centralized Supervisor Interface )

cesi is a web interface provides manage supervizors from same interface.

## Dependencies

* Python ==> 2.7.6
* Flask
* xmlrpclib
* mmap
* ConfigParser
* sqlite3

## Installation
    sudo apt-get install sqlite3, python, Flask

    sqlite3 path/to/userinfo.db < userinfo.sql

## Configuration

Fill cesi.conf.example

    mv cesi.conf.example cesi.conf

    cp cesi.conf /etc/cesi.conf


