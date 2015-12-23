#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install python-dev -y
sudo apt-get install python-virtualenv -y
sudo apt-get install postgresql-server-dev-9.3 -y
sudo apt-get install postgresql -y
sudo apt-get install postgresql-contrib -y
virtualenv venv
source venv/bin/activate
pip install Flask==0.10.1
pip install Flask-WTF==0.10.3
pip install Jinja2==2.7.3
pip install SQLAlchemy==0.9.8
pip install WTForms==2.0.1
pip install requests==2.4.3
pip install spotipy==2.1.0
pip install psycopg2==2.5.4

sudo -u postgres createuser -P -s -e vagrant
createdb audiosnowflake