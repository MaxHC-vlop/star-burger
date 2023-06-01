#!/bin/bash

git pull origin master
echo "git ok"
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
echo "Docker-compose ok"

last_commit_hash=$(git rev-parse HEAD)
echo $last_commit_hash

source .env
curl -H "X-Rollbar-Access-Token: ${ROLLBAR_ACCESS_TOKEN}" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "production", "revision": "'${last_commit_hash}'", "rollbar_name": "kiablunovskii", "local_username": "root", "comment": "auto deploy", "status": "succeeded"}'
echo "End docker deploy!"