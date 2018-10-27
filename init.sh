#!/bin/bash
source ./services/github/.env
source ./services/looker/.env
export DX_IP="$(docker-machine ip dx-automator-dev)"