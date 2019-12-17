#!/bin/bash
if [ ! -d "venv" ];
then
    python3 -m venv venv
    pip install flask pyrebase4
fi
. venv/bin/activate
export FLASK_APP=guacamole
export FLASK_ENV=development
flask run