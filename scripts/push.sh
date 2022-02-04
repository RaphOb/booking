#! /usr/bin/env sh

# Exit in case of error
set -e

TAG=${TAG?Variable not set} \
docker-compose \
-f docker-compose.yml \
push
# TODO docker push à la place de docker-compose 
#  registry:domain/image:tag