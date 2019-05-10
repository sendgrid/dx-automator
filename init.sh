#!/bin/bash
source ./source_the_things.sh
docker-machine start dx-automator-dev
docker-machine env dx-automator-dev
eval $(docker-machine env dx-automator-dev)
export DX_IP="$(docker-machine ip dx-automator-dev)"
docker-compose -f docker-compose-dev.yml up -d --build
./scripts/setup-local-db
