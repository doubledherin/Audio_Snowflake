!#/bin/bash

sudo apt-get install python-virtualenv
sudo apt-get install postgresql-server-dev-9.3
sudo apt-get install postgresql
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt