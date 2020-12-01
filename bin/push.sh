#!/usr/bin/env bash
# How to upload
./bin/build.sh

docker push pyengine/azure-cloud-services:1.0
docker push spaceone/azure-cloud-servicess:1.0