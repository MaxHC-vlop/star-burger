#!/bin/bash

cd /opt/star-burger/
git pull origin master
echo "git ok"
npm ci
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo "frontend ok"
./env/bin/python3.10 -m pip install -r requirements.txt
./env/bin/python3.10 manage.py collectstatic --noinput
./env/bin/python3.10 manage.py migrate --noinput
echo "backend ok"
sudo systemctl daemon-reload
sudo systemctl reload nginx
sudo systemctl stop django.service
sudo systemctl start django.service
echo "systemctl start ok"
last_commit_hash=$(git rev-parse HEAD)
echo $last_commit_hash
source ./star_burger/.env
curl -H "X-Rollbar-Access-Token: ${ROLLBAR_ACCESS_TOKEN}" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "production", "revision": "'${last_commit_hash}'", "rollbar_name": "kiablunovskii", "local_username": "root", "comment": "auto deploy", "status": "succeeded"}'
echo "End deploy!"