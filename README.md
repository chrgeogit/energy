# energy
collect and project kwh consumption from mains

#instructions

get a raspberry with linux
  PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
  NAME="Raspbian GNU/Linux"
  VERSION_ID="10"
  VERSION="10 (buster)"
  VERSION_CODENAME=buster
  ID=raspbian
  ID_LIKE=debian

install and start services provided

install python3 and flask

  Name: Flask
  Version: 2.2.2
  Summary: A simple framework for building complex web applications.
  Home-page: https://palletsprojects.com/p/flask
  Author: Armin Ronacher
  Author-email: armin.ronacher@active-4.com
  License: BSD-3-Clause
  Location: /usr/local/lib/python3.7/dist-packages
  Requires: itsdangerous, click, Werkzeug, Jinja2, importlib-metadata
  Required-by: Flask-Cors

install database  SQLite 3.x and create "db1" file using below command
  CREATE TABLE IF NOT EXISTS "mes" (
        "id"    integer,
        "volt"  text,
        "current"       text,
        "powewr"        text,
        "energy"        text,
        "date"  text,
        PRIMARY KEY("id" AUTOINCREMENT)
);


check the services files and put the files in the directory mentioned there

hire a liscenced electrician to mount the below kwh meter it onto mains and route its rs485 signal to rpi
![dds238](https://github.com/chrgeogit/energy/assets/144347707/1ee61b00-2d39-4d74-8952-732f1df2508a)

Last but not least dont forget to visit http://rpiIP:5000/api/power to see your power Consumption graph


[Power.pdf](https://github.com/chrgeogit/energy_consumption/files/12646828/Power.pdf)
