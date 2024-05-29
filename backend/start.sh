#!/bin/bash

python ./src/jobsearch.py
python ./src/data_explore.py
python ./src/create_db.py
python ./src/query_and_visualize.py

gunicorn backend.wsgi:application --log-file -
