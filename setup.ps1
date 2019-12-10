#!/bin/ps1
.\\venv\Scripts\Activate.ps1
$env:FLASK_APP="guacamole"
$env:FLASK_ENV="development"
flask "init-db"
echo Initialized Database
flask run