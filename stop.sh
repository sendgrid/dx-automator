#!/bin/bash
docker-compose -f docker-compose-dev.yml stop
docker-compose -f docker-compose-dev.yml down
docker-machine stop dx-automator-dev
