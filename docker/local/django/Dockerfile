# Stage 1: Build dependencies and wheels
ARG PYTHON_VERSION=3.11-slim-bookworm
FROM python:${PYTHON_VERSION} AS python-build-stage

ARG BUILD_ENVIRONMENT=local

# Prevents tzdata from prompting
ENV DEBIAN_FRONTEND=noninteractive

# Install system build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    python3-dev \
    cargo \
    ca-certificates \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirement files into image
COPY ./requirement .

# Build wheels from the selected requirements file (e.g., local.txt)
RUN test -f ${BUILD_ENVIRONMENT}.txt && \
    pip wheel -v --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Stage 2: Final runtime image
FROM python:${PYTHON_VERSION} AS python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BUILD_ENV=${BUILD_ENVIRONMENT}
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR ${APP_HOME}

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    gettext \
    sudo \
    git \
    nano \
    bash-completion \
    openssh-client \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Add django user and set permissions
RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles

# Copy built wheels from build stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels

# Install Python packages from wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && \
    rm -rf /wheels/

# Copy entry scripts and make them executable
COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint.sh
COPY --chown=django:django ./docker/local/django/start.sh /start.sh
COPY --chown=django:django ./docker/local/django/celery/worker/start.sh /start-celeryworker.sh
COPY --chown=django:django ./docker/local/django/celery/beat/start.sh /start-celerybeat.sh
COPY --chown=django:django ./docker/local/django/celery/flower/start.sh /start-flower.sh

# Fix line endings and permissions
RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh /start-celeryworker.sh /start-celerybeat.sh /start-flower.sh && \
    chmod +x /entrypoint.sh /start.sh /start-celeryworker.sh /start-celerybeat.sh /start-flower.sh

# Copy full project code
COPY --chown=django:django . ${APP_HOME}

# Switch to unprivileged user
USER django
ENTRYPOINT ["/entrypoint.sh"]
