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
COPY ./requirement .

# Ensure the pip version is up-to-date
RUN pip install --upgrade pip

# Create wheels from the specified environment file
RUN pip wheel -v --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Final image               as run-stage
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
    sudo git bash-completion nano ssh \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImport=false \
    && rm -rf /var/lib/apt/lists/*

Run addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir - p${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles \

# Copy wheels from the build stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels


# Verify wheels are present and install packages from them
RUN ls -alh /wheels  # To check the contents of /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# Copy entrypoint.sh script and make it executable
COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint.sh
COPY --chown=django:django ./docker/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /entrypoint.sh.sh /start.sh && \
    chmod +x /entrypoint.sh.sh /start.sh


COPY --chown=django:django . ${APP_HOME}

USER django


ENTRYPOINT ["/entrypoint.sh"]