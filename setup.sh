#!/bin/bash
if [ ! -d "venv" ];
then
    python3 -m venv venv
    pip3 install flask pyrebase4
fi
. venv/bin/activate
export FLASK_APP=guacamole
#export FLASK_ENV=development

if [ "$1" = "ip" ]
then
    flask run --host=$2
else
    flask run --no-reload
fi