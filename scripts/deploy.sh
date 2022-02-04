#! /usr/bin/env sh

# Exit in case of error
set -a && . .env && set +a

# DOMAIN=${DOMAIN?Variable not set} \
# TRAEFIK_TAG=${TRAEFIK_TAG?Variable not set} \
# STACK_NAME=${STACK_NAME?Variable not set} \
# TAG=${TAG?Variable not set} \


docker stack deploy -c docker-compose.yml "${STACK_NAME?Variable not set}"
