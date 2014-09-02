#!/bin/bash

echo "Installation starting..."

echo -e "Please enter your database path: "
read database_path

/usr/bin/sqlite3 $database_path < ./userinfo.sql

echo "Your username=admin and password=admin. Please change your password."

sudo mkdir /etc/cesi

mv ./cesi.conf.example ./cesi.conf

sudo cp ./cesi.conf /etc/cesi/

echo "Finish..."
