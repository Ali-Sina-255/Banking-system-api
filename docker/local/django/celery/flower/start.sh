#!/bin/bash

set -o errexit
set -o nounset

# Run Flower with basic auth using env vars
exec watchfiles --filter python celery.__main__.main \
    args \
    "-A config.celery_app -b \ "${CELERY_BROKER}" \ flower

    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}""