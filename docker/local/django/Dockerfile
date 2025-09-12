# ARG and FROM Python version
ARG PYTHON_VERSION=3.11.2-bullseye
FROM python:${PYTHON_VERSION} AS python-build-stage

ARG BUILD_ENVIRONMENT=local

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    python3-dev \
    libffi-dev \
    libjpeg-dev

# Copy the entire requirement directory into the image
COPY ./requirement/ .

# Ensure the pip version is up-to-date
RUN pip install --upgrade pip


# Create wheels from the specified environment file
RUN pip wheel -v --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

# Final image setup
FROM python:${PYTHON_VERSION} AS python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

# Set the working directory
WORKDIR ${APP_HOME}

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImport=false \
    && rm -rf /var/lib/apt/lists/*

# Create the /wheels directory if it doesn't exist (prevent "No such file or directory" error)
RUN mkdir -p /wheels

# Copy wheels from the build stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels

# Verify wheels are present and install packages from them
RUN ls -alh /wheels  # To check the contents of /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# Add django user and set permissions
RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles

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
