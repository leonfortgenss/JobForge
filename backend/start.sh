#!/bin/bash

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python ./src/jobsearch.py
python ./src/data_explore.py
python ./src/create_db.py
python ./src/query_and_visualize.py

python manage.py collectstatic --noinput

python manage.py migrate

gunicorn backend.wsgi:application --log-file -
