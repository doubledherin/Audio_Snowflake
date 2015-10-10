#!/bin/bash

APP_NAME=audiosnowflake
VENV=${APP_NAME}env

sudo apt-get install  python-dev -y
sudo apt-get install postgresql-client -y
sudo apt-get install postgresql-server-dev-9.3 -y
sudo apt-get install postgresql postgresql-contrib -y
sudo apt-get install python-virtualenv -y

virtualenv $VENV
source $VENV/bin/activate
pip install -r requirements.txt
