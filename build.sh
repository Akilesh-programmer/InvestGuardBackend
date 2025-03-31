#!/bin/zsh
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn project.wsgi:application --bind 0.0.0.0:8000
