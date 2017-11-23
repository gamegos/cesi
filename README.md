#cesi ( Centralized Supervisor Interface )

cesi is a web interface provides manage [supervizors][1] from same interface.

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

## Run With Docker

If you would like to run image, you must copy your config file in local pc in /etc/ directory.

    docker run -d -p 5000:5000 -v /path/to/config/:/etc/ burcina/docker-cesi


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


## TODO

- Filter nodes from left menu
- Group nodes by groups and environments
- Do not use external adresses for javascript and css libraries 
- Remove angular, vs from login page
- Changeerror page template
- Change server port with config
- Change page title with config
- Better format activity log (tabbed date, level, component, message)
- Fix batch action buttons 
- Auto refresh page
- Option to select different templates
- Readlog button for processes
- Show process logs