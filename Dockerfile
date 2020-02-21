# Base image
FROM python:3-alpine

# Information
LABEL maintainer="FrozenFOXX <frozenfoxx@churchoffoxx.net>"

# Variables
WORKDIR /app
ENV APPDIR="/app" \
  BUILD_DEPS="gcc musl-dev postgresql-dev"

# Add requirements
COPY requirements.txt ./
RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps ${BUILD_DEPS} && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

# Copy app source
COPY . .

# Launch
ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]
