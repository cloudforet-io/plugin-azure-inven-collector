#!/usr/bin/env bash
# Build a docker image
docker build -t pyengine/azure-cloud-services . --no-cache

docker tag pyengine/azure-cloud-services pyengine/azure-cloud-services:1.0
docker tag pyengine/azure-cloud-services spaceone/azure-cloud-services:1.0