#!/bin/bash
docker-compose -f docker-compose-dev.yml stop
docker-compose -f docker-compose-dev.yml down
docker rmi dx-automator_github-service
docker rmi dx-automator_hacktoberfest
docker rmi dx-automator_users
docker rmi dx-automator_nginx
docker rmi dx-automator_looker
docker rmi dx-automator_tasks
docker rmi dx-automator_users-db
docker rmi dx-automator_looker-db
docker rmi dx-automator_tasks-db
docker rmi dx-automator_client-react
docker-machine stop dx-automator-dev