#!/bin/bash

set -o errexit  # Exit on error
set -o nounset  # Treat unset variables as an error

# Run Flower with basic auth using environment variables
exec celery flower -A config.celery_app -b "${CELERY_BROKER}" \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
